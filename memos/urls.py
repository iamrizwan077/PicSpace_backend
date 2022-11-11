from django.urls import path,re_path
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
  path("", views.gallery, name="gallery"),
  
  path('user/create/', CustomUserCreate.as_view(), name="create_user"),
  path('token/obtain/', MyTokenObtainPairView.as_view(), name= 'token_create'),
  path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name= 'token_refresh')

]
