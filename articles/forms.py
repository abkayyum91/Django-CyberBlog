from django import forms
from django.forms import fields, widgets
from articles.models import postComment, Post
from django.core.exceptions import ValidationError


restricted_word = ['idiot', 'fake', 'spam', 'misuse']

# Form for comments
class postCommentForm(forms.ModelForm):
    class Meta:
        model = postComment
        fields = ['comment']

        widgets = {
            'comment':forms.Textarea(attrs={'class': 'form-control', 'rows': '1', 'placeholder': 'Leave comments...'}),
        }

    # Applying django form cleaning using clean_<field_name>
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        for word in restricted_word:
            if word in comment:
                raise ValidationError('Please write some useful comments?')
        else:
            return comment



# Form for creating new post
class createPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'category', 'poster']

        widgets = {
            'category':forms.Select(attrs={'class':'form-select'})
        }