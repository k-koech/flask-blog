from app.models import User,Comments,Post
from app import db
import unittest


class CommentModelTest(unittest.TestCase):
        """
         Test comment class to test behaviour of comment model
        """
        def setUp(self):
                self.new_user = User(id=1,username='triplek',email='triplek901@gmail.com',image_file="default.png",date_joined="2021-08-23", password = 'kelvin')
                self.new_post = Post(id=1,title='BBI suddenly stopped', content="BBI Court ruling today: Judgement reject Kenyatta Building Bridges Initiative to change Kenya constitution",
                                user_id=self.new_user.id, date_posted='2021-08-20 14:58:31')
                self.new_comment = Comments(id=1,comment='Waaah!! this one killed me',post_id=self.new_post.id, user_id=self.new_user.id,date_posted='2021-08-20 14:58:31')
        
        def test_instance(self):
               self.assertTrue(isinstance(self.new_comment,Comments))

