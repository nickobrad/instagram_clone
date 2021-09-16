from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image, Profile, Comment 
from django.contrib.auth import get_user_model

# Create your tests here.
class ProfileTestCase(TestCase):

    # Set up method
    def setUp(self):
        self.new_user = User(id = 1, first_name = 'James', last_name = 'Bond', username = 'jamie', email = 'jamesbond@gmail.com')
        self.new_profile = Profile(id = 1, user = self.new_user, bio = 'Hi, I am new')

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    # Testing Save method
    def test_save_method(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile) > 0)

    def test_delete_method(self):
        profile = self.new_profile
        profile.save_profile()
        profile.delete_profile()        
        self.assertTrue(len(Profile.objects.all()) == 0)

    def test_update_method(self):
        self.new_profile.save()
        profile_id = Profile.objects.last().id
        Profile.update_profile(profile_id, 'Testing2')
        new = Profile.objects.get(id = profile_id)
        self.assertEqual(new.bio, 'Testing2')

    def test_search_by_username(self):
        self.new_user.save()
        profile = Profile.search_by_username('jamie')
        self.assertTrue(len(profile) == 1)

class ImageTestClass(TestCase):

    # Creating a new editor and saving it
    def setUp(self):
        self.new_user = User(id =1, first_name = 'James', last_name = 'Bond', username = 'jamie', email = 'jamesbond@gmail.com')
        self.new_profile = Profile(id = 1, user = self.new_user, bio = 'Hi, I am new', profile_photo = 'save.jpg')
        self.new_image = Image(id = 1, image_name = 'Test Image', image_caption = 'This is a random test Post', posted_by = self.new_profile)
        self.new_comment = Comment(id = 1, post = self.new_image, posted_by = self.new_profile, body = 'Good')

    def tearDown(self):
        Comment.objects.all().delete()
        Image.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
    
    def test_instance(self):
        self.assertTrue(isinstance(self.new_image, Image))

    def test_save_image(self):
        self.new_image.save_image()
        pictures = Image.objects.all()
        self.assertTrue(len(pictures) > 0)

    def test_delete_image(self):
        picture = self.new_image
        picture.save()
        picture.delete_image()
        self.assertTrue(len(Image.objects.all()) == 0)

    def test_update_method(self):
        self.new_image.save()
        image_id = Image.objects.last().id
        Image.update_image_name(image_id, 'Testing2')
        new = Image.objects.get(id = image_id)
        self.assertEqual(new.image_name, 'Testing2')

class CommentTestCase(TestCase):

    def setUp(self):
        self.new_user = User(id = 1, first_name = 'James', last_name = 'Bond', username = 'jamie', email = 'jamesbond@gmail.com')
        self.new_profile = Profile(id = 1, user = self.new_user, bio = 'Hi, I am new')
        self.new_image = Image(id = 1, image_name = 'Test Image', image_caption = 'This is a random test Post', posted_by = self.new_profile)
        self.new_comment = Comment(id = 1, post = self.new_image, posted_by = self.new_profile, body = 'Good')

    def tearDown(self):
        Comment.objects.all().delete()
        Image.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_method(self):
        self.new_comment.save_comment()
        comment = Comment.objects.all()
        self.assertTrue(len(comment) > 0)

    def test_delete_method(self):
        comment = self.new_comment
        comment.save_comment()
        comment.delete_comment()        
        self.assertTrue(len(Comment.objects.all()) == 0)

    def test_update_method(self):
        self.new_comment.save()
        comment_id = Comment.objects.last().id
        Comment.update_comment(comment_id, 'Testing2')
        new = Comment.objects.get(id = comment_id)
        self.assertEqual(new.body, 'Testing2')

    

