from django.shortcuts import render
import jwt
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status,permissions
from .models import CustomUser, Gallery
from .serializers import GallerySerializer, TokenObtainPairSerializer, CustomUserSerializer
from django.conf import settings
import json
import rest_framework_simplejwt
from django.forms.models import model_to_dict
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
    #   token['email'] = user.email
        # ...

        return token
    """    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
    #    data['groups'] = self.user.groups.values_list('name', flat=True)
        return data
       """ 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
#class Obtain_token_for_user(TokenObtainPairView):
#    serializer_class = TokenObtainPairSerializer

"""
class CustomUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomUserTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user': self.user.username})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data
"""
class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        print(request.data)
        print(request.data['username'])
        print(request.data['email'])
        #print((request.data['email']).exists())
     #       if request.data['username'] or request.data['email']
        
        already_signed = CustomUser.objects.filter(username=request.data['username'],email=request.data['email']).exists()
        print(already_signed)
        if already_signed == False:
        
            serializer = CustomUserSerializer(data=request.data)
            print(CustomUser.objects.all().exists())
            print(serializer)
            print(serializer.is_valid())
            if serializer.is_valid():
                user = serializer.save()

                if user:
            #    key = settings.SECRET_KEY
            #    algorithm = settings.JWT_ALGORITHM
                    print(request)

            #    json = rest_framework_simplejwt.views.token_obtain_pair(request)
                
    #def get_tokens_for_user(user):
                    refreshToken = RefreshToken.for_user(user)
                    accessToken = refreshToken.access_token

                    decodedToken = jwt.decode(str(accessToken),settings.SECRET_KEY, algorithms=['HS256'])
                #Add payload here
                    decodedToken['username'] = user.username
                
                    encodedToken = jwt.encode(decodedToken,settings.SECRET_KEY, algorithm='HS256')
            
            
            
            
            
            
            #    print("UUUUUUSSSERRRRRR", user, user.username, user.email)
            #    print(refresh)
        #        json =  {
        #            'refresh': str(refresh),
        #            'access': str(refresh.access_token),#I'm adding the user data in response and not encoding it in jwt
        #            'username':user.username
        #        }
                    print(encodedToken)
                    user_info = {'refresh': str(refreshToken), 'access': encodedToken}
                
    #            token = jwt.encode(
    #                {
    #                    'iss': 'me',
    #                    'id': user.id,
    #                    'exp': datetime.utcnow() + timedelta(days=14)
    #                }, key, algorithm=algorithm).decode('utf-8')

    #            json = serializer.data
                
                    return Response(user_info, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"username": "User already exists"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Create your views here.
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def home(request):
    if request.method == "POST":
        #print(request.data)
        name = request.POST['name']
        print(name)
        #  name=name.strip('\"')
        image = request.FILES['image']
        image_size = request.POST['size']

        print(image_size)
        image_size = int(image_size)
        if image_size >= 1_000_000:
           image_size =  round(image_size/1_000_000, 1)

        elif image_size >= 1000:
           image_size = round(image_size/1000, 1)
        print(image_size)
        
        

        user= request.user
        print(image)
        # data={'name'}
        #  image=image.strip('\"')
        #  print(name, type(name))
        #  print(image, type(image))
        gallery = GallerySerializer(data={"name": name, "image": image, "image_size": image_size, "user": user.pk})
        #  print(request.data)
        print(gallery)
        # data = json.dumps(request.data)
        #   data={
        #    'name':name, 'image':image
        # }
        #gallery = Gallery(name=name, image=image)
        # if gallery.is_valid():
        #  print("save")

        print(gallery.is_valid())
        # print(gallery)
        if gallery.is_valid():
            gallery.save()

            return Response(gallery.data, status.HTTP_201_CREATED)
        return Response(gallery.errors)

        #print(gallery)
    # else:
    #    return Response(status.HTTP_400_BAD_REQUEST)

    # print(data)
    # print(type(data))

    # print(data.name)
    #context={'name':name,'image':image}
    #    serializer = GallerySerializer(data=request.data)
    # print(serializer)
    #print(request.data)
    #   if serializer.is_valid():
    #    print("saved")
    #   print(serializer.data)
    #   serializer.save()
    #  print(serializer)
    # return Response(status.HTTP_201_CREATED)

    # return Response(status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def gallery(request):
    if request.method == 'GET':
        user = request.user
#        all_data = Gallery.objects.all()
        all_data = Gallery.objects.filter(user=user.pk)
        gallery=GallerySerializer(all_data,many=True)

    #    serializer = GallerySerializer(data,s
    #                                   context={'request': request},
    #                                  many=True)
    #   return Response(serializer.data)
#        print(settings.MEDIA_ROOT)
 #       print(settings.MEDIA_URL)
  #      print(settings.BASE_DIR)

        return Response(gallery.data)
    if request.method == "DELETE":
        image_id = request.data
        print(image_id)
        user = request.user
#        all_data = Gallery.objects.all()
        image_del = Gallery.objects.get(user=user.pk, id = image_id).delete()
    #    print(image_to_delete.id)
    #    val = Gallery.objects.delete(image_to_delete.id)

        all_data = Gallery.objects.filter(user=user.pk)
        gallery=GallerySerializer(all_data,many=True)
        
        return Response(gallery.data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def profile(request):
    if request.method == 'GET':
        user = request.user
        user_images = Gallery.objects.filter(user= user.pk)
        print(user_images)
        total_storage = 0
        for i in user_images:
            print(i.image_size)
            total_storage += i.image_size 
        print(total_storage)
#        if total_storage >= 1_000_000:
 #           total_storage =  round(total_storage/1_000_000, 1)

  #          return Response(f"{total_storage}MB")
        if total_storage < 1000:
            total_storage =  round(total_storage, 1)

            return Response(f"{total_storage}KB")
   
   
   
        elif total_storage >= 1000:
            total_storage = round(total_storage/1000, 1)
        
            return Response(f"{total_storage}MB")
        
        


