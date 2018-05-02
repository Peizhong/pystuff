from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        # 表单包含的字段
        fields = ['topic']
        # 不要为字段生成标签
        labels = {'topic': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['topic', 'title', 'text']
        labels = {'topic': '', 'title': '', 'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
