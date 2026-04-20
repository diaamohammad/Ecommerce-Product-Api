from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer,RegisterSerializer,ResetPasswordSerializer,ConfirmPassword
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .services import sent_email


User=get_user_model



class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    queryset = User.objects.all()

    

class CustomTokenView(TokenObtainPairView):


    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]



class ResetPasswordView(generics.GenericAPIView):

    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        sent_email(email)


        return Response({
    "message": "If this email exists, a reset link has been sent"
})



    
class ConfirmPassword(generics.GenericAPIView):

    serializer_class = ConfirmPassword
    permission_classes = [AllowAny]

    def post(self,request):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception= True)

        serializer.save()
        return Response({"message":"Password dad been changed,ypu can sign in by new password"}
                        ,status= status.HTTP_200_OK)
    


   

    