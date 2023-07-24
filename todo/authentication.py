import requests

from django.contrib.auth.models import User
from rest_framework import authentication

from .logger import logger
from .constant import GOOGLE_TOKEN_PARAM_ID, FACEBOOK_TOKEN_PARAM_ID, GITHUB_TOKEN_PARAM_ID


class SocialAuthAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        # Check the social token sent in the url param
        username = ""
        try:
            if request.headers.get(GOOGLE_TOKEN_PARAM_ID):
                username = self.authenticate_google(request)
            elif request.headers.get(FACEBOOK_TOKEN_PARAM_ID):
                username = self.authenticate_facebook(request)
            elif request.headers.get(GITHUB_TOKEN_PARAM_ID):
                username = self.authenticate_github(request)
            else:
                return None
        except Exception as e:
            logger.info(f"Failed to authenticate request {request}, {e}")
            return None

        if username:
            user = User.objects.update_or_create(username=username)
            return user
        else:
            return None

    def authenticate_google(self, request):

        token = request.headers.get(GOOGLE_TOKEN_PARAM_ID)
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        response = requests.get(url)
        if response.ok:
            return response.json().get("email")
        else:
            logger.error(f"Failed to validate google token {token}, {response.reason}")

    def authenticate_facebook(self, request):

        token = request.headers.get(FACEBOOK_TOKEN_PARAM_ID)
        url = f"https://graph.facebook.com/me?access_token={token}"
        response = requests.get(url)
        if response.ok:
            return response.json().get("email") or response.json().get("name")  # name won't be unique, not a good idea
        else:
            logger.error(f"Failed to validate facebook token {token}, {response.reason}")

    def authenticate_github(self, request):

        token = request.headers.get(GITHUB_TOKEN_PARAM_ID)
        url = f"https://api.github.com/user"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if response.ok:
            return response.json().get("login")  # name won't be unique, not a good idea
        else:
            logger.error(f"Failed to validate github token {token}, {response.reason}")
