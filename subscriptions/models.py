from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Subscription(models.Model):
    Active = 1
    Deactive = 2
    ACTIVE_CHOICES = ((Active, '启用'), (Deactive, '暂停'))
    MEDIA_CHOICES = (
        ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
        ),
        ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
        ),
        ('unknown', 'Unknown'),
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subs_link = models.CharField(max_length=400)
    is_active = models.CharField(
        max_length=2, choices=ACTIVE_CHOICES, default=Active)
    count = models.IntegerField(default=0, editable=False)

    def __repr__(self):
        '%r_%r_%r' % (self.user_id, self.subs_link, self.is_active)
