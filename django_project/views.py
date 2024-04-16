from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer, TokensSerializer, RefreshTokenSerializer
from .serializers import RetrieveDataSerializer, ChangeDataSerializer, AccessTokenSerializer
from rest_framework import status
from .authentication import create_access_token, create_refresh_token
from .authentication import decode_access_token, decode_refresh_token
from user.models import User
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
)
@api_view(['POST'])
def register(request):

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        return Response({"id": serializer.data["id"], "email": serializer.data["email"]})
    
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@extend_schema(
        request=UserSerializer,
        responses={201: TokensSerializer},
)
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "not found"}, status = status.HTTP_404_NOT_FOUND)
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    user.refresh_token = refresh_token
    user.save()
    #token, created = Token.objects.get_or_create(user=user)    #refresh token here
    serializer = UserSerializer(instance=user)
    return Response({"access_token": access_token, "refresh_token": refresh_token})

@extend_schema(
        request=RefreshTokenSerializer,
        responses={201: AccessTokenSerializer},
)
@api_view(['POST'])
def refresh(request):
    refresh_token = request.data["refresh_token"]
    token_info = decode_refresh_token(request.data["refresh_token"])
    user = User.objects.get(id=token_info["user_id"])

    if not (refresh_token == user.refresh_token):
        return Response({"detail": "wrong token"}, status = status.HTTP_404_NOT_FOUND)
    
    new_access_token = create_access_token(token_info["user_id"])
    return Response({"access_token": new_access_token})

@extend_schema(
        request=RefreshTokenSerializer,
        responses={201: UserSerializer},
)
@api_view(['POST'])
def logout(request):
    refresh_token = request.data["refresh_token"]
    token_info = decode_refresh_token(request.data["refresh_token"])
    user = User.objects.get(id=token_info["user_id"])
    
    if not (refresh_token == user.refresh_token):
        return Response({"detail": "wrong token"}, status = status.HTTP_404_NOT_FOUND)
    

    user.refresh_token = ""
    user.save()
    return Response({"success": "User logged out.", "User": user.email})

@extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                name='access token', 
                type=str, 
                location=OpenApiParameter.HEADER,  
                description='check user access',
            ),
        ],
        responses={201: RetrieveDataSerializer},
        methods=["GET"]
)
@extend_schema(
        request=ChangeDataSerializer,
        parameters=[
            OpenApiParameter(
                name='access token', 
                type=str, 
                location=OpenApiParameter.HEADER,  
                description='check user access',
            ),
        ],
        responses={201: ChangeDataSerializer},
        methods=["PUT"]
)
@api_view(['GET', 'PUT'])
def me(request):
    header_data = request.headers["Header"].split()

    if not (len(header_data) == 3):
        return Response({"detail": "wrong header"}, status = status.HTTP_404_NOT_FOUND)
    token = header_data[2]
    token_info = decode_access_token(token)

    if request.method == "GET":
        return Response(
            {"id": token_info["user_id"],
             "username": token_info["username"],
             "email": token_info["email"],
                }
            )
    if request.method == "PUT":
        user = User.objects.get(id=token_info["user_id"])
        user.username = request.data["username"]
        user.save()
        return Response({"username": user.username})

