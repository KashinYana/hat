from django.contrib import admin
from game.models import Game, Word, ReportGame, UserWord

admin.site.register(Game)
admin.site.register(Word)
admin.site.register(ReportGame)
admin.site.register(UserWord)


