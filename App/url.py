from django.urls import path
from . import views


urlpatterns=[
    path("Register", views.Register, name="Register"),
    path("Login", views.Login, name="Login"),
    path("CompareSentences", views.CompareSentences, name="CompareSentences"),
    path("LetterTestScore", views.LetterTestScore,name="LetterTestScore"),
    path("SentenceTestScore", views.SentenceTestScore,name="SentenceTestScore"),
    path("GetSentenceTestScore", views.GetSentenceTestScore,name="GetSentenceTestScore"),
    path("WordsTestScore", views.WordsTestScore,name="WordsTestScore"),
    path("GetWordsTestScore",views.GetWordsTestScore,name="GetWordsTestScore"),
    path("SetStoryTestScore",views.SetStoryTestScore,name="SetStoryTestScore"),
    path("CompareStories",views.CompareStories,name="CompareStories"),
    path("Retake",views.Retake,name="Retake"),
    path("PostTestRetake",views.PostTestRetake,name="PostTestRetake"),
    path("Resetpaswword",views.Resetpaswword,name="Resetpaswword"),
    path("FetchIntelligenceQsn",views.FetchIntelligenceQsn,name="FetchIntelligenceQsn"),
    path("GetIntelligenceResult",views.GetIntelligenceResult,name="GetIntelligenceResult"),
    path("GetInventoryQuestions",views.GetInventoryQuestions,name="GetInventoryQuestions"),
    path("SendInventoryResult",views.SendInventoryResult,name="SendInventoryResult"),
    path("GetCompletedTest",views.GetCompletedTest,name="GetCompletedTest"),
    path("GetCompletedPostTest",views.GetCompletedPostTest,name="GetCompletedPostTest"),
    path("PosttestletterScore",views.PosttestletterScore,name="PosttestletterScore"),
    path("PostSentenceTestScore",views.PostSentenceTestScore,name="PostSentenceTestScore"),
    path("PostWordsTestScore",views.PostWordsTestScore,name="PostWordsTestScore"),
    path("PostSetStoryTestScore",views.PostSetStoryTestScore,name="PostSetStoryTestScore"),
    path("PostTestGetWordsTestScore",views.PostTestGetWordsTestScore,name="PostTestGetWordsTestScore"),
    path("PostCompareStories",views.PostCompareStories,name="PostCompareStories"),
    path("Verify", views.Verify,name="Verify"),
    path("PretestResults",views.PretestResults,name="PretestResults"),
    path("PosttestResults",views.PosttestResults,name="PosttestResults"),
    path("GetAllStudentsData",views.GetAllStudentsData,name="GetAllStudentsData"),
    path("GetPreTestData",views.GetPreTestData,name="GetPreTestData"),
    path("GetPostTestData",views.GetPostTestData,name="GetPostTestData"),
    path("GetInventoryTestData",views.GetInventoryTestData,name="GetInventoryTestData"),
    path("GetInterestTestData",views.GetInterestTestData,name="GetInterestTestData"),
    path("GetPretestLettersData", views.GetPretestLettersData, name = "GetPretestLettersData"),
    path("GetPretestSentencesData", views.GetPretestSentencesData, name = "GetPretestSentencesData"),
    path("GetPretestWordsData", views.GetPretestWordsData, name = "GetPretestWordsData"),
    path("GetPretestStoryData", views.GetPretestStoryData, name = "GetPretestStoryData"),
    path("GetPosttestLettersData", views.GetPosttestLettersData, name = "GetPosttestLettersData"),
    path("GetPosttestSentencesData", views.GetPosttestSentencesData, name = "GetPosttestSentencesData"),
    path("GetPosttestWordsData", views.GetPosttestWordsData, name = "GetPosttestWordsData"),
    path("GetPosttestStoryData", views.GetPosttestStoryData, name = "GetPosttestStoryData"),
    path("GetInteligencesData", views.GetInteligencesData, name = "GetInteligencesData"),
    path("GetInventoryData", views.GetInventoryData, name = "GetInventoryData"),
    path("GetAllStudentData", views.GetAllStudentData, name = "GetAllStudentData"),
    path("ConvertAudioandSpeechtoText", views.ConvertAudioandSpeechtoText, name = "ConvertAudioandSpeechtoText"),

]