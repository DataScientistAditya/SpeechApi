from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Account
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import os
from datetime import datetime
import shutil
import json
import requests
from urllib import parse, request
from .models import Account,LettersTest,SentencesTest,WordTest,Storytest,Questions,IntelligenceTest,IntelligenceTestScore,InventoryTest,InventoryTestScore,PostTestLettersScore,PostTestSentencesScore,PostWordTestScore,PostTestStoryQuestions,PostStorytestScore

class AccountAuth(ModelBackend):

    def authenticate(Username=None, Password = None):
        #UserModel = get_user_model()
        if Username is not None:
            try:
                Id = Account.objects.all().filter(email = Username).values("id")[0]["id"]
            except:
                Id = None
        if Id is not None:
            try:
                user_pass = Account.objects.all().filter(id = Id).values("password")[0]['password']
                if user_pass == Password:
                    return Id
            except:
                return None

        else:
            return None

    def get_user(self,id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk= id) # <-- must be primary key and number
        except User.DoesNotExist:
            return None

    def Send_Email(Recipient, Token,Name):
        try:
            Subject = "Peruzor Email Verification"
            Message = f"https://www.peruzor.com/Verify/{Token}"
            Html_Content = render_to_string('EmailTemplate.html',{'Name':Name, 'VerificationLink':Message})
            Text_Content = strip_tags(Html_Content)
            Email_Sender = settings.EMAIL_HOST_USER
            Email_Reciever = [Recipient]
            Email = EmailMultiAlternatives(
                    Subject,
                    Text_Content,
                    Email_Sender,
                    Email_Reciever
                )
            Email.attach_alternative(Html_Content,"text/html")
            Email.send()
            return Subject
        except:
            return None


    def GetPretestResults(Uid):
        ListofScores=[]
        try:
            Int_ID= int(Uid)
            Id = Account.objects.all().filter(id = Int_ID).values("id")[0]["id"]
            LettersScore = LettersTest.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            WordsScore = WordTest.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            SenetenceScore = SentencesTest.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            StoryScore = Storytest.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            StoryTestMissingWords = Storytest.objects.all().filter(user = Int_ID).values("Numberof_MissingWords").last()["Numberof_MissingWords"]

            LettersTestDict = {"Letters":LettersScore}
            SentenceTestDict = {"Sentence":SenetenceScore}
            WordsTestDict = {"Words":WordsScore}
            StoryTestDict = {"Story":StoryScore}
            StorytestMissingDict = {"StoryMissing":StoryTestMissingWords}
            ListofScores.append([LettersTestDict,SentenceTestDict,WordsTestDict,StoryTestDict,StorytestMissingDict])
            return ListofScores
        except(InterfaceError, DatabaseError) as e:
            db.connection.close()
            Id = Account.objects.all().filter(id = Uid).values("id")[0]["id"]
            return Id

    def GetPosttestResults(Uid):
        ListofScores=[]
        try:
            Int_ID= int(Uid)
            Id = Account.objects.all().filter(id = Int_ID).values("id")[0]["id"]
            LettersScore = PostTestLettersScore.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            WordsScore = PostWordTestScore.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            SenetenceScore = PostTestSentencesScore.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            StoryScore = PostStorytestScore.objects.all().filter(user = Int_ID).values("Score").last()["Score"]
            StoryTestMissingWords = PostStorytestScore.objects.all().filter(user = Int_ID).values("Numberof_MissingWords").last()["Numberof_MissingWords"]

            LettersTestDict = {"Letters":LettersScore}
            SentenceTestDict = {"Sentence":SenetenceScore}
            WordsTestDict = {"Words":WordsScore}
            StoryTestDict = {"Story":StoryScore}
            StorytestMissingDict = {"StoryMissing":StoryTestMissingWords}
            ListofScores.append([LettersTestDict,SentenceTestDict,WordsTestDict,StoryTestDict,StorytestMissingDict])
            return ListofScores
        except:
            return None
