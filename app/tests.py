from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Galaxy, Star, Planet

class UserCreationTestCase(TestCase):
    def testCreateAstronomer(self):
        user = CustomUser.objects.create_user(
            username='testastronomer',
            email='testastronomer@example.com',
            password='testpass',
            type='astronomer'
        )
        self.assertEqual(user.type, 'astronomer')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def testCreateRegularUser(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
            type='user'
        )
        self.assertEqual(user.type, 'user')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

class AccessControlTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.astronomer = CustomUser.objects.create_user(
            username='astronomer',
            email='astro@example.com',
            password='testpass',
            type='astronomer'
        )
        self.regular_user = CustomUser.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='testpass',
            type='user'
        )
        self.creation_url = reverse('celestialBodyCreation')

    def testAstronomerCanAccessCreationPage(self):
        self.client.login(email='astro@example.com', password='testpass')
        response = self.client.get(self.creation_url)
        self.assertEqual(response.status_code, 200)

    def testRegularUserCannotAccessCreationPage(self):
        self.client.login(email='regular@example.com', password='testpass')
        response = self.client.get(self.creation_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def testUnauthenticatedUserCannotAccessCreationPage(self):
        response = self.client.get(self.creation_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

class DynamicSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.search_url = reverse('search')

        self.galaxy1 = Galaxy.objects.create(name='Andromeda',
                                           type='Spiral',
                                           distanceMly=2.5)
        self.galaxy2 = Galaxy.objects.create(name='Triangulum',
                                           type='Spiral',
                                           distanceMly=3.0)
        
        self.star1 = Star.objects.create(name='Sun',
                                       starType='G-type',
                                       temperature=5778,
                                       luminosity=1.0,
                                       galaxy=self.galaxy1)
        self.star2 = Star.objects.create(name='Proxima Centauri',
                                       starType='M-type',
                                       temperature=3042,
                                       luminosity=0.0017,
                                       galaxy=self.galaxy1)
        self.planet1 = Planet.objects.create(name='Earth',
                                           habitable=True,
                                           orbitPeriod=365.25,
                                           star=self.star1)
        self.planet2 = Planet.objects.create(name='Mars',
                                           habitable=False,
                                           orbitPeriod=687.0,
                                           star=self.star1)

    def testDynamicSearchGalaxyByName(self):
        response = self.client.get(self.search_url, {
            'type': 'galaxy',
            'name': 'Andromeda'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.galaxy1, response.context['galaxies'])
        self.assertNotIn(self.galaxy2, response.context['galaxies'])

    def testDynamicSearchStarByType(self):
        response = self.client.get(self.search_url, {
            'type': 'star',
            'star_type': 'G-type'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.star1, response.context['stars'])
        self.assertNotIn(self.star2, response.context['stars'])

    def testDynamicSearchPlanetByHabitable(self):
        response = self.client.get(self.search_url, {
            'type': 'planet',
            'habitable': 'true'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.planet1, response.context['planets'])
        self.assertNotIn(self.planet2, response.context['planets'])

    def testDynamicSearchNoTypeQuery(self):
        response = self.client.get(self.search_url, {
            'q': 'Sun'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.star1, response.context['stars'])
        self.assertNotIn(self.galaxy1, response.context['galaxies'])

    def testDynamicSearchEmptyQuery(self):
        response = self.client.get(self.search_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['results'])
