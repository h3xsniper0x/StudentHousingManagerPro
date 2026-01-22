from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from applications.models import HousingApplication
from housing.models import Building, Room
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.admin_dashboard_url = reverse('admin_dashboard')
        self.student_dashboard_url = reverse('home') # 'home' redirects to student dashboard if role is student, or is the dashboard
        
        # Minimal valid GIF
        self.valid_image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'

    def test_student_registration_creates_user_and_application(self):
        """
        PRD 3.1 & 3.2: Verify that registering a student creates a User record 
        and automatically creates a HousingApplication.
        """
        profile_img = SimpleUploadedFile('profile.gif', self.valid_image_content, content_type='image/gif')
        card_img = SimpleUploadedFile('card.gif', self.valid_image_content, content_type='image/gif')

        data = {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'first_name': 'Ahmed',
            'last_name': 'Ali',
            'phone': '1234567890',
            'student_id': '20123456',
            'governorate': "Sana'a",
            'age': 20,
            'profile_image': profile_img,
            'university_card_image': card_img,
            'gender': 'M'
        }
        
        response = self.client.post(self.register_url, data, format='multipart')
        
        # Check for redirection to success page
        self.assertRedirects(response, reverse('register_success'))
        
        # Verify User Created
        user = User.objects.get(username='newstudent')
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertEqual(user.phone, '1234567890')
        
        # Verify Housing Application Created
        application = HousingApplication.objects.filter(student=user).first()
        self.assertIsNotNone(application)
        self.assertEqual(application.status, HousingApplication.Status.PENDING)
        self.assertEqual(application.name, "Ahmed Ali")

    def test_registration_validation_phone_unique(self):
        """
        PRD 3.1: Secure Sign-up: Students must provide unique phone numbers.
        """
        # Create user with phone
        User.objects.create_user(username='u1', password='p1', phone='999999', governorate="Sana'a", age=20)
        
        profile_img = SimpleUploadedFile('profile.gif', self.valid_image_content, content_type='image/gif')
        card_img = SimpleUploadedFile('card.gif', self.valid_image_content, content_type='image/gif')

        data = {
            'username': 'u2',
            'password': 'p2',
            'password_confirm': 'p2',
            'phone': '999999', # Duplicate
            'governorate': "Ibb",
            'age': 21,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'u2@example.com',
            'student_id': '20999999',
            'gender': 'F',
            'profile_image': profile_img,
            'university_card_image': card_img
        }
        response = self.client.post(self.register_url, data, format='multipart')
        self.assertEqual(response.status_code, 200) # Should stay on page
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('phone', form.errors)

    def test_login_redirection_admin(self):
        """
        PRD 3.1: Role-Based Access Control
        """
        admin = User.objects.create_superuser(username='admin', password='password', role=User.Role.ADMIN)
        self.client.login(username='admin', password='password')
        response = self.client.post(self.login_url, {'username': 'admin', 'password': 'password'})
        self.assertRedirects(response, self.admin_dashboard_url)

    def test_login_redirection_student(self):
        student = User.objects.create_user(username='student', password='password', role=User.Role.STUDENT, governorate="Sana'a", age=20)
        response = self.client.post(self.login_url, {'username': 'student', 'password': 'password'})
        self.assertRedirects(response, reverse('student_dashboard'))
    
    def test_admin_create_student_with_housing(self):
        """
        Test that creating a student requires Supervisor, Building, and Room,
        and correctly creates a StudentProfile.
        """
        self.client.login(username='admin', password='password')
        supervisor = User.objects.create_user(username='sup1', password='p', role=User.Role.SUPERVISOR)
        building = Building.objects.create(name='TestBuild', address='Addr', supervisor=supervisor)
        room = Room.objects.create(building=building, number='101', capacity=5, status=Room.Status.AVAILABLE)
        
        url = reverse('user_create')  # Assuming this is the URL name for user_create view
        
        # Case 1: Missing housing fields
        data_missing = {
            'username': 'newstud',
            'email': 'ns@e.com',
            'password': 'pass',
            'role': User.Role.STUDENT,
            'phone': '55555555',
            'first_name': 'F',
            'last_name': 'L',
            'student_id': '20000001'
        }
        response = self.client.post(url, data_missing)
        form = response.context['form']
        self.assertTrue(form.errors)
        # Check for our new custom errors
        self.assertIn('supervisor', form.errors)
        self.assertIn('building', form.errors)
        
        # Case 2: Success
        data_success = data_missing.copy()
        data_success.update({
            'username': 'newstud2',
            'phone': '55555556',
            'supervisor': supervisor.id,
            'building': building.id,
            'room': room.id
        })
        response = self.client.post(url, data_success)
        
        # Check success redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify StudentProfile
        new_user = User.objects.get(username='newstud2')
        self.assertTrue(hasattr(new_user, 'student_profile'))
        self.assertEqual(new_user.student_profile.room, room)
        
        # Verify Room Occupancy Increased
        room.refresh_from_db()
        self.assertEqual(room.current_occupants, 1)
