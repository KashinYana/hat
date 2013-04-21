from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
	name = models.CharField(max_length = 100)
	password = models.IntegerField()
	creator = models.ForeignKey(User, related_name='creator')
	user = models.ManyToManyField(User, related_name='user')
	def __unicode__(self):
		return u'%s' % (self.name)	

class Word(models.Model):
	word = models.CharField(max_length = 100)
	user = models.ManyToManyField(User, through='UserWord')
	
	def __unicode__(self):
		return u'%s' % (self.word)	

class UserWord(models.Model):
	user = models.ForeignKey(User)
	word = models.ForeignKey(Word)
	game = models.ManyToManyField(Game)
	
	def allow_delete(self):
		if len(self.game.all()) == 0:
			if len(self.word.user.all()) <= 1:
				return True
		return False

	def __unicode__(self):
		return u'%s %s' % (self.user.first_name, self.word.word)

class ReportGame(models.Model):
	gameId = models.ForeignKey(Game)
	userFrom = models.ForeignKey(User, related_name='userFrom')
	userTo = models.ForeignKey(User, related_name='userTo')
	word = models.ForeignKey(UserWord)
	outcome = models.IntegerField()
	duration = models.IntegerField()
	tour = models.IntegerField()
	def __unicode__(self):
		return u'%s %s->%s' % (self.word.word, self.userFrom.first_name, self.userTo.first_name)


