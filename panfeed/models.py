# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from django_extensions.db.fields import AutoSlugField

import urllib
import hashlib

class Domains(models.Model):
    toplevel = models.URLField(max_length=255) #https://tools.ietf.org/html/rfc3986
    
    def __unicode__(self):
        return self.toplevel

class AcademicFeeds(models.Model):
    url = models.URLField(unique=True)
    toplevel = models.URLField(max_length=255) #https://tools.ietf.org/html/rfc3986
    etag = models.CharField(max_length=255, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.url;

class Corpus(TimeStampedModel, TitleSlugDescriptionModel):
    feed = models.ForeignKey(AcademicFeeds)
    url = models.URLField(max_length=6249)
    date = models.DateTimeField()
        
    def __unicode__(self):
        return self.title
        
    class Meta:
        #unique_together = ("url", "feed") #Currently bugged to cause too large values
        verbose_name_plural = "corpora"

class SpiderToDo(models.Model):
    pageurl=models.URLField(primary_key=True,max_length=255)

class SpiderDone(models.Model):
    doneurl=models.URLField(primary_key=True,max_length=255)

class SpiderRSS(models.Model):
    rssurl=models.URLField(primary_key=True,max_length=255)

class Feed(TimeStampedModel):
    owner = models.ForeignKey(User) 
    title = models.CharField('feed title', max_length=120, help_text='Try to keep your title brief but informative (e.g. "Student Project News")')
    slug = AutoSlugField(_('slug'), populate_from='title')
    description = models.TextField('feed description', help_text='Briefly describe the purpose of this feed (e.g. "Information for students working on their Third Year Project")')
    displayAll = models.BooleanField('publishing options', default=True, help_text='Don\'t worry, you can change this later if you change your mind') #True=display all items, False=only display latest publication
    
    def get_fragment_id(self):
        return "feed-{feed_id}".format(feed_id=self.id)
    
    @models.permalink
    def get_absolute_url(self):
        return ("viewfeed", [str(self.slug)])
        
    @models.permalink
    def get_modify_url(self):
        return ("managefeed", [str(self.slug)])
        
    def __unicode__(self):
        return self.title

class SpecialIssue(TimeStampedModel):
    title = models.CharField(max_length=120)
    slug = AutoSlugField(_('slug'), populate_from='title')
    description = models.TextField()
    feed = models.ForeignKey(Feed)

    @models.permalink
    def get_modify_url(self):
        return ("manageissue", (self.feed.slug, self.slug))

class FeedItem(TimeStampedModel):
    title = models.CharField(max_length=120)
    slug = AutoSlugField(_('slug'), populate_from='title')
    description = models.TextField(help_text='This content will be displayed in the viewer\'s Feed Reader. They can still click the link to view the full article')
    url = models.URLField("URL", max_length=6249, blank=True)
    image = models.URLField("image", max_length=6249, blank=True)
    feed = models.ForeignKey(Feed)
    special_issue = models.ForeignKey(SpecialIssue, null=True, blank=True)
    issue_position = models.IntegerField(null=True, db_index=True, blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ("manageitem", (self.feed.slug, self.slug))

    @models.permalink
    def get_modify_url(self):
        return ("manageitem", (self.feed.slug, self.slug))
            
    def __unicode__(self):
        return self.title
        
class UserProfile(TimeStampedModel, TitleSlugDescriptionModel):
    user = models.OneToOneField(User, editable=False)
    gravatar_hash = models.CharField(max_length=32, editable=False)
        
    #https://en.gravatar.com/site/implement/images/python/
    def gravatar_url(self, size=80):
        gravatar_url = "https://secure.gravatar.com/avatar/" + self.gravatar_hash + "?"
        gravatar_url += urllib.urlencode({'d':"retro", 's':str(size)})
        return gravatar_url
    
    def big_gravatar_url(self):
        return self.gravatar_url(size=256)
    
    def __unicode__(self):
        return "{title}({email})".format(
            nickname = self.title,
            email = self.user.email
        )
    
    @models.permalink
    def get_absolute_url(self):
        return('profile', (), {"slug" : self.slug})

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user = instance,
            title = instance.email.rsplit("@",1)[0][:30],
            gravatar_hash = hashlib.md5(instance.email.lstrip().lower()).hexdigest()
        )

signals.post_save.connect(create_user_profile, sender=User)
