from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Participation, Profile

ROOT_URL = 'accounts'


class AccountTests(TestCase):
    def setUp(self):
        a, b, c = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'abc')
        Participation.objects.create(user=a, site=Site.objects.first())
        Participation.objects.create(user=c, site=Site.objects.first(), orga=True)

    def test_models(self):
        self.assertEqual(Profile.objects.count(), 3)
        self.client.login(username='c', password='c')
        for model in [Profile, Participation]:
            item = model.objects.first()
            self.assertEqual(self.client.get(item.full_link()).status_code, 200)
            self.assertTrue(str(item))

    def test_views(self):
        # User b wants to update its username, email and biography
        user = User.objects.get(username='b')
        self.assertEqual(user.email, 'b@example.org')
        self.assertEqual(user.profile.biography, '')

        self.client.login(username='b', password='b')

        # He tries with an invalid address
        self.client.post(reverse('profile'), {'email': 'bnewdomain.com', 'username': 'z', 'biography': 'tester'})
        self.assertEqual(User.objects.filter(username='z').count(), 0)

        self.client.post(reverse('profile'), {'email': 'b@newdomain.com', 'username': 'z', 'biography': 'tester'})

        user = User.objects.get(username='z')
        self.assertEqual(user.email, 'b@newdomain.com')
        self.assertEqual(user.profile.biography, 'tester')
        self.client.logout()

    def test_participant_views(self):
        self.client.login(username='b', password='b')
        self.assertEqual(self.client.get(reverse('list-participant')).status_code, 302)
        b = User.objects.get(username='b')
        b.is_superuser = True
        b.save()
        self.assertEqual(self.client.get(reverse('list-participant')).status_code, 200)
