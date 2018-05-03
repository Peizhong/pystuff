from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    topic = models.CharField(max_length=200)
    date_add = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        "储存额外的信息，用entries表示多个条目"
        verbose_name_plural = '主题'

    def __str__(self):
        "模型的简单表示"
        return self.topic


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=1024)
    text = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        "储存额外的信息，用entries表示多个条目"
        verbose_name_plural = '文章'

    def __str__(self):
        "模型的简单表示"
        # self.date_add.strftime('%Y-%m-%d'),
        temp = '%s: %s' % (self.title, self.text)
        if len(temp) > 100:
            return temp[:100]+'...'
        return temp
