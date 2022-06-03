from django.shortcuts import render,HttpResponse

#imports pf signup api
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from .models import *
from datetime import datetime,timedelta,date,timezone
from django.db.models import Q
from rest_framework.response import Response
from email.mime.multipart import MIMEMultipart
from main import settings
# from rest_framework.authtoken.models import Token
from django.contrib.auth import login,authenticate,logout
from .helpers import send_otp_to_phone,send_verification_email

# Create your views here.

from django.db.models.signals import post_save
from django.dispatch import receiver

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)  # 

# token_url = "http://localhost:8000/auth/api-token-auth/"
# token_payload = {"username":credentials.username,"password":credentials.password}

@api_view(['GET','POST'])
@permission_classes(( ))
@csrf_exempt

def Signup(request):
    #if user does not verify the phone verification withon 10 minute,so user will be deleted from the db.
    CustomerModel.objects.filter(date_Join__lte=(datetime.utcnow()-timedelta(minutes = 10)),is_phone_verified=0).delete()
    dictV={}
    # data=request.GET    
    Email=request.POST.get('Email')      #get or input the data from request user from postman
    password=request.POST.get('password')
    MobileNumber=request.POST.get('MobileNumber')
    Name=request.POST.get('Name')
    DeviceType=request.POST.get('DeviceType')
    DeviceToken=request.POST.get('DeviceToken')

    InvitationCode=''
    if len(request.POST.getlist('InvitationCode'))>0:
        InvitationCode=request.POST['InvitationCode']
    Language_id=1
    if len(request.POST.getlist('Language_id'))>0:
        Language_id=request.POST['Language_id']

    # if CustomerModel.objects.filter(mobile_number=MobileNumber):
    #     dictV['msg']='phone number already exists'  
    #     return Response(dictV)     

    c=CustomerModel.objects.filter(email=Email,is_phone_verified=1,is_deleted=0) #filter the objects who email is exists in db and whoose isdeleted=false,isphoneverified is true.
    cc=CustomerModel.objects.filter(mobile_number=str(MobileNumber),is_deleted=0,is_phone_verified=1)  #filter the objects from db whoose mobile number is exists in db or not.

    #performs validation on email and phone number
    if len(c)>0 or len(cc)>0:
        if len(c)>0:
            dictV['Message']='The email already exists.'
        if len(cc)>0:
            dictV['Message']='The mobile number already exists.'
        if len(c)>0 and len(cc)>0:
            dictV['Message']='The email and mobile number already exists.'
        dictV['Response']=0
        return Response(dictV) 
    else:
        import random
        Email_otp = random.randint(1000,9999)
        user_email=request.POST.get('Email')
        email_body="otp is send to your email for verify your account"+str(Email_otp)
        # user=CustomerModel.objects.get(email=user_email)
        if user_email and email_body:
            send_verification_email(request,user_email,email_body)

        #response= client.messages.create(messaging_service_sid='MG443a218d0365b645f8dafa9b9ae27880',body=phonemsg,to='+'+str(MobileNumber)) 
        try:
            import random
            PhoneOTP = random.randint(1111,2222)
            phone_number=request.POST.get('MobileNumber')
            message="your otp is "+str(PhoneOTP)
            if phone_number and message:
                send_otp_to_phone(request,phone_number,message)
            # verification = client.verify.services(credentials.verify_service_id).verifications.create(to='+'+str(MobileNumber), channel='sms',locale='en')
        except:
           dictV['Response']=0
           dictV['Message']='Invalid mobile number.'
           return Response(dictV) 

        #len of object who has email=email present over the db is 1..therfore if object is not present so its length is 0.if 1==0 and 0==0(True)
        if len(CustomerModel.objects.filter(email=Email))==0 and len(CustomerModel.objects.filter(mobile_number=str(MobileNumber)))==0:
            c=CustomerModel.objects.create(email=Email,username=Email,name=Name,mobile_number=str(MobileNumber),device_type=DeviceType,device_token=DeviceToken,phone_otp=PhoneOTP,
                email_otp=Email_otp,language_id=Language_id,invitation_code=InvitationCode)
            c.set_password(password)    
            c.save()
            cid=c.id  #returns the customer id which is created.
        else:
            try:
                cid=CustomerModel.objects.filter(email=Email).values()[0]['id']   
            except:
                cid=CustomerModel.objects.filter(mobile_number=str(MobileNumber)).values()[0]['id']  
            CustomerModel.objects.filter(id=cid).update(name=Name,device_type=DeviceType,device_token=DeviceToken,language_id=Language_id,invitation_code=InvitationCode)    

        dictV['Response']=1
        dictV['Message']='Sent OTP to your registered mobile number.'
        dictV['UserInfo']=CustomerModel.objects.filter(id=cid).values('id')[0]  

    return Response(dictV)      



from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import filters, permissions, serializers, status, viewsets
from .serializers import *

class Login(APIView):
    """
    login user api
    """
    @swagger_auto_schema(
        operation_description="User login API",
        operation_summary="User login API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    
    @csrf_exempt
    def post(self,request):
        data=request.data
        email=data.get('email')
        password=data.get('password')

        try:
            user=CustomerModel.objects.get(email=email)
        except CustomerModel.DoesNotExist:
            return Response({'data':'User not found'})

        if user.check_password(password):
            token=RefreshToken.for_user(user)
            # print('refresh'+str(token),'access'+str(token.access_token))

            # if not Token.objects.filter(token_type="access_token", user_id=user_object.id).exists():
            #equivalent to:->
            if len(Token.objects.filter( token_type="access_token", user_id=user.id))==0:
                Token.objects.create(
                    user_id=user.id,
                    token=str(token.access_token),
                    token_type="access_token"
                )
            else:
                Token.objects.filter(user_id=user.id,token_type="access_token").update(token=str(token.access_token))
                serializer=UserSerializer(user)

                return Response(
                {
                    "data": serializer.data,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                    "code": status.HTTP_200_OK,
                    "message": "Login SuccessFully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "data": "wrong credentials",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Serializer error",
                }
            )    

class Resendotp(APIView):
    """"
    Resend Otp
    """
    @swagger_auto_schema(
        operation_description="User login API",
        operation_summary="User login API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
                # "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )

    @csrf_exempt
    def post(self,request):
        data=request.data
        phone=data.get('phone_number')
        
        if phone == '':
            return Response({'msg':'plz enter a phone number'})

        user=request.user
        print(user.id)

        user_obj=CustomerModel.objects.filter(id=user.id,is_deleted=0,is_phone_verified=1)
        print(user_obj)

        if user_obj:
            return Response({
                'data':'the customer is already verified'
            })
        else:
            import random
            PhoneOTP = random.randint(1111,2222)
            phone_number=data.get('phone_number')
            message="your otp is "+str(PhoneOTP)
            try:
                send_otp_to_phone(request,phone_number,message)
            except:
                return Response({'msg':'invalid phone_number'})

            finally:
                   c=CustomerModel.objects.filter(id=user.id,is_deleted=0,mobile_number=phone)
                   if not c:
                       return Response({'msg':'enter a registered phone_number'})
                   if c:
                       c.update(phone_otp=PhoneOTP)
                       cc=CustomerModel.objects.filter(id=user.id).values('id','phone_otp')[0]

                       return Response({
                           'msg':'otp is sent to your register mobile number',
                           'data':cc
                       })    


class PhoneOtpVerification(APIView):
    """
     Phone Otp_verification
    """
    @swagger_auto_schema(
        operation_description="User login API",
        operation_summary="User login API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "otp": openapi.Schema(type=openapi.TYPE_STRING),
                # "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @csrf_exempt
    def post(self,request):
        data=request.data
        otp=data.get('otp')
        user=request.user

        if CustomerModel.objects.filter(id=user.id,is_deleted=0,is_phone_verified=1).exists():  #when we use filter queryset--> .exists() is used .but not with get queryset
            return Response({'msg':'user is already verified'})
    
        try:
            user_obj=CustomerModel.objects.get(id=user.id,is_deleted=0,is_phone_verified=0)
        
            if str(user.phone_otp) == otp:  
                user_obj.is_phone_verified = True
                user_obj.save() 
                return Response ({
                            "data": None,
                            "code": status.HTTP_200_OK,
                            "message": "Otp verification successfully",
                             },status = status.HTTP_200_OK)

            else:
                return Response({
                        "data": None,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "You Entered Wrong OTP",
                    })                
        except CustomerModel.DoesNotExist:
            return Response({
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "User Does Not Exist",
                })


                
    





























        


             





        















    








