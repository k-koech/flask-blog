import unittest
from app.models import Quote

class QuoteTest(unittest.TestCase):
    '''
      Test Class to test the behaviour of the Quote class
    '''
    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_quote = Quote(id = 1,author="Kelvin Koech",quote='Work hard and you will achieve', permalink='https://www.bbc.com/pidgin/world-58276094')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote,Quote))



