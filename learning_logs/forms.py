from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        # 表单包含的字段
        fields = ['topic']
        # 不要为字段生成标签
        labels = {'topic': '主题'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['topic', 'title', 'link', 'text', ]
        labels = {'topic': '主题', 'title': '标题', 'link': '链接', 'text': '内容'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
