from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import *
import json
class ClientTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('testUser')
        user.save()
        self.test_user = user 

        user2 = User.objects.create(username='testuser2')
        user2.set_password('testUser2')
        user2.save()
        self.test_user2 = user2

    def test_Client(self):
        # Unauthenticated users can only access the login and register view.
        client = Client()
        # Redirect to login page
        response = client.get(reverse('index'))
        self.assertEqual(response.url, '/login?next=/')
        
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_Client1(self):        
        client = Client()
        # Login the client
        logged_in = client.login(username = 'testuser', password = 'testUser')
        self.assertTrue(logged_in)
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # No posts exist yet.
        self.assertContains(response, 'No posts to show')
        # No follows have been made
        response = client.get(reverse('follow_view'))
        self.assertContains(response, 'You are not following anyone.')
        self.assertContains(response, 'No one is following you.')
    
        response = client.get(reverse('logout'))
        # Make sure the user has actually logged out.
        self.test_Client()

    def test_Client2(self):
        # Creating a post        
        client = Client()
        logged_in = client.login(username = 'testuser', password = 'testUser')
        self.assertTrue(logged_in)
        response = client.post(reverse('post'),  json.dumps({'types':'post', 'body':'First post'}),content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content)['message'], 'Post was made successfully.')

        first_post_id = json.loads(response.content)['id']
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['likes'], 0)

        client2 = Client()
        logged_in = client2.login(username = 'testuser2', password = 'testUser2')
        self.assertTrue(logged_in)
        # New user likes the post
        response = client2.post(reverse('post'),  json.dumps({'types':'like', 'post':first_post_id }),content_type="application/json")
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['likes'], 1)

        # New user comments on the post
        response = client2.post(f'/comment/{first_post_id}', {'comment':'First comment on first post!'})
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['comments'], 1)
        self.assertEqual(post['likes'], 1)
        self.assertEqual(len(post['followers']), 0)

        #New user follows the first_user
        response = client2.post(reverse('follow_view'), {'user_id':self.test_user.id})
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['comments'], 1)
        self.assertEqual(post['likes'], 1)
        self.assertEqual(len(post['followers']), 1)

        # Can't like a post twice
        response = client2.post(reverse('post'),  json.dumps({'types':'like', 'post':first_post_id }),content_type="application/json")
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['likes'], 1)
        self.assertEqual(response.status_code,400)

        # Delete the like
        response = client2.delete(reverse('post'),  json.dumps({'post':first_post_id }),content_type="application/json")
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['likes'], 0)
        self.assertEqual(response.status_code,201)

        # Can't delete a non existed like
        response = client2.delete(reverse('post'),  json.dumps({'post':first_post_id }),content_type="application/json")
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['likes'], 0)
        self.assertEqual(json.loads(response.content)['message'], "Like doesn't exist to delete it.")
        self.assertEqual(response.status_code,400)

        # testUser2 can't edit testUser's post
        response = client2.post(f'/edit_post/{first_post_id}', {'post_body': 'Edited first post.'})
        self.assertContains(response, 'Post: First post')
        # but testUser can!
        response = client.post(f'/edit_post/{first_post_id}', {'post_body': 'Edited first post.'})
        self.assertContains(response, 'Post: Edited first post.')
        # Editing post body doesn't change comments/likes/followers
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['comments'], 1)
        self.assertEqual(post['likes'], 0)
        self.assertEqual(len(post['followers']), 1)

        comment = Comment.objects.get(user= self.test_user2)
        comment_id = comment.id
        comment_comm = comment.comment
        # testUser can't delete testUser2's post
        response = client.post(f'/del_comment/{comment_id}',  json.dumps({'post':first_post_id }),content_type="application/json")
        self.assertContains(response, comment_comm)
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['comments'], 1)
        # but testUser2 can
        response = client2.post(f'/del_comment/{comment_id}',  json.dumps({'post':first_post_id }),content_type="application/json")
        self.assertNotContains(response, comment_comm)
        post = Post.objects.get(id = first_post_id).serialize()
        self.assertEqual(post['comments'], 0)