from .models import Gallery
from .serializers import GallerySerializer
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import filter_users_by_email, user_pk_to_url_str, user_username
from allauth.account.forms import default_token_generator
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.utils import build_absolute_uri
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer
from picspace import serializers


#Verify Email URL view
class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f'https://picspacevault.netlify.app/account-confirm-email/{emailconfirmation.key}'


#Password Reset form View
class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):

    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get(
            'token_generator', default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            path = f"https://picspacevault.netlify.app/reset-password-confirm/{user_pk_to_url_str(user)}/{temp_key}/"

            # Values which are passed to password_reset_key_message.txt
            url = build_absolute_uri(request, path)
            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
                "path": path,
            }

            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email', email, context
            )

        return self.cleaned_data['email']


#Password Reset Serializer
class MyPasswordResetSerializer(PasswordResetSerializer):

    def validate_email(self, value):
        # use the custom reset form
        self.reset_form = CustomAllAuthPasswordResetForm(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value


#Google Authorization Code Grant View
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'https://picspacevault.netlify.app'
    client_class = OAuth2Client


#Facebook Login View
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


#View for retrieving Token based on User info
@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):

    email = request.data.get('email')
    user = User.objects.get(email=email)
    token = Token.objects.get(user=user)
    return Response({'key': str(token)}, status.HTTP_200_OK)


#Home page view
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def home(request):
    if request.method == "POST":
        image_info = request.data.get('image_url')
        data = {
            'user': request.user.pk,
            'name': image_info['name'],
            'image_uuid': image_info['uuid'],
            'image_size': image_info['size']
        }

        gallery = GallerySerializer(data=data)
        if gallery.is_valid():
            gallery.save()
            return Response(gallery.data, status.HTTP_200_OK)
        return Response(gallery.errors)


#Gallery View
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@api_view(['GET', 'PUT', 'DELETE'])
def gallery(request):
    if request.method == 'GET':
        user = request.user
        all_data = Gallery.objects.filter(user=user.pk)
        gallery = GallerySerializer(all_data, many=True)
        return Response(gallery.data)
    if request.method == "DELETE":
        image_id = request.data

        user = request.user
        image_del = Gallery.objects.get(user=user.pk, id=image_id).delete()

        all_data = Gallery.objects.filter(user=user.pk)
        gallery = GallerySerializer(all_data, many=True)

        return Response(gallery.data)


#Profile View
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def profile(request):
    if request.method == 'GET':
        user = request.user

        user_images = Gallery.objects.filter(user=user.pk)

        total_storage = 0
        for i in user_images:
            total_storage += i.image_size

        #Check if email is verified or not
        email = EmailAddress.objects.get(user=user.pk, primary=True)
        verified_email = False
        if email.verified:
            verified_email = True

        #Check if user has signed in using Social apps or email-password
        provider = SocialAccount.objects.filter(user=user.pk).first()
        social_provider = True
        if provider == None:
            social_provider = False

        total_storage = niceBytes(total_storage)
        data = {
            'social_provider': social_provider,
            'storage': f'{total_storage}',
            'verified_email': verified_email
        }

        return Response(data)

#Conveerting file size units
def niceBytes(x):
    units = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    l = 0
    n = int(x) or 0
    while n >= 1024 and l < len(units)-1:
        l += 1
        n /= 1024
    return f"{n:.1f} {units[l]}"
