from django.shortcuts import render

# Create your views here.

from django.views import View
from django.conf import settings
from twilio.rest import Client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import status

import json
import pyotp
from datetime import datetime, timedelta

from icecream import ic

from .models import OTP
from account.models import User


class TwilioBaseView:
    def get_twilio_client(self):
        return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


@method_decorator(csrf_exempt, name='dispatch')
class SendOTPView(View, TwilioBaseView):
    def post(self, request, *args, **kwargs):
        try:

            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            print(phone_number)

            print(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            print(settings.TWILIO_SERVICE_ID)
            
            if not phone_number:
                return JsonResponse({'error': 'Phone number is required'}, status=400)

            client = self.get_twilio_client()
            
            try:
                print('**********Phone Verification**********')
                verification = client.verify.v2.services(settings.TWILIO_SERVICE_ID).verifications.create(
                    to=phone_number,
                    channel='sms'
                )
                print(verification.status)
                return JsonResponse({'status': 'OTP sent'})
            except Exception as e:
                print(f"Error creating verification: {e}")
                return JsonResponse({'error': str(e)}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        


@method_decorator(csrf_exempt, name='dispatch')
class VerifyOTPView(View, TwilioBaseView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        otp_code = data.get('otp_code')
        print(phone_number,otp_code)
        if not phone_number or not otp_code:
            return JsonResponse({'error': 'Phone number and OTP code are required'}, status=400)

        client = self.get_twilio_client()

        try:
            print('Verification check')
            verification_check = client.verify.v2.services(settings.TWILIO_SERVICE_ID).verification_checks.create(
                to=phone_number,
                code=otp_code
            )
            print(verification_check)

            if verification_check.status == 'approved':
                return JsonResponse({'status': 'OTP verified'})
            else:
                return JsonResponse({'error': 'Invalid OTP'}, status=400)
        except Exception as e:
            return JsonResponse({'error': "Expire or Invalid OTP"}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class SendEmailOTPView(View, TwilioBaseView):
    # def post(self, request, *args, **kwargs):
        # try:

            # data = json.loads(request.body)
            # email = data.get('email')
            # print(email)
            
            # if not email:
            #     return JsonResponse({'error': 'Email is required'}, status=400)

            # client = self.get_twilio_client()
            
            # try:
            #     verification = client.verify.v2.services(settings.TWILIO_EMAIL_SERVICE_ID).verifications.create(
            #         to=email,
            #         channel='email'
            #     )
            #     print(verification.status)
            #     return JsonResponse({'status': 'OTP sent'})
            # except Exception as e:
            #     return JsonResponse({'error': str(e)}, status=500)


    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            receiver = [email, ]

            print('***************************************')

            user= User.objects.filter(email=email).first()
            if user:
                print('user Created: ', user)
                return JsonResponse({'error':"Email already registered!"},status=400)

            totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
            otp = totp.now()

            # Set OTP expiration time
            valid_time = timezone.now() + timedelta(seconds=300)

            # Save OTP to database
            otp_record = OTP(
                email=email,
                otp=otp,
                expires_at=valid_time
            )
            otp_record.save()

            subject = "Email Verification"
            message = f"""
                Hi, here is your OTP {otp}
                It expires in 5 minutes.
            """
            sender = settings.EMAIL_HOST_USER

            # Send email
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            return JsonResponse({'status': 'OTP sent'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        

@method_decorator(csrf_exempt, name='dispatch')
class VerifyEmailOTPView(View, TwilioBaseView):
    def post(self, request, *args, **kwargs):
        error_message = None
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            otp = data.get('otp')

            try:
                print('*******************Otp verify*******************')
                otp_record = OTP.objects.filter(email=email).order_by('-created_at').first()

                if otp_record is None:
                    return JsonResponse({'error': 'No OTP record found'}, status=400)

                if otp_record.is_expired():
                    return JsonResponse({'error': 'One time password has expired'}, status=400)
                
                print(otp_record,otp)

                if otp_record.otp == otp:
                    print('otp check')
                    otp_record.delete()  # Delete the OTP record after successful validation
                    
                    user = User.objects.create_user(email=email)
                    print('user_created: ',user)
                    user_data = {
                        'tokens':user.tokens(),
                        'user':{
                            'id':user.id,
                            'email':user.email
                        }
                    }

                    return JsonResponse({"message": "OTP validation Success", 'user_data':user_data}, status=200)
                    # return JsonResponse({"message": "OTP validation Success"})
                else:
                    error_message = 'Invalid one time password'

            except Exception as e:
                print(f"Exception: {e}")
                error_message = 'Something went wrong'

            return JsonResponse({"error": error_message})


        # data = json.loads(request.body)
        # email = data.get('email')
        # otp_code = data.get('otp_code')
        # print(email,otp_code)
        # if not email or not otp_code:
        #     return JsonResponse({'error': 'Email and OTP code are required'}, status=400)

        # client = self.get_twilio_client()

        # try:
        #     print('Verification check')
        #     verification_check = client.verify.v2.services(settings.TWILIO_EMAIL_SERVICE_ID).verification_checks.create(
        #         to=email,
        #         code=otp_code
        #     )
        #     print(verification_check)

        #     if verification_check.status == 'approved':
        #         return JsonResponse({'status': 'OTP verified'})
        #     else:
        #         return JsonResponse({'error': 'Invalid OTP'}, status=400)
        # except Exception as e:
        #     return JsonResponse({'error': "Expire or Invalid OTP"}, status=500)