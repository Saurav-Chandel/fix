from django.shortcuts import render

#imports pf signup api
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from .models import *
from datetime import datetime,timedelta,date,timezone
from django.db.models import Q
from rest_framework.response import Response
from email.mime.multipart import MIMEMultipart
from main import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth import login,authenticate,logout

# Create your views here.

from django.db.models.signals import post_save
from django.dispatch import receiver

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)  # 



@api_view(['GET','POST'])
@permission_classes(( ))
@csrf_exempt

def Signup(request):
    CustomerModel.objects.filter(date_Join__lte=(datetime.utcnow()-timedelta(minutes = 10)),is_phone_verified=0).delete()
    dictV={}
    # data=request.GET    
    Email=request.POST['Email']       #get or input the data from request user from postman
    print(Email)
    MobileNumber=request.POST['MobileNumber']
    print(MobileNumber)
    Name=request.POST['Name']
    print(Name)
    DeviceType=request.POST['DeviceType']
    DeviceToken=request.POST['DeviceToken']


    InvitationCode=''
    if len(request.POST.getlist('InvitationCode'))>0:
        InvitationCode=request.POST['InvitationCode']
    Language_id=1
    if len(request.POST.getlist('Language_id'))>0:
        Language_id=request.POST['Language_id']


    c=CustomerModel.objects.filter(email=Email,is_deleted=False,is_phone_verified=True) #filter the objects who email is exists in db and whoose isdeleted=false,isphoneverified is true.
    print(c)
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
        PhoneOTP = random.randint(1000,9999)
        phonemsg= "FixV Registration OTP is "+str(PhoneOTP)
        msg=MIMEMultipart()
        msg['FROM']=settings.DEFAULT_FROM_EMAIL
        msg['TO']=Email  
        msg['SUBJECT']="Email verification for FixV Application SignUp"

        #response= client.messages.create(messaging_service_sid='MG443a218d0365b645f8dafa9b9ae27880',body=phonemsg,to='+'+str(MobileNumber)) 
        try:
            pass
        #    verification = client.verify.services(credentials.verify_service_id).verifications.create(to='+'+str(MobileNumber), channel='sms',locale='en')
        except:
           dictV['Response']=0
           dictV['Message']='Invalid mobile number.'
           return Response(dictV) 

        #len of object who has email=email present over the db is 1..therfore if object is not present so its length is 0.if 1==0
        if len(CustomerModel.objects.filter(email=Email))==0 and len(CustomerModel.objects.filter(mobile_number=str(MobileNumber)))==0:
            c=CustomerModel.objects.create(email=Email,name=Name,mobile_number=str(MobileNumber),device_type=DeviceType,device_token=DeviceToken,phone_otp=PhoneOTP,
                language_id=Language_id,invitation_code=InvitationCode)
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
        username='Customer'+str(cid)    #return username = Customer1

        # tokenfilterobj=Token.objects.filter(user=authenticate(username=username,password=username))
        # if len(tokenfilterobj)==0:
        #     username='Customer'+str(cid)
        #     userobj=User.objects.filter(username=username)

        #     if len(userobj)==0:
        #         userobj=User.objects.create(username=username)
        #         userobj.set_password(username)
        #         userobj.save()
        #     else:
        #         userobj=User.objects.get(username=username)

        #     tokenobj=Token.objects.create(user=authenticate(username=username,password=username))
        #     tokenobj.save()
        #     dictV['Token']=tokenobj.key  
        # else:
        #     username='Customer'+str(cid)
        #     tokenobj=Token.objects.get(user=authenticate(username=username,password=username))
        #     dictV['Token']=tokenobj.key   

    return Response(dictV)            











    








