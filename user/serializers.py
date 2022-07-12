from rest_framework import serializers
from .models import User, UserFollowing, PetProfile, UserProfile

EMAIL = ("@naver.com", "@gmail.com", "@kakao.com")

class PetProfileSerializer(serializers.ModelSerializer):

    pet_owner = serializers.SerializerMethodField()

    def get_pet_owner(self, obj):
        return obj.user.username

    class Meta:
        model = PetProfile
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):


    gender = serializers.SerializerMethodField()
    def get_gender(self,obj):
        return obj.userprofile.gender
    
    birthday = serializers.SerializerMethodField()
    def get_birthday(self,obj):
        return obj.userprofile.birthday

    show_profile = serializers.SerializerMethodField()
    def get_show_profile(self,obj):
         return obj.userprofile.is_active
    


    # def validate(self, data):

    #     if not data.get("email", "").endswith(EMAIL):
    #         raise serializers.ValidationError(
    #             detail={"error": "네이버, 구글, 카카오 이메일만 가입할 수 있습니다."}
    #         )
    #     if not len(data.get("password", "")) >= 6:
    #         raise serializers.ValidationError(
    #             detail={"error": "password의 길이는 6자리 이상이어야 합니다."}
    #         )


    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'created_at', 'updated_at','latitude', 'longitude', 'gender', 'birthday', 'show_profile']

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'error_messages': {'required': '이메일을 입력해주세요', 'invalid': '알맞은 형식의 이메일을 입력해주세요'},
                'required': False
            },
        }
