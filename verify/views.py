import redis
from random import randint

from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserLoginSerializer, UserVerifySerializer, UserPostSerializer
from .permissions import IsOwnerOrReadOnly
from .models import UserPostModel
from .tasks import send_code

redis_connection = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
random_code = str(randint(100000, 999999))


class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        print(mobile)
        redis_connection.set(mobile, random_code, ex=120)
        send_code.apply_async(args=[mobile, random_code])
        return Response(status=status.HTTP_200_OK)


class UserVerification(generics.CreateAPIView):
    serializer_class = UserVerifySerializer

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        otp_code = request.data.get('otp')
        cached_otp = redis_connection.get(mobile)
        if otp_code == cached_otp:
            custom, created = User.objects.get_or_create(username=mobile)
            refresh = RefreshToken.for_user(custom)
            access_token = refresh.access_token
            response_data = {
                'token': str(access_token),
                'refresh': str(refresh),
                'created': created
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "It`s wrong"}, status=status.HTTP_404_NOT_FOUND)


class Home(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response("ok", status=status.HTTP_200_OK)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPostSerializer()

    def post(self, request, *args, **kwargs):
        serializer = UserPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        text = serializer.validated_data['text']
        if UserPostModel.objects.filter(title=title).exists():
            return Response({"error": "title is already exist"}, status=status.HTTP_409_CONFLICT)
        queryset = UserPostModel.objects.create(text=text, title=title, owner=request.user)
        response_data = {
            "id": queryset.id,
            "user": queryset.owner.username,
            "title": queryset.title,
            "slug": queryset.slug,
            "rext": queryset.text,
            "created": queryset.created,
            "modified": queryset.modified,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PostRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug_id):
        try:
            queryset = UserPostModel.objects.get(slug=slug_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response_data = {
            "id": queryset.id,
            "user": queryset.owner.username,
            "title": queryset.title,
            "slug": queryset.slug,
            "rext": queryset.text,
            "created": queryset.created,
            "modified": queryset.modified,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PostUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def put(self, request, slug_id):
        queryset = UserPostModel.objects.get(slug=slug_id)
        self.check_object_permissions(request, queryset)
        serializer = UserPostSerializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if UserPostModel.objects.filter(title=serializer.validated_data['title']).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def delete(self, request, slug_id):
        queryset = UserPostModel.objects.get(slug=slug_id)
        queryset.delete()
        return Response({'message': 'delete'}, status=status.HTTP_200_OK)