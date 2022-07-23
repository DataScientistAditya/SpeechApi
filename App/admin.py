from django.contrib import admin

from App.models import Account
from .models import Account,SentencesTest,WordTest,LettersTest,Questions,Storytest,IntelligenceTest,IntelligenceTestScore,InventoryTest,InventoryTestScore,PostTestLettersScore,PostTestSentencesScore,PostWordTestScore,PostTestStoryQuestions,PostStorytestScore
# Register your models here.
admin.site.register(Account)
admin.site.register(SentencesTest)
admin.site.register(WordTest)
admin.site.register(LettersTest)
admin.site.register(Questions)
admin.site.register(Storytest)
admin.site.register(IntelligenceTest)
admin.site.register(IntelligenceTestScore)
admin.site.register(InventoryTest)
admin.site.register(InventoryTestScore)
admin.site.register(PostTestLettersScore)
admin.site.register(PostTestSentencesScore)
admin.site.register(PostStorytestScore)
admin.site.register(PostTestStoryQuestions)
admin.site.register(PostWordTestScore)