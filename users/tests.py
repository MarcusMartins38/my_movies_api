from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

    def test_update_user_valid_data(self):
        data = {'username': 'newusername', 'email': 'newemail@example.com'}
        serializer = UserSerializer(instance=self.user, data=data, partial=True, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, 'newusername')
        self.assertEqual(updated_user.email, 'newemail@example.com')

    def test_change_password_valid(self):
        data = {
            'current_password': 'testpassword123',
            'new_password': 'newtestpassword123',
            'confirm_new_password': 'newtestpassword123'
        }
        serializer = UserSerializer(instance=self.user, data=data, partial=True, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertTrue(updated_user.check_password('newtestpassword123'))

    def test_change_password_incorrect_current(self):
        data = {
            'current_password': 'wrongpassword',
            'new_password': 'newtestpassword123',
            'confirm_new_password': 'newtestpassword123'
        }
        serializer = UserSerializer(instance=self.user, data=data, partial=True, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_password', serializer.errors)

    def test_change_password_mismatch(self):
        data = {
            'current_password': 'testpassword123',
            'new_password': 'newtestpassword123',
            'confirm_new_password': 'differentpassword'
        }
        serializer = UserSerializer(instance=self.user, data=data, partial=True, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password', serializer.errors)

    def test_incomplete_password_fields(self):
        data = {
            'current_password': 'testpassword123',
        }
        serializer = UserSerializer(instance=self.user, data=data, partial=True, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password', serializer.errors)


class RegisterSerializerTest(TestCase):
    def test_register_valid_data(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('StrongPass123!'))

    def test_register_password_mismatch(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'DifferentPass123!'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_register_existing_username(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='password123')

        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_register_existing_email(self):
        User.objects.create_user(username='user1', email='existing@example.com', password='password123')

        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)