from django.test import TestCase
from fbuser.models import Fbuser
from .models import Post
from comment.models import Comment

# Create your tests here.


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        self.user = Fbuser(
            username='testuser',
            password='testuser1',
            email='testuser@gmail.com',
            is_active=True,
            is_staff=True
        )
        self.user.save()
        self.post = Post(
            contents='test asdf',
            writer=self.user
        )
        self.post.save()
        self.post2 = Post(
            contents='test asdf',
            writer=self.user
        )
        self.post2.save()

    def test_create_comment_and_list(self):
        self.comment = []
        for _ in range(10):
            c = Comment(
                contents='comment test',
                writer=self.user,
                parent=self.post
            )
            c.save()
            self.comment.append(c)
            self.assertEqual(Post, type(c.parent))

        for _ in range(5):
            c = Comment(
                contents='comment test',
                writer=self.user,
                parent=self.post2
            )
            c.save()
            self.comment.append(c)
            self.assertEqual(Post, type(c.parent))

        for _ in range(5):
            c = Comment(
                contents='comment test',
                writer=self.user,
                parent=self.comment[0]
            )
            c.save()
            self.assertEqual(Comment, type(c.parent))

        comments = Comment.objects.filter(
            content_type__model='post').filter(object_id=self.post.id)
        self.assertEqual(10, len(comments))

        comments = Comment.objects.filter(
            content_type__model='post').filter(object_id=self.post2.id)
        self.assertEqual(5, len(comments))

        comments = Comment.objects.filter(
            content_type__model='comment').filter(object_id=self.comment[0].id)
        print(comments)
        self.assertEqual(5, len(comments))
