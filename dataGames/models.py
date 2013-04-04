from django.db import models
from django.contrib.auth.models import User
from games.models import Games
from words.models import Words

# Create your models here.

class DataGames(models.Model):
	gameId = models.ForeignKey(Games)
	word = models.ForeignKey(Words)
	playerFrom = models.ForeignKey(User, related_name='playerFrom')
	playerTo = models.OneToOneField(User, related_name='playerTo')
	def __unicode__(self):
		return u'%s %s->%s' % (self.word.word, self.playerFrom.first_name, self.playerTo.first_name)