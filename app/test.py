from twilio.rest import Client
import random
otp=random.randint(1000,9999)
# Your Account SID from twilio.com/console
account_sid = "AC77b0b5ff6daa1b596c30632c72e17c6a"
# Your Auth Token from twilio.com/console
auth_token  = "9e92134f37630e144c6d1449f2aad78a"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+918219356956", 
    from_="+19106066129",
    body="your otp is "+str(otp))

print(message.sid)