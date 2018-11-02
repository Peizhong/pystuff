from django.db import models

# Create your models here.


class Podcast(models.Model):
    Title = models.CharField(max_length=200)
    Summary = models.CharField(max_length=500)
    Link = models.CharField(max_length=200)
    PublishDate = models.DateTimeField('date published')
    IsDownloaded = models.BooleanField(default=False)
    DownloadResult = models.CharField(max_length=500, null=True, blank=True)
