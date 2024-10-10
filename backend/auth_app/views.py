# auth_app/views.py

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
frontend_url = 'http://127.0.0.1:4321';
class OAuthLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, provider):
        social_auth = settings.SOCIAL_AUTH.get(provider)
        if not social_auth:
            return Response({'error': 'Invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

        if provider == 'google':
            auth_url = (
                'https://accounts.google.com/o/oauth2/v2/auth'
                '?response_type=code'
                f'&client_id={social_auth["client_id"]}'
                f'&redirect_uri={social_auth["redirect_uri"]}'
                '&scope=openid%20email%20profile'
                '&access_type=offline'
            )
        elif provider == 'facebook':
            auth_url = (
                'https://www.facebook.com/v21.0/dialog/oauth'
                '?response_type=code'
                f'&client_id={social_auth["client_id"]}'
                f'&redirect_uri={social_auth["redirect_uri"]}'
                '&scope=email,public_profile'
            )
        elif provider == 'tiktok':
            auth_url = (
                'https://www.tiktok.com/v2/auth/authorize/'
                '?response_type=code'
                f'&client_key={social_auth["client_id"]}'
                f'&redirect_uri={social_auth["redirect_uri"]}'
                '&scope=user.info.basic'
            )
        else:
            return Response({'error': 'Invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'auth_url': auth_url})

class OAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, provider):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'Code not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Optionally, you can redirect to the frontend with the code
        frontend_redirect_url = f'{frontend_url}/auth/{provider}/callback?code={code}'
        return redirect(frontend_redirect_url)

class TokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        provider = request.data.get('provider')
        code = request.data.get('code')

        if not provider or not code:
            return Response({'error': 'Provider and code are required'}, status=status.HTTP_400_BAD_REQUEST)

        social_auth = settings.SOCIAL_AUTH.get(provider)
        if not social_auth:
            return Response({'error': 'Invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code for access token
        if provider == 'google':
            token_url = 'https://oauth2.googleapis.com/token'
            data = {
                'code': code,
                'client_id': social_auth['client_id'],
                'client_secret': social_auth['client_secret'],
                'redirect_uri': social_auth['redirect_uri'],
                'grant_type': 'authorization_code',
            }
            token_response = requests.post(token_url, data=data)
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            id_token = token_data.get('id_token')

            # Get user info
            user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}
            user_info_response = requests.get(user_info_url, headers=headers)
            user_info = user_info_response.json()
            email = user_info.get('email')
            name = user_info.get('name')
        elif provider == 'facebook':
            token_url = 'https://graph.facebook.com/v21.0/oauth/access_token'
            data = {
                'client_id': social_auth['client_id'],
                'redirect_uri': social_auth['redirect_uri'],
                'client_secret': social_auth['client_secret'],
                'code': code,
            }
            token_response = requests.get(token_url, params=data)
            token_data = token_response.json()
            access_token = token_data.get('access_token')

            # Get user info
            user_info_url = 'https://graph.facebook.com/me'
            params = {
                'fields': 'id,name,email',
                'access_token': access_token,
            }
            user_info_response = requests.get(user_info_url, params=params)
            user_info = user_info_response.json()
            email = user_info.get('email')
            name = user_info.get('name')
        elif provider == 'tiktok':
            token_url = 'https://open.tiktokapis.com/v2/oauth/token/'
            data = {
                'client_key': social_auth['client_id'],
                'client_secret': social_auth['client_secret'],
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': social_auth["redirect_uri"],
            }
            token_response = requests.post(token_url, data=data)
            token_data = token_response.json()
            print(token_data);
            data_info = token_data
            access_token = data_info.get('access_token')
            open_id = data_info.get('open_id')

            # Get user info
            user_info_url = 'https://open.tiktokapis.com/v2/user/info/'
            params = {
                'fields': open_id,
            }
            user_info_response = requests.get(user_info_url, params=params, headers={
                'Authorization': f'Bearer {access_token}',
                # 'Content-Type': 'application/x-www-form-urlencoded',
            })
            user_info = user_info_response.json()
            # user_data = user_info.get('data', {}).get('user', {})
            email = None  # TikTok does not provide email
            name = user_info.get('display_name', '')
        else:
            return Response({'error': 'Invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

        if not email:
            email = f'{provider}_{user_info.get("id")}@example.com'
        print(user_info)
        # Create or get user
        user, created = User.objects.get_or_create(email=email, defaults={'name': name})
        token, created = Token.objects.get_or_create(user=user)

        # Generate JWT tokens
        # refresh = RefreshToken.for_user(user)
        return Response({
            'access': token.key,
            'token': token.key,
            # 'user': user,
            # 'access': str(refresh.access_token),
        })
