from django.core.management.base import BaseCommand
from panfeed.models import AcademicFeeds, Corpus
from corpus import Corpus as CorpusScraper

import feedparser
import urllib2
import datetime

class Command(BaseCommand):

    help = 'Grabs new items from feeds in the database.'

    def handle(self, *args, **options):
        corp = corpus_obj()
        corp.build_corpus()

class corpus_obj(CorpusScraper):
    
    def build_corpus(self):
        #### Builds a corpus of documents from a set of feeds.
    
        #c.execute("""SELECT url,toplevel FROM feeds""")
        feeds = AcademicFeeds.objects.all().values_list('url', flat=True)
        for feedurl in feeds:
            print feedurl
            try:
                page = urllib2.urlopen(feedurl)
                feed = feedparser.parse(page)
                for item in feed.entries:
                    if (Corpus.objects.filter(url=item.link).filter(feed=feedurl).count()==0):
                        try:
                            d = datetime.datetime(*(item.date_parsed[0:6]))
                        except AttributeError:
                            d=datetime.datetime.now()
                        print item.title+" "+item.link
                        Corpus.objects.create(title=item.title,description=item.description,url=item.link,feed=feedurl,length=len(item.description+item.title),date=d,toplevel=feedurl.toplevel)
            except urllib2.URLError:
                print "Error getting page: ", feedurl
