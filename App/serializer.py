from django.db.models import fields
from rest_framework import serializers
from .models import Account
from .backends import AccountAuth

class Accountserializer(serializers.ModelSerializer):
    class Meta:
        model =Account
        fields = ['email','username', 'password']


class AuthecticationSerializer():
    def UpdatePassword(Data):
        Email = Data["Email"]
        Valid_email = Account.objects.all().filter(email = Email)
        if Valid_email is not None:
            Uuid = Account.objects.all().filter(email = Email).values("UUid_Token")[0]['UUid_Token']
            AccountAuth.Get_Urls(Recipient=Email, Token=Uuid)

    def ResetPassword(Data):
        Password = Data["Password"]
        Email = Data[0]['Email']
        Account.objects.all().filter(email =Email).update(password = Password)



    def Validating_User(Data):
        try:
            Email = Data["email"]
            Password = Data["password"]
            User_Valid = AccountAuth.authenticate(Username=Email, Password= Password)

            if User_Valid is not None:
                # Isverified = Account.objects.all().filter(email=Email).values("is_email_varified")[0]["is_email_varified"]
                # if Isverified:
                return User_Valid
                # else:
                #     Uuid = Account.objects.all().filter(email = Email).values("UUid_Token")[0]['UUid_Token']
                #     AccountAuth.Send_Email(Recipient=Email,Token=Uuid)
                #     return None
            else:
                return None
        except:
            return None




    def Get_User(User_Email):
        try:
            User_Exsist = Account.objects.all().filter(email = User_Email).values("email")[0]["email"]
            return User_Exsist
        except:
            return None
