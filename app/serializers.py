from rest_framework import serializers
from app.models import CustomerModel


class CustomerSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerModel
        fields=["mobile_number",'name','email','invitation_code']

    def create(self, validated_data):
        customer = CustomerModel.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            invitation_code=validated_data['invitation_code'],
        )
        customer.set_password(validated_data['password'])
        customer.save()
        return customer 


class CustomerLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerModel
        field=["email","password"]

        extra_kwargs = {
            "password": {"write_only": True},
        }       

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerModel
        fields = "__all__"
        # fields=("email","password")
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
