from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


class SmSRequestTestCase(APITestCase):
    def test_sms_request(self):
        response = self.client.post(
            '/api/v1/users/sms_request/',
            {'phone': '+79101010101'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sms', response.data)


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='+79101010101',
        )
        self.superuser = get_user_model().objects.create_superuser(
            phone='+78888888888',
            password='password',
        )

    def test_create(self):
        sms = self.client.post(
            '/api/v1/users/sms_request/',
            {'phone': '+79999999999'},
        ).data['sms']
        response = self.client.post(
            '/api/v1/users/',
            {'phone': '+79999999999', 'sms': sms},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth(self):
        sms = self.client.post(
            '/api/v1/users/sms_request/',
            {'phone': '+79101010101'},
        ).data['sms']
        response = self.client.post(
            '/api/v1/users/',
            {'phone': '+79101010101', 'sms': sms},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_login(self.user)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.superuser)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = self.client.get(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_login(self.user)
        response = self.client.get(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.patch(f'/api/v1/users/{self.user.id}/', {'phone': '+79999999999'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_login(self.user)
        response = self.client.patch(f'/api/v1/users/{self.user.id}/', {'phone': '+79999999999'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+79999999999')

    def test_destroy(self):
        response = self.client.delete(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_login(self.user)
        response = self.client.delete(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ActivateReferralCodeTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='+79101010101',
        )
        self.another_user = get_user_model().objects.create_user(
            phone='+79999999999',
        )

    def test_code_activation(self):
        response = self.client.post(
            '/api/v1/users/activate_code/',
            {'phone': '+79101010101', 'referral_code': 'nx5fa7'},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_login(self.user)
        response = self.client.post(
            '/api/v1/users/activate_code/',
            {'phone': self.user.phone, 'referral_code': self.another_user.referral_code.code},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            '/api/v1/users/activate_code/',
            {'phone': self.user.phone, 'referral_code': self.user.referral_code.code},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetProfileTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='+79101010101',
        )

    def test_get_profile(self):
        response = self.client.get(f'/api/v1/users/profile/?phone={self.user.phone}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_login(self.user)
        phone = self.user.phone.replace('+', '%2B')
        response = self.client.get(f'/api/v1/users/profile/?phone={phone}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], self.user.phone)
