from django.db import models
from django.contrib.auth.models import User

from words.models import Words
# Create your models here.


class Games(models.Model):
	name = models.CharField(max_length = 100)
	words = models.ManyToManyField(Words)
	players = models.ManyToManyField(User)
	def __unicode__(self):
		return u'%s' % (self.name)	