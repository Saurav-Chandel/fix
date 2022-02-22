from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta

# Create your models here.

def currentDateTime():
    return datetime.utcnow()

genderChoices = ( ('Male','Male'), ('Female','Female'), ('Others','Others'))
ItemBrandChoices=(('Samsung', 1),('Apple', 2))
CategoryChoices=(('Service', 1),('Storage', 2),('Memory', 3),('Network', 4))



class AppUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("username",email)
      
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a Super Admin. Not to be used by any API. Only used for django-admin command.
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('username', email)
        extra_fields.setdefault('is_phone_verified', True)

        user = self._create_user(email, password, **extra_fields)
        return user


class Reasons(models.Model):
    id=models.AutoField(primary_key=True)  
    reason_type=models.CharField(max_length = 500, blank = True, null = True)
    date_added= models.DateTimeField(default = datetime.utcnow)
    reason=models.CharField(max_length = 500, blank = True, null = True)
    arabic_reason=models.CharField(max_length = 500, blank = True, null = True)

    def __str__(self):
        template = '{0.reason_type} {0.reason} {0.date_added}'
        return template.format(self)

    def __unicode__(self):
        return self.reason_type


class CustomerModel(AbstractUser):
    name = models.CharField(
        max_length=200, default=None, null=True, blank=True
    )
    email=models.EmailField(max_length=70,unique=True,null=True,blank=True)
    dob=models.DateTimeField(default=None,blank=True,null=True)
    mobile_number = models.CharField(max_length = 15,blank = True, null = True,unique=True)
    device_token = models.CharField(max_length = 200, blank = True, null = True)
    device_type = models.CharField(max_length = 7,  blank = True, null = True)
    gender = models.CharField(max_length = 7,  blank = True, null = True,choices = genderChoices)
    profile_image = models.ImageField(upload_to='Customer_Profile_Images/',blank = True, null = True)
    date_Join = models.DateTimeField(default = datetime.utcnow)
    phone_otp=models.BigIntegerField(blank = True, null = True)
    email_otp=models.BigIntegerField(blank = True, null = True)
    is_email_verified=models.BooleanField(default = False)
    is_phone_verified=models.BooleanField(default = False)
    is_deleted=models.BooleanField(default = False)
    delete_reason_id=models.ForeignKey(Reasons,on_delete=models.CASCADE, blank = True,null=True)
    description=models.CharField(max_length = 200, blank = True, null = True)
    total_points=models.BigIntegerField(default=0)
    referal_code=models.CharField(max_length = 7, blank = True, null = True)
    invitation_code=models.CharField(max_length = 7, blank = True, null = True)
    type=models.CharField(max_length = 200, blank = True, null = True)
    language_id=models.CharField(max_length = 6, blank = True, null = True)
    active=models.CharField(max_length = 100,default="Yes")
    is_disabled=models.BooleanField(default = False)

    manager = AppUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        
        return str(self.email)


    # def __unicode__(self):
    #     if self.name:
    #         return u'%s'%( self.name )
    #     else:
    #         return u'%s'%( self.authUser.username )



class ArchivedCustomers(models.Model):
    id=models.BigIntegerField(primary_key=True) 
    name = models.CharField(max_length = 500, default = 'Customer')
    email = models.EmailField(max_length=70,unique=True,null=True,blank=True)
    dob = models.DateField(default = None,blank = True, null = True)
    mobile_number = models.CharField(max_length = 15,blank = True, null = True)
    device_token = models.CharField(max_length = 500, blank = True, null = True)
    device_type = models.CharField(max_length = 7,  blank = True, null = True)
    gender = models.CharField(max_length = 7,  blank = True, null = True,choices = genderChoices)
    profile_images = models.ImageField(upload_to='Customer_Profile_Images/',blank = True, null = True)
    date_joined = models.DateTimeField(default = datetime.utcnow)
    phone_otp=models.BigIntegerField(blank = True, null = True)
    email_otp=models.BigIntegerField(blank = True, null = True)
    is_mail_verified=models.BooleanField(default = False)
    is_phone_verified=models.BooleanField(default = False)
    is_deleted=models.BooleanField(default = False)
    delete_reason_id=models.ForeignKey(Reasons,on_delete=models.CASCADE,null=True)
    description=models.CharField(max_length = 500, blank = True, null = True)
    total_points=models.BigIntegerField(default=0)
    referal_code=models.CharField(max_length = 7, blank = True, null = True)
    invitation_code=models.CharField(max_length = 7, blank = True, null = True)
    type=models.CharField(max_length = 500, blank = True, null = True)
    language_id=models.CharField(max_length = 6, blank = True, null = True)
    active=models.CharField(max_length = 100,default="Yes")
    is_disabled=models.BooleanField(default = False)
    date_deleted = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        template = '{0.id} {0.Name} {0.mobile_number} {0.email}'
        return template.format(self)


class Problems(models.Model):
    name = models.CharField(max_length = 500,unique=True)
    arabic_name = models.CharField(max_length = 500,blank = True, null = True)
    image=models.ImageField(blank = True, null = True)
    selection_image=models.ImageField(blank = True, null = True)

    def __str__(self):
        return self.name


class ProblemOptions(models.Model):
    problem_id=models.ForeignKey(Problems,on_delete=models.CASCADE)
    options = models.CharField(max_length = 500)
    arabic_options = models.CharField(max_length = 500,blank = True, null = True)

    def __str__(self):
        return self.problem_id.name