"""Author model for Zinnia"""
from django.db import models
from django.contrib.auth.models import User

from zinnia.managers import entries_published
from zinnia.managers import AuthorPublishedManager
from zinnia.settings import UPLOAD_TO

from stdimage import StdImageField

try:
    from south.modelsinspector import add_introspection_rules

    rules = [((StdImageField,), [],
                  {'size': ['size', {"default": None}],
                   'thumbnail_size': ['thumbnail_size', {"default": None}],
                   'upload_to': ['upload_to', {"default": ""}],
                   })]
    add_introspection_rules(rules, ["^stdimage\.fields.\StdImageField"])
except ImportError:
    pass


class Author(User):
    """Proxy model around :class:`django.contrib.auth.models.User`"""

    objects = models.Manager()
    published = AuthorPublishedManager()

    def entries_published(self):
        """Return only the entries published"""
        return entries_published(self.entries)

    def __unicode__(self):
        if self.first_name and self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        return self.username

    @models.permalink
    def get_absolute_url(self):
        """Return author's URL"""
        return ('zinnia_author_detail', (self.username,))

    class Meta:
        """Author's Meta"""
        app_label = 'zinnia'
        proxy = True

class AuthorProfile(models.Model):
    author = models.ForeignKey(Author, unique=True)
    about_text = models.TextField(null=True, blank=True)
    photo = StdImageField(upload_to=UPLOAD_TO, size=(1024, 1024),thumbnail_size=(150, 150), null=True, blank=True)

    def __unicode__(self):
        return self.author.get_full_name()

    class Meta:
        app_label = 'zinnia'
Author.author_profile = property(lambda a: AuthorProfile.objects.get_or_create(author=a)[0])