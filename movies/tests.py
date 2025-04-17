from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from .models import Movie

User = get_user_model()


class MovieModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        self.movie_data = {
            'user': self.user,
            'title': 'Test Movie',
            'rate': 8,
            'image_url': 'https://example.com/movie.jpg',
            'description': 'A test movie description'
        }

    def test_create_movie(self):
        movie = Movie.objects.create(**self.movie_data)
        self.assertEqual(movie.title, 'Test Movie')
        self.assertEqual(movie.rate, 8)
        self.assertEqual(movie.user, self.user)

    def test_string_representation(self):
        movie = Movie.objects.create(**self.movie_data)
        expected_str = f"Test Movie - {self.user.username}"
        self.assertEqual(str(movie), expected_str)

    def test_optional_fields_can_be_null(self):
        data = self.movie_data.copy()
        data['image_url'] = None
        data['description'] = None

        movie = Movie.objects.create(**data)
        self.assertIsNone(movie.image_url)
        self.assertIsNone(movie.description)

    def test_rate_validation_not_negative_rate(self):
        data = self.movie_data.copy()
        data['rate'] = -1

        with self.assertRaises(IntegrityError):
            Movie.objects.create(**data)

    def test_created_and_updated_timestamps(self):
        movie = Movie.objects.create(**self.movie_data)
        self.assertIsNotNone(movie.created_at)
        self.assertIsNotNone(movie.updated_at)