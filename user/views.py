from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers_jwt import TokenObtainPairSerializer
from .serializers import UserProfileSerializer, UserSerializer, PetProfileSerializer

from .models import User, UserFollowing, PetProfile

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


# 회원가입
class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):         
        request.user
        user_serializer=UserSerializer(data=request.data)
        
        print("*********************")
        print(user_serializer)
        print(user_serializer.is_valid())

        if user_serializer.is_valid() :
            user_serializer.save()
            request.data['username']=User.objects.get(username = request.data['username'])
            # request.data['username_id']=User.objects.get(username = request.data['username']).id
            user_profile_serializer=UserProfileSerializer(data=request.data)
            print("*********************")
            print(user_profile_serializer)
            print(user_profile_serializer.is_valid())
            if user_profile_serializer.is_valid():
                user_profile_serializer.save()
            
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        # if user_serializer.is_valid():
        # #     user_serializer.save()
        # return Response(user_serializer.data, status=status.HTTP_200_OK)
            
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request. user:
            user_serializer = UserSerializer(request.user).data
            user_serializer['followers'] = UserFollowing.objects.filter(following_user_id=request.user).count() # 나를 팔로우 하는 사람 수
            user_serializer['followings'] = UserFollowing.objects.filter(user_id=request.user).count() # 내가 팔로우 하는 사람 수
            return Response(user_serializer, status=status.HTTP_200_OK)
        return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

# 로그인 기능
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# 수정
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def put(self, request, obj_id):
        user = User.objects.get(id=obj_id)
        if request.user != user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        user_serializer = UserSerializer(user, request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 팔로우/언팔로우
class UserFollowingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self,request):
        following_user=User.objects.get(username=request.data['username'])
        new_follow, created = UserFollowing.objects.get_or_create(user_id=request.user, following_user_id= following_user)
        if created:
            new_follow.save()
            return Response({"message": "팔로우 성공!"}, status=status.HTTP_200_OK)
        new_follow.delete()
        return Response({"message":"언.팔.로.우"}, status=status.HTTP_200_OK)

class PetView(APIView):
    authentication_classes=[JWTAuthentication]

    def get(self, request):
        user = request.user
        pets = PetProfile.objects.filter(user=user)
        serializer = PetProfileSerializer(pets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        print(request.data)
        serializer=PetProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        pet = PetProfile.objects.get(pk=pk)
        serializer = PetProfileSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pet = PetProfile.objects.get(pk=pk)
        pet.delete()
        return Response({"massege" : "삭제 성공"},status=status.HTTP_200_OK)
