#Unit Tests for backend

import json
from django.test import TestCase, Client
from django.urls import reverse, resolve
from api.models import User
from .models import Vehicle, VehicleLog, Post, Comment, Reply
from . import views


class TestURLs(TestCase):
    """Tests for URLs"""

    def test_main_spa_url(self):
        url = reverse('main_spa')
        self.assertEqual(resolve(url).func, views.main_spa)

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signup_view)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login_view)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout_view)

    def test_user_api_url(self):
        url = reverse('user_api')
        self.assertEqual(resolve(url).func, views.user_api)

    def test_update_user_profile_url(self):
        url = reverse('update_user_profile')
        self.assertEqual(resolve(url).func, views.update_user_profile)

    def test_vehicle_search_url(self):
        url = reverse('vehicle_search')
        self.assertEqual(resolve(url).func, views.vehicle_search)

    def test_add_vehicle_url(self):
        url = reverse('add_vehicle')
        self.assertEqual(resolve(url).func, views.add_vehicle)

    def test_get_vehicles_url(self):
        url = reverse('get_vehicles')
        self.assertEqual(resolve(url).func, views.get_vehicles)

    def test_get_vehicle_url(self):
        url = reverse('get_vehicle', args=[1]) 
        self.assertEqual(resolve(url).func, views.get_vehicle)

    def test_remove_vehicle_url(self):
        url = reverse('remove_vehicle', args=[1])  
        self.assertEqual(resolve(url).func, views.remove_vehicle)

    def test_add_vehicle_log_url(self):
        url = reverse('add_vehicle_log', args=[1])
        self.assertEqual(resolve(url).func, views.add_vehicle_log)

    def test_get_vehicle_logs_url(self):
        url = reverse('get_vehicle_logs', args=[1])
        self.assertEqual(resolve(url).func, views.get_vehicle_logs)

    def test_delete_vehicle_log_url(self):
        url = reverse('delete_vehicle_log', args=[1]) 
        self.assertEqual(resolve(url).func, views.delete_vehicle_log)

    def test_add_post_url(self):
        url = reverse('add_post')
        self.assertEqual(resolve(url).func, views.add_post)

    def test_get_posts_url(self):
        url = reverse('get_posts')
        self.assertEqual(resolve(url).func, views.get_posts)

    def test_get_post_url(self):
        url = reverse('get_post', args=[1]) 
        self.assertEqual(resolve(url).func, views.get_post)

    def test_delete_post_url(self):
        url = reverse('delete_post', args=[1])  
        self.assertEqual(resolve(url).func, views.delete_post)

    def test_add_comment_url(self):
        url = reverse('add_comment', args=[1]) 
        self.assertEqual(resolve(url).func, views.add_comment)

    def test_get_comments_url(self):
        url = reverse('get_comments', args=[1])  
        self.assertEqual(resolve(url).func, views.get_comments)

    def test_delete_comment_url(self):
        url = reverse('delete_comment', args=[1])  
        self.assertEqual(resolve(url).func, views.delete_comment)

    def test_add_reply_url(self):
        url = reverse('add_reply', args=[1])
        self.assertEqual(resolve(url).func, views.add_reply)

    def test_get_replies_url(self):
        url = reverse('get_replies', args=[1])
        self.assertEqual(resolve(url).func, views.get_replies)

    def test_delete_reply_url(self):
        url = reverse('delete_reply', args=[1])
        self.assertEqual(resolve(url).func, views.delete_reply)

    def test_send_email_url(self):
        url = reverse('send_email')
        self.assertEqual(resolve(url).func, views.send_email)

    
class testViews(TestCase):
    """Tests for views functions"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_main_spa_view(self):
        response = self.client.get(reverse('main_spa'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_add_vehicle_view(self):
        self.client.force_login(self.user)
        url = reverse('add_vehicle')
        data = {
            'registration_number': 'ABC123',
            'make': 'Toyota',
            'colour': 'Blue',
            'year_of_manufacture': 2020,
            'fuel_type': 'Petrol',
            'engine_capacity': 2000,
            'tax_status': 'Paid',
            'tax_due_date': '2024-04-30',
            'mot_status': 'Valid',
            'mot_expiry_date': '2024-10-30'
        }
        vehicles = Vehicle.objects.all()
        print("Number of Vehicles before POST:", vehicles.count())
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        vehicles = Vehicle.objects.all()
        print("Number of Vehicles after POST:", vehicles.count())

    def test_get_vehicles_view(self):
        self.client.force_login(self.user)
        url = reverse('get_vehicles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_posts_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_posts'))
        self.assertEqual(response.status_code, 200)

    def test_add_post_view(self):
        self.client.force_login(self.user)
        url = reverse('add_post')
        data = {
            'title': 'Test Post',
            'description': 'This is a test post.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201) 

    # def test_add_comment_view(self):
    #     self.client.force_login(self.user)
    #     post = Post.objects.create(title='Test Post', description='This is a test post.', user_id=self.user)
    #     response = self.client.get(reverse('add_comment', args=[post.id]))
    #     self.assertEqual(response.status_code, 200)

    def test_send_email_view(self):
        response = self.client.get(reverse('send_email'))
        self.assertEqual(response.status_code, 302)
