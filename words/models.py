from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Words(models.Model):
    user = models.ForeignKey(User)
    word = models.CharField(max_length = 100)
    def __unicode__(self):
        return u'word:%s user: %s' % (self.word, self.user.first_name)