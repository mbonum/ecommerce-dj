from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser('test@clavem.co', 'testpswd', 'testname')
        self.assertEqual(super_user.email, 'test@clavem.co')
        self.assertEqual(super_user.password, 'testpswd')
        self.assertEqual(super_user.email, 'test@clavem.co')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'test@clavem.co')# test def __str__(self)
        # Argon test error
        # with self.assertRaises(ValueError):
        #     db.objects.create_superuser(email='test@clavem.co', password='testpswd', first_name='testname', is_superuser=False)

        # with self.assertRaises(ValueError):
        #     db.objects.create_superuser(email='test@clavem.co', password='testpswd', first_name='testname', is_staff=False)

        # with self.assertRaises(ValueError):
        #     db.objects.create_superuser(email='', password='testpswd', first_name='testname', is_superuser=False)

    def test_new_user(self):
        db = get_user_model()
        super_user = db.objects.create_user('test@clavem.co', 'testpswd', 'testname')
        self.assertEqual(super_user.email, 'test@clavem.co')
        self.assertFalse(super_user.is_superuser)
        self.assertFalse(super_user.is_staff)
        self.assertFalse(super_user.is_active)

        # with self.assertRaises(ValueError):
        #     db.objects.create_user(email='', password='testpswd', first_name='testname')

        # with self.assertRaises(ValueError):
        #     db.objects.create_user(email='test@clavem.co', password='testpswd', first_name='testname', is_staff=False)
