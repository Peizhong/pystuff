from django.db import models

# Create your models here.


class Podcast(models.Model):
    PODCAST_STATUS = (
        (0, 'None'),
        (1, 'WillDownload'),
        (2, 'Downloading'),
        (3, 'Downloaded'),
        (4, 'Error'),
        (5, 'Deleted'),
    )
    Title = models.CharField(max_length=200)
    Summary = models.CharField(max_length=2048)
    Link = models.CharField(max_length=200)
    PublishDate = models.DateTimeField('date published')
    Status = models.IntegerField(default=0, choices=PODCAST_STATUS)
    Location = models.CharField(max_length=200, null=True, blank=True)
    Remark = models.CharField(max_length=2048, null=True, blank=True)
