from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.core.files import File
from urllib.request import urlretrieve
from .models import User, Token
from django.utils.crypto import get_random_string




def send_email(subject, email_from, html_alternative, text_alternative):
    msg = EmailMultiAlternatives(
        subject, text_alternative, settings.EMAIL_FROM, [email_from])
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)


async def create_file_from_image(url):
    return File(open(url, 'rb'))



def generate_otp():
            try:
                token = get_random_string(6, '0123456789')
            except Exception as e:
                generate_otp()
            return token
         
def gen_send_otp(email):
    from .tasks import send_otp_email_message_template
    
    otp_lifespan= settings.OTP_LIFESPAN
    current_otp = generate_otp()
    otp_data = {'message': f"Your code is: {current_otp}. It expires in {round(otp_lifespan/3600)} hour(s)"}
    send_otp_email_message_template.delay(otp_data)
    user_obj = User.objects.create_user(email=email, password=get_random_string(6))
    Token.objects.create(user=user_obj, token=current_otp, token_type="ACCOUNT_VERIFICATION")
    return current_otp