from django.test import TestCase
from .models import Post

class ModelTestCase(TestCase):
    def setUp(self):
        self.post_Hello_name = "Ekaterina"
        self.blog_post = Post(name=self.post_Hello_name)

    def test_model_can_create_task(self):
        old_count = Post.objects.count()
        self.post.save()
        new_count = Post.objects.count()
        self.assertNotEqual(old_count, new_count)


from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_date = {
            'Hello_name': 'Ekaterina',
            'Task': 'Сдать лабораторную работу',
            'Phone_number': '89999999999'
        }
        self.response = self.client.post(reverse('create'), self.post_data, format='json')

    def test_api_can_create_a_post(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)