import unittest
from app.models import User

class UserModelTest(unittest.TestCase):
    """
      Test User class to test behaviour of User model
    """
    def setUp(self):
        self.new_user = User(id=1,username='triplek',email='triplek901@gmail.com',image_file="default.png",date_joined="2021-08-23", password = 'kelvin')
    
    def test_instance(self):
        self.assertTrue(isinstance(self.new_user,User))


