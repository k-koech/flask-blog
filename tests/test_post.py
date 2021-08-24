import unittest
from app.models import Post,User

class PostModelTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Post class
    '''
    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_user = User(id=1,username='triplek',email='triplek901@gmail.com',image_file="default.png",date_joined="2021-08-23", password = 'kelvin')
        self.new_post = Post(id=1,comment='Waaah!! this one killed me',user_id=self.new_user.id,date_posted='2021-08-20 14:58:31.689649')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))

