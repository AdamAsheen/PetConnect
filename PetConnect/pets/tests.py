# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .forms import *
import json

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.category = Category.objects.create(category_name='Test Category', category_description='Test Description')
        self.post = Post.objects.create(user=self.user_profile, title='Test Post', category=self.category, caption='Test Caption')
        self.pet = Pet.objects.create(owner=self.user_profile, name='Fido', breed='Dog', age=3, description='Good boy')

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.pet_name, 'No Pet')

    def test_category_slug_creation(self):
        self.assertEqual(self.category.slug, 'test-category')

    def test_post_slug_creation(self):
        self.assertEqual(self.post.slug, 'test-post')

    def test_comment_creation(self):
        comment = Comment.objects.create(user=self.user_profile, post=self.post, comment_text='Test comment')
        self.assertEqual(comment.comment_text, 'Test comment')

    def test_like_creation(self):
        like = Like.objects.create(user=self.user_profile, post=self.post)
        self.assertEqual(like.post, self.post)

    def test_follow_relationship(self):
        user2 = User.objects.create_user(username='testuser2', password='testpass2')
        profile2 = UserProfile.objects.get(user=user2)
        follow = Follow.objects.create(follower=self.user_profile, followed=profile2)
        self.assertEqual(follow.follower, self.user_profile)
        self.assertEqual(follow.followed, profile2)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.category = Category.objects.create(category_name='Test Category')
        self.post = Post.objects.create(
            user=self.user_profile, 
            title='Test Post', 
            category=self.category,
            caption='Test Caption'  # Added caption to match template
        )

    def test_home_view(self):
        response = self.client.get(reverse('pets:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Caption')  # Check for caption instead of title

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass')  # Added login
        response = self.client.get(reverse('pets:profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_login_view(self):
        response = self.client.post(reverse('pets:login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)

    def test_signup_view(self):
        response = self.client.post(reverse('pets:signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_post_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('pets:create-post'), {
            'caption': 'New Post',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(caption='New Post').exists())

    def test_delete_post_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('pets:delete-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_add_like_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('pets:add-likes'),
            json.dumps({'post-id': self.post.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.likes.count(), 1)

    def test_category_detail_view(self):
        response = self.client.get(reverse('pets:category-detail', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_add_pet_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('pets:add_pet'),  # Changed to correct URL name
            {
                'name': 'Buddy',
                'breed': 'Cat',
                'age': 2,
                'description': 'Fluffy cat'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pet.objects.filter(name='Buddy').exists())

class FormTests(TestCase):
    def test_user_profile_form(self):
        form_data = {'pet_name': 'Max', 'bio': 'Test bio'}
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_pet_form(self):
        form_data = {
            'name': 'Buddy',
            'breed': 'Dog',
            'age': 3,
            'description': 'Good dog'
        }
        form = PetForm(data=form_data)
        self.assertTrue(form.is_valid())

class AuthenticationTests(TestCase):
    def test_edit_profile_authentication(self):
        response = self.client.get(reverse('pets:edit_profile'))
        self.assertEqual(response.status_code, 302)

    def test_create_post_authentication(self):
        response = self.client.get(reverse('pets:create-post'))
        self.assertEqual(response.status_code, 302)

class ChatTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.chat_room = ChatRoom.objects.create(chat_name='test-room')
        self.chat_room.users.add(self.user)

    def test_chat_index_view(self):
        response = self.client.get(reverse('pets:chat'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test-room')

    def test_chat_room_view(self):
        response = self.client.get(reverse('pets:room', args=['test-room']))
        self.assertEqual(response.status_code, 200)

    def test_create_chat_view(self):
        response = self.client.post(
            reverse('pets:create-chat'),
            json.dumps({'chat_name': 'new-room'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ChatRoom.objects.filter(chat_name='new-room').exists())

class FollowTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.profile1 = UserProfile.objects.get(user=self.user1)
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.profile2 = UserProfile.objects.get(user=self.user2)

    def test_follow_unfollow(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.post(
            reverse('pets:follower'),
            json.dumps({'username': 'user2'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Follow.objects.filter(follower=self.profile1, followed=self.profile2).exists())

        # Unfollow
        response = self.client.post(
            reverse('pets:follower'),
            json.dumps({'username': 'user2'}),
            content_type='application/json'
        )
        self.assertFalse(Follow.objects.filter(follower=self.profile1, followed=self.profile2).exists())

class SignalTests(TestCase):
    def test_user_profile_creation_signal(self):
        user = User.objects.create_user(username='signaluser', password='testpass')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

class URLTests(TestCase):
    def test_url_resolution(self):
        # Updated to match your actual URL patterns
        self.assertEqual(reverse('pets:home'), '/pets/home/')
        self.assertEqual(reverse('pets:profile', args=['testuser']), '/pets/profile/testuser/')
        self.assertEqual(reverse('pets:category-detail', args=['test-category']), '/pets/categories/test-category/')