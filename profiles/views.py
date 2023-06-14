from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from profiles.models import User
from profiles.serializers import UserSerializer, UserLoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return Response('Invalid username or password', status=status.HTTP_401_UNAUTHORIZED)
        request.session['user_id'] = user.id
        return Response('Logged in successfully')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
    
    # logout operations
    request.session.flush()
    return Response('Logged out successfully')

class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        response = super().post(request.data)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})
