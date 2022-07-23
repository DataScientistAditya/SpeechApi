import json
import random
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .serializer import Accountserializer,AuthecticationSerializer
from .models import Account,LettersTest,SentencesTest,WordTest,Storytest,Questions,IntelligenceTest,IntelligenceTestScore,InventoryTest,InventoryTestScore,PostTestLettersScore,PostTestSentencesScore,PostWordTestScore,PostTestStoryQuestions,PostStorytestScore
from django.views.decorators.csrf import csrf_exempt
import requests
from .backends import AccountAuth
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import os
import time
from pydub import AudioSegment

# Create your views here.


@csrf_exempt
def Register(request):

    if request.method == "POST":
        data = JSONParser().parse(request)
        Serializer = Accountserializer(data=data)
        if Serializer.is_valid():
            try:
                Serializer.save()
                try:
                    Email= data["email"]
                    Uuid = Account.objects.all().filter(email = Email).values("UUid_Token")[0]['UUid_Token']
                    Id = Account.objects.all().filter(email = Email).values("id")[0]['id']
                    Uuid_Str = str(Uuid)
                    token = "{}_{}_{}".format(Uuid_Str,Id,data["username"])
                    isEmailSent = AccountAuth.Send_Email(Recipient=Email,Token=token,Name=data['username'])
                    if isEmailSent != None:
                        Dict = {"Ud":Uuid,"Username":data["username"],"data":"A verification Email sent you"}
                        return JsonResponse(Dict, status =201)
                    else:
                        Dict = {"data":"You are Registered, Please Login"}
                        return JsonResponse(Dict, status =201)
                except:
                    Dict = {"data":"Not able to Register"}
                    return JsonResponse(Dict, status =400)

            except:
                Dict = {"data":"Somthing went wrong"}
                return JsonResponse(Dict, status =400)
        else:
            Dict_Valid = {"data":"User Already Exists"}
            return JsonResponse(Dict_Valid, status =400)
    elif request.method == "GET":
        Dict_Valid = {"data":"Not a valid request"}
        #Serializer_get = Accountserializer(data, many=True)
        return JsonResponse(Dict_Valid, status =400)




@csrf_exempt
def Login(request):
    Dict={}
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            User_Valid = AuthecticationSerializer.Validating_User(Data=data)
            if User_Valid is not None:
                try:
                    Int_Id = int(User_Valid)
                    Uuid = Account.objects.all().filter(id = Int_Id).values("UUid_Token")[0]['UUid_Token']
                    Username = Account.objects.all().filter(id = Int_Id).values("username")[0]['username']
                    Uuid_Str = str(Uuid)
                    token = "{}_{}_{}".format(Uuid_Str,Int_Id,Username)
                    Dict["Ud"] = token
                    return JsonResponse(Dict,status=201)
                except:
                    Dict["Ud"] = {"Valid_User":"Somthing went wrong"}
                    return JsonResponse(Dict,status=400)
            else:
                Dict = {"Valid_User":"No"}
                return JsonResponse(Dict,status =400 )
        else:
            Dict = {"Valid_User":"Please Enter valid credentials"}
            return JsonResponse(Dict, status =400)
    else:
        Dict = {"Valid_User":"Please Enter valid credentials"}
        return JsonResponse(Dict, status =404)



@csrf_exempt
def CompareSentences(request):
    DispalySentences = ["I Love You","I can play with the bat and ball here","The three boys like to walk to the bus stop",
    "We are sleeping We woke up late and we are very tired","Mother and father work from home They help people and tell them what to do Some of them left their houses very early",
    "Sometimes we need to place animals into groups of same and different Together we must write the important ones on the same list"]
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            Dict = {}
            Sentence = data["SpelledSentence"]
            Index = data["index"]
            IntIndex = int(Index)
            print("Sentence is",Sentence)
            print("Index is",IntIndex)
            SmallSentence = str(DispalySentences[IntIndex]).lower()
            Split_Original_Sentences_List = str(SmallSentence).split(" ")
            SentenceListLower = str(Sentence).lower()
            SentenceList = str(SentenceListLower).split(" ")
            Diffrence_Of_Sentences = list(set(Split_Original_Sentences_List) - set(SentenceList))
            if len(Diffrence_Of_Sentences)>0:
                Dict["Unmatched"] = Diffrence_Of_Sentences
                print(Dict)
                return JsonResponse(Dict,safe=False,status=201)
            else:
                Dict["Unmatched"] = "None"
                print(Dict)
                return JsonResponse(Dict,safe=False,status=201)
        else:
            dictError = {"Unmatched":"Not Valid Data"}
            return JsonResponse(dictError,status=404)
    else:
        dictError = {"Unmatched":"Not Valid Request"}
        return JsonResponse(dictError,status=500)


@csrf_exempt
def LetterTestScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id ).values("id")[0]["id"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id= Int_Id)
                Data_toSaved = LettersTest(user = User_Obj, Score = data["Score"] )
                Data_toSaved.save()
                Account.objects.all().filter(id = Int_Id).update(is_Letterstest = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=500)



@csrf_exempt
def SentenceTestScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id ).values("id")[0]["id"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id = Int_Id )
                Data_toSaved = SentencesTest(user = User_Obj, Score = data["Score"] )
                Data_toSaved.save()
                Account.objects.all().filter(id = Int_Id).update(is_SentenceTest = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=400)




@csrf_exempt
def GetSentenceTestScore(request):
    Preprimer = ["a","and","away","big","blue","can","come","down","find","for","funny","go","help","here","I","in","is","it","jump","little","look","make","me","my","not","one","play","red","run","said","see","the","three","to","two","up","we","where","yellow","you"]
    Primer = ["all","am","are", "at","ate","be","black","brown","but","came","did","do","eat","four","get","good","have","he","into","like","must","new","no","now","on","our","out","please","pretty","ran","ride","saw","say","she","so","soon","that","there","they","this","Too","under","want","was","well","went","what","white","who","will","with","yes"]
    Level1 = ["after","again","an","any","ask","as","by","could","every","fly","from","give","going","had","has","her","him","his","how","just","know","let","live","may","of","old","once","open","over","put","round","some","stop","take","thank","them","then","think","walk","were","When"]
    Level2 = ["always","around","because","been","before","best","both","buy","call","cold","does","don’t","fast","first","five","found","gave","goes","green","its","made","many","off","or","pull","read","right","sing","sit","sleep","tell","their","these","those","upon","us","use","very","wash","Which","why","wish","work","would","write","your","Warm"]
    Level3 = ["about","better","bring","carry","clean","cut","done","draw","drink","eight","fall","far","full","got","grow","hold","hot","hurt","if","keep","kind","laugh","light","long","much","myself","never","only","own","pick","seven","shall","show","six","small","start","ten","today","together","try"]
    Level4 = ["listen","important","event","towards","notice","problems","favourite","information","hundred","continue","pleaded","complete","Coaches","however","excitement","several","perfect","culture","voice","Products","ply","prepare","return","distance","certain","travel","thought","laugh","provision","gathered","transport","known","health","produce","video","written","enough","brought"]
    Preprimer_and_Premier_Number_of_List = 10
    Level1_to_Level3 = 15
    Level4_to_Level6 = 20
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id ).values("id")[0]["id"]
            if Valid_User is not None:
                if data["TestType"] == "PostTest":
                    Scores = PostTestSentencesScore.objects.all().filter(user = Valid_User).values("Score").last()['Score']
                elif data["TestType"] == "PreTest":
                    Scores = SentencesTest.objects.all().filter(user = Valid_User).values("Score").last()['Score']
                print(Scores)
                Score=int(Scores)
                if Score<1:
                    List = random.sample(Preprimer,Preprimer_and_Premier_Number_of_List)
                    print(List)
                    Dict ={"DataList":List,"type":"Preprimer"}
                    return JsonResponse(Dict,status=201)
                if Score==1:
                    List = random.sample(Primer,Preprimer_and_Premier_Number_of_List)
                    print(List)
                    Dict ={"DataList":List,"type":"Primer"}
                    return JsonResponse(Dict,status=201)
                if Score==2:
                    List = random.sample(Level1,Level1_to_Level3)
                    print(List)
                    Dict ={"DataList":List,"type":"Level1"}
                    return JsonResponse(Dict,status=201)
                if Score==3:
                    List = random.sample(Level2,Level1_to_Level3)
                    print(List)
                    Dict ={"DataList":List,"type":"Level2"}
                    return JsonResponse(Dict,status=201)
                if Score == 4:
                    List = random.sample(Level3,Level1_to_Level3)
                    print(List)
                    Dict ={"DataList":List,"type":"Level3"}
                    return JsonResponse(Dict,status=201)
                if Score==5:
                    List = random.sample(Level4,Level4_to_Level6)
                    print(List)
                    Dict ={"DataList":List,"type":"Level4"}
                    return JsonResponse(Dict,status=201)

        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=400)





@csrf_exempt
def WordsTestScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id ).values("id")[0]["id"]
            #Valid_User = Account.objects.all().filter(UUid_Token = data["Uid"]).values("UUid_Token")[0]["UUid_Token"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id = Int_Id)
                Data_toSaved = WordTest(user = User_Obj, Score = data["Score"], TypeofTest = data["Level"] )
                Data_toSaved.save()
                Account.objects.all().filter(id = Int_Id).update(is_Wordsstest = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=400)



@csrf_exempt
def GetWordsTestScore(request):
    Preprimer = "I am Roy I am a big boy I can play bat and ball Pam is a little girl She can play bat and ball "
    Primer = "I have two brown and white cats They love to run and play They love milk Father has a pet at home too He has a pet dog and it loves run and jump The dog is black with white It loves to eat food It is big When I go to school mother stays at home with our pets "
    Level1 = "Pat lives on a farm There are pigs and hens on the farm It rains on the farm The hens run to get out of the rain They look funny when they are wet The pigs like to play in the rain The rain is good for the farmer He can get good things to take to the market After the rain stops, the farmer goes to the market He likes to go to the market"
    Level2 = "Cake day at home My name is Peter There are four of us at home mother father Ann and I We have cake day at home Mother and Ann make the cake First they buy the things they need Then they read the labels wash their hands and write what they should do Mother and Ann sing when they bake Father and I work in the yard When the cake is done mother takes it from the oven She puts it to cool on the table We wash up and then we eat our cake We love our cake day at home "
    Level3 = "Tom and his friends love to draw and paint Together they do pretty pictures in class They do their best work when they are at school First they think about what they would want to draw Then they get all the items that they need Next they begin Tom likes to use cold colours when he draws and paints Cold colours are blue green and purple His friends like to use warm colours like red yellow and orange When they work together they use only the three Primary colours to get all the six colours The Primary colours are red yellow and blue If the paint falls on the floor they clean it up When they are finished painting they show their work to their friends and family Friends and family will buy their paintings "
    Level4 = "Sports days at school are an important part of our culture Athletes and non-athletes look forward to this activity filled event This annual event is normally held on the two day before Ash Wednesday The excitement begins weeks even months before the big days Students and teachers dress in their house colours sing cheers and practice for each event Some of the events include cheerleading cross-country race one hundred up eight hundred metre race shuttle relay and my favourite baton relays Glucose oranges and water are a must have for these days as the days are usually very hot and runners get very competitive Coaches and teachers select their best runners or the person they believe would have a chance at winning There are four houses at our school They are Red House Blue House Yellow and Green Houses I had recently transferred from another school and my house leader or captain did not know about my abilities On the day of the big events I pleaded with the house leader to let me run but I was told that they had all the athletes for each race already So I went back to my seat to continue watching the races When it was time for the eight hundred metres race the announcer called for two runners from each house Then I overheard the house leader and captain discussing that they only had one name written done I immediately volunteered myself as both looked at me from head to toe as if to say he is so frail The announcer repeated the call and they said go ahead I quickly changed into my gears and confidently walked onto the field to the starting position That day I surpassed everyone's expectations"
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id ).values("id")[0]["id"]
            #Valid_User = Account.objects.all().filter(UUid_Token = data["Uid"]).values("id")[0]["id"]
            if Valid_User is not None:
                Scores = WordTest.objects.all().filter(user = Valid_User).values("Score").last()['Score']
                TestType = WordTest.objects.all().filter(user = Valid_User).values("TypeofTest").last()['TypeofTest']
                print(Scores)
                Score=int(Scores)

                #Pre-Premier stories
                if TestType == "Preprimer":
                    if Score<8:
                        Dict ={"DataList":Preprimer,"type":"Preprimer"}
                        return JsonResponse(Dict,status=201)
                    if Score>=8:
                        Dict ={"DataList":Primer,"type":"Primer"}
                        return JsonResponse(Dict,status=201)

                #Premier Stories
                if TestType == "Primer":
                    if Score<8:
                        Dict ={"DataList":Preprimer,"type":"Preprimer"}
                        return JsonResponse(Dict,status=201)
                    if Score>=8:
                        Dict ={"DataList":Primer,"type":"Primer"}
                        return JsonResponse(Dict,status=201)

                #Level1 stories
                if TestType == "Level1":
                    if Score<12:
                        Dict ={"DataList":Primer,"type":"Primer"}
                        return JsonResponse(Dict,status=201)
                    if Score>=12:
                        Dict ={"DataList":Level1,"type":"Level1"}
                        return JsonResponse(Dict,status=201)

                #Level 2 Stories
                if TestType == "Level2":
                    if Score<12:
                        Dict ={"DataList":Level1,"type":"Level1"}
                        return JsonResponse(Dict,status=201)
                    if Score>=12:
                        Dict ={"DataList":Level2,"type":"Level2"}
                        return JsonResponse(Dict,status=201)

                #Level3 Stories
                if TestType == "Level3":
                    if Score<12:
                        Dict ={"DataList":Level2,"type":"Level2"}
                        return JsonResponse(Dict,status=201)
                    if Score>=12:
                        Dict ={"DataList":Level3,"type":"Level3"}
                        return JsonResponse(Dict,status=201)

                #Level4 Stories
                if TestType=="Level4":
                    if Score<15:
                        Dict ={"DataList":Level3,"type":"Level3"}
                        return JsonResponse(Dict,status=201)
                    if Score>=15:
                        Dict ={"DataList":Level4,"type":"Level4"}
                        return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=400)


@csrf_exempt
def SetStoryTestScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id ).values("id")[0]["id"]
            #Valid_User = Account.objects.all().filter(UUid_Token = data["Uid"]).values("UUid_Token")[0]["UUid_Token"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id = Int_Id)
                Data_toSaved = Storytest(user = User_Obj, Score = data["Score"], TypeofTest = data["Level"], Numberof_MissingWords = data["Missing"] )
                Data_toSaved.save()
                Account.objects.all().filter(id = Int_Id).update(is_Storiestest = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=500)



@csrf_exempt
def Verify(request):
    Dict ={}
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            if Valid is not None:
                Account.objects.all().filter(id = Int_Id).update(is_email_varified = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
            else:
                pass
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=403)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=500)





@csrf_exempt
def Retake(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            Account.objects.all().filter(id = Int_Id).update(is_Letterstest = False)
            Account.objects.all().filter(id = Int_Id).update(is_SentenceTest = False)
            Account.objects.all().filter(id = Int_Id).update(is_Wordsstest = False)
            Account.objects.all().filter(id = Int_Id).update(is_Storiestest = False)
            Dict ={"Ud":data["Uid"]}
            return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not valid Request"}
        return JsonResponse(Dict,status=500)




@csrf_exempt
def PostTestRetake(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            Account.objects.all().filter(id = Int_Id).update(is_PostTestletters = False)
            Account.objects.all().filter(id = Int_Id).update(is_PostTestSentences = False)
            Account.objects.all().filter(id = Int_Id).update(is_PostTestWords = False)
            Account.objects.all().filter(id = Int_Id).update(is_PostTestStories = False)
            Dict ={"Ud":data["Uid"]}
            return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not valid Request"}
        return JsonResponse(Dict,status=500)




@csrf_exempt
def CompareStories(request):
    Preprimer = "I am Roy.I am a big boy I can play bat and ball Pam is a little girl She can play bat and ball "
    Primer = "I have two brown and white cats They love to run and play They love milk Father has a pet at home too He has a pet dog and it loves run and jump The dog is black with white It loves to eat food  It is big When I go to school mother stays at home with our pets "
    Level1 = "Pat lives on a farm There are pigs and hens on the farm It rains on the farm The hens run to get out of the rain They look funny when they are wet The pigs like to play in the rain The rain is good for the farmer  He can get good things to take to the market After the rain stops, the farmer goes to the market  He likes to go to the market "
    Level2 = "Cake day at home My name is Peter  There are four of us at home, mother, father, Ann and I We have cake day at home Mother and Ann make the cake First, they buy the things they need Then they read the labels, wash their hands and write what they should do Mother and Ann sing when they bake  Father and I work in the yard When the cake is done, mother takes it from the oven She puts it to cool on the table We wash up and then we eat our cake We love our cake day at home "
    Level3 = "Tom and his friends love to draw and paint Together they do pretty pictures in class  They do their best work when they are at school First, they think about what they would want to draw Then they get all the items that they need  Next they begin Tom likes to use cold colours when he draws and paints  Cold colours are blue, green and purple His friends like to use warm colours like red, yellow and orange  When they work together they use only the three Primary colours to get all the six colours The Primary colours are red, yellow and blue If the paint falls on the floor, they clean it up When they are finished painting, they show their work to their friends and family Friends and family will buy their paintings "
    Level4 = "Sports days at school are an important part of our culture  Athletes and non-athletes look forward to this activity filled event This annual event is normally held on the two day before Ash Wednesday The excitement begins weeks, even months before the big days  Students and teachers dress in their house colours, sing cheers and practice for each event Some of the events include cheerleading, cross-country race, one hundred,  up eight hundred metre race, shuttle relay and my favourite baton relays  Glucose, oranges and water are a must have for these days as the days are usually very hot and runners get very competitive Coaches and teachers select their best runners or the person they believe would have a chance at winning There are four houses at our school  They are Red House, Blue House, Yellow and Green Houses I had recently transferred from another school and my house leader or captain did not know about my abilities  On the day of the big events, I pleaded with the house leader to let me run but I was told that they had all the athletes for each race already  So I went back to my seat to continue watching the races  When it was time for the eight hundred metres race the announcer called for two runners from each house  Then I overheard the house leader and captain discussing that they only had one name written done I immediately volunteered myself as both looked at me from head to toe as if to say, he is so frail  The announcer repeated the call and they said go ahead  I quickly changed into my gears and confidently walked onto the field to the starting position  That day, I surpassed everyone's expectations "
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            Dict = {}
            Type = data["type"]
            Value = data["story"]
            List_Response = {}
            #PrePrimer
            if Type=="Preprimer":
                List_Of_Dict = []
                List_of_Quistions = Questions.objects.all().filter(TestType ="Preprimer" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Preprimer.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)

            #Level1
            if Type=="Level1":
                List_Of_Dict = []
                List_of_Quistions = Questions.objects.all().filter(TestType ="Level1" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level1.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)

            #Level2
            if Type=="Level2":
                List_Of_Dict = []
                List_of_Quistions = Questions.objects.all().filter(TestType ="Level2" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level2.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
            #Level3
            if Type=="Level3":
                List_Of_Dict = []
                List_of_Quistions = Questions.objects.all().filter(TestType ="Level3" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level3.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
            #Level4
            if Type=="Level4":
                List_Of_Dict = []
                List_of_Quistions = Questions.objects.all().filter(TestType ="Level4" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level4.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)

            #Primer
            if Type=="Primer":
                List_Of_Dict = []
                List_of_Quistions = Questions.objects.all().filter(TestType ="Primer" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Primer.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
        else:
            dictError = {"Unmatched":"Not Valid Data"}
            return JsonResponse(dictError,status=401)
    else:
        dictError = {"Unmatched":"Not Valid Request"}
        return JsonResponse(dictError,status=500)


@csrf_exempt
def Resetpaswword(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        Dict={}
        try:
            Account.objects.all().filter(email = data["email"]).update(password = data["password"])
            Dict["res"] = "Password Changed"
            print(Dict)
            return JsonResponse(Dict,safe=False,status=201)
        except:
            Dict["res"] = "Password not Changed"
            print(Dict)
            return JsonResponse(Dict,safe=False,status=404)
    else:
        Dict["res"] = "not valid Request"
        return JsonResponse(Dict,safe=False,status=500)


def FetchIntelligenceQsn(request):
    try:
        QsnData= IntelligenceTest.objects.all().values("Question","Answer1","Answer2","Answer3")
        ListofIntlqsn=[]
        Dict={}
        for i in QsnData:
            ListofIntlqsn.append(i)
        Dict["intslist"] = ListofIntlqsn
        print(Dict)
        return JsonResponse(Dict,status=201)
    except:
        Dict["msg"] = "Not a valid request"
        return JsonResponse(Dict,status=500)




@csrf_exempt
def GetIntelligenceResult(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print("Data for Calculation",data)
        Dict={}
        try:
            Spatial_List = []
            Musical_List = []
            Logical_List = []
            Bodily_List = []
            Linguistic_List = []
            Intra_List = []
            Inter_List = []
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            User_Obj = Account.objects.get(id = Int_Id)
            AnsList=data["AnswerList"]
            Original_List = IntelligenceTest.objects.all().values("TypeofQsn")
            for i in range(len(Original_List)):
                if AnsList[i] == "True":
                    if Original_List[i]['TypeofQsn']=='Spatial':
                        Spatial_List.append("Answer_Spatial")

                    if Original_List[i]['TypeofQsn'] == "Musical":
                        Musical_List.append("Answer_Musical")

                    if Original_List[i]['TypeofQsn'] == "Logical- Mathematical":
                        Logical_List.append("Answer_Logical")

                    if Original_List[i]['TypeofQsn'] == "Bodily- Kinesthetic":
                        Bodily_List.append("Answer_Bodily")

                    if Original_List[i]['TypeofQsn'] == "Linguistic":
                        Linguistic_List.append("Answer_Linguistic")

                    if Original_List[i]['TypeofQsn'] == "Intra-personal":
                        Intra_List.append("Answer_Intra")

                    if Original_List[i]['TypeofQsn'] == "Inter-personal":
                        Inter_List.append("Answer_Inter")

            #print("List of all list is",[Linguistic_List,Logical_List,Musical_List,Spatial_List,Bodily_List])
            ListLen_List = []
            for lst in [Linguistic_List,Logical_List,Musical_List,Spatial_List,Bodily_List,Intra_List,Inter_List]:
                ListLen_List.append(len(lst))

            Max_Value = max(ListLen_List)
            Maxvalue_Index = ListLen_List.index(Max_Value)

            if Maxvalue_Index == 0:
                Dict["Character"] = "Strong ability"
                Data_To_be_Saved = IntelligenceTestScore(user = User_Obj, Linguistic = ListLen_List[0],Logical = ListLen_List[1], Musical=ListLen_List[2],Spatial = ListLen_List[3],Bodily = ListLen_List[4],Intra = ListLen_List[5],Inter = ListLen_List[6],TopScoreSection="Linguistic")
                Data_To_be_Saved.save()
                Account.objects.all().filter(id = Int_Id).update(is_IntelligenceTest = True)
                return JsonResponse(Dict,status=201)
            if Maxvalue_Index == 1:
                Dict["Character"] = "Strong ability"
                Data_To_be_Saved = IntelligenceTestScore(user = User_Obj, Linguistic = ListLen_List[0],Logical = ListLen_List[1], Musical=ListLen_List[2],Spatial = ListLen_List[3],Bodily = ListLen_List[4],Intra = ListLen_List[5],Inter = ListLen_List[6],TopScoreSection="Logical")
                Data_To_be_Saved.save()
                Account.objects.all().filter(id = Int_Id).update(is_IntelligenceTest = True)
                return JsonResponse(Dict,status=201)

            if Maxvalue_Index == 2:
                Dict["Character"] = "Strong ability"
                Data_To_be_Saved = IntelligenceTestScore(user = User_Obj, Linguistic = ListLen_List[0],Logical = ListLen_List[1], Musical=ListLen_List[2],Spatial = ListLen_List[3],Bodily = ListLen_List[4],Intra = ListLen_List[5],Inter = ListLen_List[6],TopScoreSection="Musical")
                Data_To_be_Saved.save()
                Account.objects.all().filter(id = Int_Id).update(is_IntelligenceTest = True)
                return JsonResponse(Dict,status=201)

            if Maxvalue_Index == 3:
                Dict["Character"] = "Strong ability"
                Data_To_be_Saved = IntelligenceTestScore(user = User_Obj, Linguistic = ListLen_List[0],Logical = ListLen_List[1], Musical=ListLen_List[2],Spatial = ListLen_List[3],Bodily = ListLen_List[4],Intra = ListLen_List[5],Inter = ListLen_List[6],TopScoreSection="Spatial")
                Data_To_be_Saved.save()
                Account.objects.all().filter(id = Int_Id).update(is_IntelligenceTest = True)
                return JsonResponse(Dict,status=201)

            if Maxvalue_Index == 4:
                Dict["Character"] = "Strong ability"
                Data_To_be_Saved = IntelligenceTestScore(user = User_Obj, Linguistic = ListLen_List[0],Logical = ListLen_List[1], Musical=ListLen_List[2],Spatial = ListLen_List[3],Bodily = ListLen_List[4],Intra = ListLen_List[5],Inter = ListLen_List[6],TopScoreSection="Bodily")
                Data_To_be_Saved.save()
                Account.objects.all().filter(id = Int_Id).update(is_IntelligenceTest = True)
                return JsonResponse(Dict,status=201)

            if Maxvalue_Index == 5:
                Dict["Character"] = "Good ability"
                Data_To_be_Saved = IntelligenceTestScore(user = User_Obj, Linguistic = ListLen_List[0],Logical = ListLen_List[1], Musical=ListLen_List[2],Spatial = ListLen_List[3],Bodily = ListLen_List[4],Intra = ListLen_List[5],Inter = ListLen_List[6],TopScoreSection="Intra-personal")
                Data_To_be_Saved.save()
                Account.objects.all().filter(id = Int_Id).update(is_IntelligenceTest = True)
                return JsonResponse(Dict,status=201)

            if Maxvalue_Index == 6:
                Dict["Character"] = "Good ability"
                Data_To_be_Saved = IntelligenceTestScore(user = User_Obj, Linguistic = ListLen_List[0],Logical = ListLen_List[1], Musical=ListLen_List[2],Spatial = ListLen_List[3],Bodily = ListLen_List[4],Intra = ListLen_List[5],Inter = ListLen_List[6],TopScoreSection="Inter-personal")
                Data_To_be_Saved.save()
                Account.objects.all().filter(id = Int_Id).update(is_IntelligenceTest = True)
                return JsonResponse(Dict,status=201)
        except:
            Dict["msg"] ="User not found"
            return JsonResponse(Dict,status=404)
    else:
        Dict["msg"]= "Not a valid request"
        return JsonResponse(Dict,status=500)







def GetInventoryQuestions(request):
    Listofqsn=[]
    Dict = {}
    try:
        Ques = InventoryTest.objects.all().values("Question","Answer1","Answer2","Answer3")
        for j in Ques:
            Listofqsn.append(j)
        Dict["intslist"] = Listofqsn
        return JsonResponse(Dict,status=201)
    except:
        return JsonResponse(Dict,status=404)





@csrf_exempt
def SendInventoryResult(request):
    if request.method=="POST":
        data = JSONParser().parse(request)
        Dict={}
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            User_Obj = Account.objects.get(id = Int_Id)
            AnswerLists = data["AnswerList"]
            Score = 0
            for i in AnswerLists:
                if i == "Always":
                    Score= Score + 2
                if i == "Sometime":
                    Score= Score + 1
                if i == "Never":
                    Score = Score + 0


            Data_to_be_Saved = InventoryTestScore(user = User_Obj,Score = Score)
            Data_to_be_Saved.save()
            Dict["Score"] = Score
            return JsonResponse(Dict,status=201)
        except:
            Dict["msg"] = "Not a valid User"
            return JsonResponse(Dict,status=404)







@csrf_exempt
def GetCompletedTest(request):
    if request.method=="POST":
        data = JSONParser().parse(request)
        Dict={}
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Uid_Token=Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            Is_LetterTest = Account.objects.all().filter(id=Uid_Token).values("is_Letterstest")[0]["is_Letterstest"]
            Is_WordsTest = Account.objects.all().filter(id=Uid_Token).values("is_Wordsstest")[0]["is_Wordsstest"]
            Is_SentenceTest = Account.objects.all().filter(id=Uid_Token).values("is_SentenceTest")[0]["is_SentenceTest"]
            Is_StoryTest = Account.objects.all().filter(id=Uid_Token).values("is_Storiestest")[0]["is_Storiestest"]


            """
            if Is_Intelligenence_Test:
                Dict = {"TestPassed":"Intl"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            """
            if Is_StoryTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"Story"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_StoryTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"Story"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_WordsTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"Words"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_SentenceTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"Sentence"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_LetterTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"Letters"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_LetterTest == False:
                Dict = {"Ud":data["Uid"],"TestPassed":"Pretest"}
                print(Dict)
                return JsonResponse(Dict,status =201)
        except:
            Dict={"msg":"User not valid"}
            return JsonResponse(Dict,status =404)
    else:
        Dict={"msg":"request is not valid"}
        return JsonResponse(Dict,status =500)





@csrf_exempt
def GetCompletedPostTest(request):
    if request.method=="POST":
        data = JSONParser().parse(request)
        Dict={}
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            #Uid_Token=Account.objects.all().filter(UUid_Token = data["Uid"]).values("UUid_Token")[0]["UUid_Token"]
            Is_PostLetterTest=Account.objects.all().filter(id = Int_Id).values("is_PostTestletters")[0]["is_PostTestletters"]
            Is_PostSentenceTest=Account.objects.all().filter(id = Int_Id).values("is_PostTestSentences")[0]["is_PostTestSentences"]
            Is_PostWordsTest=Account.objects.all().filter(id = Int_Id).values("is_PostTestWords")[0]["is_PostTestWords"]
            Is_PostStoryTest=Account.objects.all().filter(id = Int_Id).values("is_PostTestStories")[0]["is_PostTestStories"]
            #Is_Intelligenence_Test = Account.objects.all().filter(email=Uid_Token).values("is_IntelligenceTest")[0]["is_IntelligenceTest"]


            """
            if Is_Intelligenence_Test:
                Dict = {"TestPassed":"Intl"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            """
            if Is_PostStoryTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"PostStory"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_PostWordsTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"PostWords"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_PostSentenceTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"PostSentence"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_PostLetterTest:
                Dict = {"Ud":data["Uid"],"TestPassed":"PostLetters"}
                print(Dict)
                return JsonResponse(Dict,status =201)
            if Is_PostLetterTest == False:
                Dict = {"Ud":data["Uid"],"TestPassed":"PreStory"}
                print(Dict)
                return JsonResponse(Dict,status =201)
        except:
            Dict={"msg":"User not valid"}
            return JsonResponse(Dict,status =404)
    else:
        Dict={"msg":"request is not valid"}
        return JsonResponse(Dict,status =500)




@csrf_exempt
def PosttestletterScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id = Int_Id)
                Data_toSaved = PostTestLettersScore(user = User_Obj, Score = data["Score"] )
                Data_toSaved.save()
                Account.objects.all().filter(id = Int_Id).update(is_PostTestletters = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=500)





@csrf_exempt
def PostSentenceTestScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            #Valid_User = Account.objects.all().filter(UUid_Token = data["Uid"]).values("UUid_Token")[0]["UUid_Token"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id =Int_Id)
                Data_toSaved = PostTestSentencesScore(user = User_Obj, Score = data["Score"] )
                Data_toSaved.save()
                Account.objects.all().filter(id =Int_Id).update(is_PostTestSentences = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=404)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=500)





@csrf_exempt
def PostWordsTestScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            #Valid_User = Account.objects.all().filter(UUid_Token = data["Uid"]).values("UUid_Token")[0]["UUid_Token"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id = Int_Id)
                Data_toSaved = PostWordTestScore(user = User_Obj, Score = data["Score"], TypeofTest = data["Level"] )
                Data_toSaved.save()
                Account.objects.all().filter(id = Int_Id).update(is_PostTestWords = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=500)







@csrf_exempt
def PostTestGetWordsTestScore(request):
    Preprimer = "I am a big boy My name is Sam. I can run. I can play bat and ball. She my bat here. It is red. See my ball here. It is blue."
    Primer = "My name is Tom. I like to eat red apples. I can eat three red apples at once. They are good for me. They are good for you too. Apples make me big and I can run. I can run in the race at school."
    Level1 = "Sam and Pam are friends. They are going home from school. Pam takes the bus four days out of the week. She sings and talks on the bus. Pam gets home early Sam walks home four days out of the week. He likes to walk, run and jump. He gets home late. Mr. White is Sam’s father. He takes the children home from school on Friday. They like to go with him because he takes them to the shop. At the shop he buys sweets and buns for them."
    Level2 = "Sunday is my birthday. I will be seven years old. I plan to have a birthday party on that day. So I tell all my friends to come and take a gift. On Saturday my mother buys a cake, some balloons and ice cream. Before we begin on Sunday my brother, sister, and I set up for my party in a room. We blow the balloons and fix up the place. All my friends and family came. My friends came from school and church. When my party began, we ate, sang and danced. Everyone enjoyed the birthday party."
    Level3 = "Trees and other plants are very important to us. So let us all take care of them. We should not cut down those that we already have, because they are very useful. They provide us with oxygen, food and shade. These help us to stay alive and be safe. Others are used to beautify a place. Therefore, plants that are cut down should be replaced. If there is an area without trees, we should also begin to plant new ones and prune them so that they may grow. By doing this, we may be able to grow enough food to provide for the people in our country. If we are able to plant and grow these trees, we may also be able to save our planet earth."
    Level4 = "Going to the market day is a very special occasion in rural areas. For many higglers, preparations begin from the Thursday or Friday before depending on the day they go to the market. Those who leave on Friday, prepare from Thursday and do not return home until Saturday night. The others leave early Saturday morning. The preparations and delivery of the products and service they provide includes very hard work. Firstly, they have to arise very early in the morning before the sun rises to go to their farmland or to the bush. Several of them have to walk long distances because their farms are far away and they do not own a donkey or other means of transportation. When they get to their farm, they begin the reaping. The yams, potatoes, carrots ground provisions have to be dug from the ground, dirt removed and the item washed. Oranges, along with other fruits and vegetables that grow on trees must be picked and gathered. Finally, when they have finished gathering, those who have transportations or donkeys will load them up with the produce and head home. Those who don’t have transportations or donkeys will have to make several trips with their load in hand or on their heads. At home, the products are further grouped and the sellers wait for the market truck or bus to be able to ply their wares to customers or other vendors."
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            #Valid_User = Account.objects.all().filter(UUid_Token = data["Uid"]).values("id")[0]["id"]
            if Valid_User is not None:
                Scores = PostWordTestScore.objects.all().filter(user = Valid_User).values("Score").last()['Score']
                TestType = PostWordTestScore.objects.all().filter(user = Valid_User).values("TypeofTest").last()['TypeofTest']
                print(Scores)
                Score=int(Scores)

                #Pre-Premier stories
                if TestType == "Preprimer":
                    if Score<8:
                        Dict ={"DataList":Preprimer,"type":"Preprimer"}
                        return JsonResponse(Dict,status=201)
                    if Score>=8:
                        Dict ={"DataList":Primer,"type":"Primer"}
                        return JsonResponse(Dict,status=201)

                #Premier Stories
                if TestType == "Primer":
                    if Score<8:
                        Dict ={"DataList":Preprimer,"type":"Preprimer"}
                        return JsonResponse(Dict,status=201)
                    if Score>=8:
                        Dict ={"DataList":Primer,"type":"Primer"}
                        return JsonResponse(Dict,status=201)

                #Level1 stories
                if TestType == "Level1":
                    if Score<12:
                        Dict ={"DataList":Primer,"type":"Primer"}
                        return JsonResponse(Dict,status=201)
                    if Score>=12:
                        Dict ={"DataList":Level1,"type":"Level1"}
                        return JsonResponse(Dict,status=201)

                #Level 2 Stories
                if TestType == "Level2":
                    if Score<12:
                        Dict ={"DataList":Level1,"type":"Level1"}
                        return JsonResponse(Dict,status=201)
                    if Score>=12:
                        Dict ={"DataList":Level2,"type":"Level2"}
                        return JsonResponse(Dict,status=201)

                #Level3 Stories
                if TestType == "Level3":
                    if Score<12:
                        Dict ={"DataList":Level2,"type":"Level2"}
                        return JsonResponse(Dict,status=201)
                    if Score>=12:
                        Dict ={"DataList":Level3,"type":"Level3"}
                        return JsonResponse(Dict,status=201)

                #Level4 Stories
                if TestType=="Level4":
                    if Score<15:
                        Dict ={"DataList":Level3,"type":"Level3"}
                        return JsonResponse(Dict,status=201)
                    if Score>=15:
                        Dict ={"DataList":Level4,"type":"Level4"}
                        return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=400)





@csrf_exempt
def PostSetStoryTestScore(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            Valid_User = Account.objects.all().filter(id = Int_Id).values("id")[0]["id"]
            #Valid_User = Account.objects.all().filter(UUid_Token = data["Uid"]).values("UUid_Token")[0]["UUid_Token"]
            if Valid_User is not None:
                User_Obj = Account.objects.get(id = Int_Id)
                Data_toSaved = PostStorytestScore(user = User_Obj, Score = data["Score"], TypeofTest = data["Level"], Numberof_MissingWords = data["Missing"] )
                Data_toSaved.save()
                Account.objects.all().filter(id = Int_Id).update(is_PostTestStories = True)
                Dict ={"Ud":data["Uid"]}
                return JsonResponse(Dict,status=201)
        except:
            Dict ={"Ud":"Not a valid user"}
            return JsonResponse(Dict,status=400)
    else:
        Dict ={"Ud":"Not a valid request"}
        return JsonResponse(Dict,status=500)






@csrf_exempt
def PostCompareStories(request):
    Preprimer = "I am a big boy My name is Sam I can run I can play bat and ball She my bat here It is red See my ball here It is blue"
    Primer = "My name is Tom I like to eat red apples I can eat three red apples at once They are good for me They are good for you too"
    Level1 = "Sam and Pam are friends They are going home from school Pam takes the bus four days out of the week She sings and talks on the bus Pam gets home early Sam walks home four days out of the week He likes to walk run and jump He gets home late Mr. White is Sam's father He takes the children home from school on Friday They like to go with him because he takes them to the shop At the shop he buys sweets and buns for them"
    Level2 = "My birthday Sunday is my birthday I will be seven years old I plan to have a birthday party on that day So I tell all my friends to come and take a gift On Saturday my mother buys a cake, some balloons and ice cream Before we begin on Sunday my brother sister and I set up for my party in a room We blow the balloons and fix up the place All my friends and family came My friends came from school and church When my party began we ate sang and danced Everyone enjoyed the birthday party"
    Level3 = "Trees and other plants are very important to us So let us all take care of them We should not cut down on those that we already have because they are very useful They provide us with oxygen food and shade These help us to stay alive and be safe Others are used to beautify a place Therefore plants that are cut down should be replaced If there is an area without trees we should also begin to plant new ones and prune them so that they may grow By doing this we may be able to grow enough food to provide for the people in our country If we are able to plant and grow these trees we may also be able to save our planet earth"
    Level4 = "Going to the market day is a very special occasion in rural areas For many higglers preparations begin from the Thursday or Friday before depending on the day they go to the market Those who leave on Friday prepare from Thursday and do not return home until Saturday night The others leave early Saturday morning The preparations and delivery of the products and service they provide include very hard work Firstly they have to arise very early in the morning before the sun rises to go to their farmland or to the bush Several of them have to walk long distances because their farms are far away and they do not own a donkey or other means of transportation When they get to their farm they begin the reaping The yams potatoes carrots ground provisions have to be dug from the ground dirt removed and the item washed Oranges along with other fruits and vegetables that grow on trees must be picked and gathered Finally when they have finished gathering those who have transportations or donkeys will load them up with the produce and head home Those who don't have transportations or donkeys will have to make several trips with their load in hand or on their heads At home the products are further grouped and the sellers wait for the market truck or bus to be able to ply their wares to customers or other vendors"
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            Dict = {}
            Type = data["type"]
            Value = data["story"]
            List_Response = {}
            #PrePrimer
            if Type=="Preprimer":
                List_Of_Dict = []
                List_of_Quistions = PostTestStoryQuestions.objects.all().filter(TestType ="Preprimer" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Preprimer.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)

            #Level1
            if Type=="Level1":
                List_Of_Dict = []
                List_of_Quistions =  PostTestStoryQuestions.objects.all().filter(TestType ="Level1" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level1.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)

            #Level2
            if Type=="Level2":
                List_Of_Dict = []
                List_of_Quistions =  PostTestStoryQuestions.objects.all().filter(TestType ="Level2" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level2.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
            #Level3
            if Type=="Level3":
                List_Of_Dict = []
                List_of_Quistions =  PostTestStoryQuestions.objects.all().filter(TestType ="Level3" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level3.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
            #Level4
            if Type=="Level4":
                List_Of_Dict = []
                List_of_Quistions =  PostTestStoryQuestions.objects.all().filter(TestType ="Level4" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Level4.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)

            #Primer
            if Type=="Primer":
                List_Of_Dict = []
                List_of_Quistions =  PostTestStoryQuestions.objects.all().filter(TestType ="Primer" ).values("Questions","Answer","Answer2","Answer3","Answer4")
                for x in List_of_Quistions:
                    List_Of_Dict.append(x)
                Split1 = str(Value).split(" ")
                Split2 = Primer.split(" ")
                Diffrence_Of_Sentences = list(set(Split2) - set(Split1))
                if len(Diffrence_Of_Sentences)>0:
                    Dict["Unmatched"] = Diffrence_Of_Sentences
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
                else:
                    Dict["Unmatched"] = "None"
                    List_Response["Unmathched_List"] = Dict
                    List_Response["Questions_List"] = List_Of_Dict
                    print(List_Response)
                    return JsonResponse(List_Response,safe=False,status=201)
        else:
            dictError = {"Unmatched":"Not Valid Data"}
            return JsonResponse(dictError,status=401)
    else:
        dictError = {"Unmatched":"Not Valid Request"}
        return JsonResponse(dictError,status=500)






@csrf_exempt
def PretestResults(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            RespData = AccountAuth.GetPretestResults(Uid =Int_Id )
            if RespData is not None:
                return JsonResponse(RespData,safe=False,status=201)
            else:
                RespData= {"Msg":"Somthing Went wrong"}
                return JsonResponse(RespData,safe=False,status=400)
        else:
            RespData= {"Msg":"Data not Recieved"}
            return JsonResponse(RespData,safe=False,status=500)
    else:
        RespData= {"Msg":"Invalid Request"}
        return JsonResponse(RespData,safe=False,status=500)




@csrf_exempt
def PosttestResults(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            Splitstr = str(data["Uid"]).split("_")
            Int_Id = int(Splitstr[1])
            RespData = AccountAuth.GetPosttestResults(Uid = Int_Id)
            if RespData is not None:
                return JsonResponse(RespData,safe=False,status=201)
            else:
                RespData= {"Msg":"Somthing Went wrong"}
                return JsonResponse(RespData,safe=False,status=400)
        else:
            RespData= {"Msg":"Data not Recieved"}
            return JsonResponse(RespData,safe=False,status=500)
    else:
        RespData= {"Msg":"Invalid Request"}
        return JsonResponse(RespData,safe=False,status=500)




def GetAllStudentsData(request):
    data={}
    try:
        StudentsList = Account.objects.all().values("username","email","is_email_varified")
        Dict=[]
        for i in StudentsList:
            Dict.append(i)
        data["data"] = Dict
        return JsonResponse(data,safe=False,status=200)
    except:
        data["data"] = "Somthing went wrong"
        return JsonResponse(data,safe=False,status=403)



@csrf_exempt
def GetPreTestData(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            try:
                Id = Account.objects.all().filter(email= data["email"]).values("id")
                RespData = AccountAuth.GetPretestResults(Uid =Id )
                return JsonResponse(RespData,safe=False,status=201)
            except:
                RespData = None
                return JsonResponse(RespData,safe=False,status=404)
        else:
            RespData= {"Msg":"Data not Recieved"}
            return JsonResponse(RespData,safe=False,status=403)
    else:
        RespData= {"Msg":"Invalid Request"}
        return JsonResponse(RespData,safe=False,status=500)


@csrf_exempt
def GetPostTestData(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            try:
                Id = Account.objects.all().filter(email= data["email"]).values("id")
                RespData = AccountAuth.GetPosttestResults(Uid =Id )
                return JsonResponse(RespData,safe=False,status=201)
            except:
                RespData = None
                return JsonResponse(RespData,safe=False,status=404)
        else:
            RespData= {"Msg":"Data not Recieved"}
            return JsonResponse(RespData,safe=False,status=403)
    else:
        RespData= {"Msg":"Invalid Request"}
        return JsonResponse(RespData,safe=False,status=500)


@csrf_exempt
def GetInventoryTestData(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            try:
                Id = Account.objects.all().filter(email= data["email"]).values("id")
                RespData = InventoryTestScore.objects.filter(user = Id).values("Score")
                return JsonResponse(RespData,safe=False,status=201)
            except:
                RespData = None
                return JsonResponse(RespData,safe=False,status=404)
        else:
            RespData= {"Msg":"Data not Recieved"}
            return JsonResponse(RespData,safe=False,status=403)
    else:
        RespData= {"Msg":"Invalid Request"}
        return JsonResponse(RespData,safe=False,status=500)


@csrf_exempt
def GetInterestTestData(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            try:
                Id = Account.objects.all().filter(email= data["email"]).values("id")
                RespData = IntelligenceTestScore.objects.filter(user = Id).values("Linguistic","Logical","Musical","Spatial","Bodily","Intra","Inter","TopScoreSection")
                return JsonResponse(RespData,safe=False,status=201)
            except:
                RespData = None
                return JsonResponse(RespData,safe=False,status=404)
        else:
            RespData= {"Msg":"Data not Recieved"}
            return JsonResponse(RespData,safe=False,status=403)
    else:
        RespData= {"Msg":"Invalid Request"}
        return JsonResponse(RespData,safe=False,status=500)


def GetPretestLettersData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = LettersTest.objects.all().filter(user = j ).values("Score").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['Score'])
                emaillist.append(EmailId)
        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)

def GetPretestSentencesData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = SentencesTest.objects.all().filter(user = j ).values("Score").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['Score'])
                emaillist.append(EmailId)

        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)

def GetPretestWordsData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = WordTest.objects.all().filter(user = j ).values("Score").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['Score'])
                emaillist.append(EmailId)
        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
        #return JsonResponse(data,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)


def GetPretestStoryData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        MissingWordCount = []
        emaillist = []
        for j in range(len(ListId)):
            Ltrsobj = Storytest.objects.all().filter(user = ListId[j] ).values("Score","Numberof_MissingWords").last()
            EmailId = Account.objects.all().filter(id = ListId[j]).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj["Score"])
                MissingWordCount.append(Ltrsobj['Numberof_MissingWords'])
                emaillist.append(EmailId)

        for k in range(len(ScorList)):
                data={"email":emaillist[k],"Scorelist":ScorList[k],"missing":MissingWordCount[k]}
                Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)

    #return JsonResponse(data,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)



def GetPosttestLettersData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = PostTestLettersScore.objects.all().filter(user = j ).values("Score").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['Score'])
                emaillist.append(EmailId)
        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)


def GetPosttestSentencesData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = PostTestSentencesScore.objects.all().filter(user = j ).values("Score").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['Score'])
                emaillist.append(EmailId)
        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)


def GetPosttestWordsData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = PostWordTestScore.objects.all().filter(user = j ).values("Score").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['Score'])
                emaillist.append(EmailId)
        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)


def GetPosttestStoryData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        MissingWordCount = []
        emaillist = []
        for j in range(len(ListId)):
            Ltrsobj = PostStorytestScore.objects.all().filter(user = ListId[j] ).values("Score","Numberof_MissingWords").last()
            EmailId = Account.objects.all().filter(id = ListId[j]).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj["Score"])
                MissingWordCount.append(Ltrsobj['Numberof_MissingWords'])
                emaillist.append(EmailId)

        for k in range(len(ScorList)):
                data={"email":emaillist[k],"Scorelist":ScorList[k],"missing":MissingWordCount[k]}
                Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)

    #return JsonResponse(data,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)



def GetInteligencesData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = IntelligenceTestScore.objects.all().filter(user = j ).values("TopScoreSection").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['TopScoreSection'])
                emaillist.append(EmailId)
        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)



def GetInventoryData(request):
    data= {}
    Lists = []
    try:
        Accounts = Account.objects.all().values("id")
        ListId = []
        for i in Accounts:
            ListId.append(i['id'])
        ScorList = []
        emaillist = []
        for j in ListId:
            Ltrsobj = InventoryTestScore.objects.all().filter(user = j ).values("Score").last()
            EmailId = Account.objects.all().filter(id = j).values("email")[0]["email"]
            if Ltrsobj != None:
                ScorList.append(Ltrsobj['Score'])
                emaillist.append(EmailId)
        for k in range(len(ScorList)):
            data={"email":emaillist[k],"Scorelist":ScorList[k]}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(data,safe=False,status=400)



def GetAllStudentData(request):
    data ={}
    Lists = []
    try:
        AccountDetails = Account.objects.all().values("id","email","username","date_joined","UUid_Token","is_active")
        for i in AccountDetails:
            Uuid_Str = str(i["UUid_Token"])
            token = "{}_{}_{}".format(Uuid_Str,i["id"],i["username"])
            date_time = i["date_joined"].strftime("%m/%d/%Y, %H:%M:%S")
            datesplt = date_time.split(",",2)
            if i["is_active"] == True:
                Active= "Yes"
            else:
                Active= "No"
            data={"email":i["email"], "username":i["username"],"date":datesplt[0],"token":token,"active":Active}
            Lists.append(data)
        return JsonResponse(Lists,safe=False,status=200)
    except:
        return JsonResponse(Lists,safe=False,status=400)


@csrf_exempt
def ConvertAudioandSpeechtoText(request):
    Dict = {}
    if request.method == "POST":
        data = request.data
        if data != None:
            Dict= {"data":"Received"}
            return JsonResponse(Dict,safe=False,status=200)
        else:
            Dict= {"data":"Not Received"}
            return JsonResponse(Dict,safe=False,status=400)
    else:
        Dict= {"data":"Not Valid Request"}
        return JsonResponse(Dict,safe=False,status=403)




