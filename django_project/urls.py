from django.urls import path
from dj_rest_auth.views import PasswordResetConfirmView
from django.contrib import admin
from django.urls import path, include, re_path
from picspace import views
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.registration.views import VerifyEmailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/verify-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/password/reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    re_path(r'^api/home', views.home),
    re_path(r'^api/gallery/$', views.gallery),
    re_path(r'^api/profile/$', views.profile),
    path('api/', include('picspace.urls'))
]
