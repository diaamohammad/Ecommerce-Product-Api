from .views import ResetPasswordView
from .models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


   
 






def sent_email(email):

    user = User.objects.filter(email=email).first()

    if user:

        uidb64=urlsafe_base64_encode(force_bytes(user.id))
        token=default_token_generator.make_token(user)

        frontend_url = f"http://localhost:3000/reset_password/{uidb64}/{token}/"

        
    else:
       
        return  

