from django.test import TestCase
from . models import *


class ModelTests(TestCase):

    def setUp(self):
          self.forms = Categoryone.objects.create()