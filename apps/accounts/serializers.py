from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode






class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','password','confirm_password','email']
    

        extra_kwargs = {
            'password':{'write_only',True}
        }

    def validate_password(self, value):
        
        if len(value) < 8 :
            raise serializers.ValidationError('Password must be 8 numbers at least')
        return value
    
    def validate(self, data):

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Password must be like confirm password')
        return data
    
        

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user 





class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token  = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token
    


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        if not User.objects.filter(value).exists():
            raise serializers.ValidationError('Not exit')
        return value
    


class ConfirmPassword(serializers.Serializer):

    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length = 8)


    def validate(self, attrs):

        try:
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.filter(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('This link invalid or user not exit')
        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('This link invalid or had been used')
        
        attrs['user']  =user
        return attrs
    

    def save(self, **kwargs):
        user = self.validated_data['user']
        password = self.validated_data['new_password']

        user.set_password(password)
        user.save()
        return user
        
         