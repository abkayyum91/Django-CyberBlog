from django import forms
from django.core.exceptions import ValidationError
from home.models import ContactModel


# Contact Form
class ContactForm(forms.ModelForm):
    subject = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Query Heading...'}))

    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'subject', 'query']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name..'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your E-mail..'}),
            'query': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Explain Query Here...', 'rows': '5'}),
        }

    # Applying django form cleaning using clean_<field_name>
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) <= 3:
            raise ValidationError('Name is too short!')
        else:
            return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '.' not in email:
            raise ValidationError("Missing '.' symbol in email! ")
        elif '@' not in email:
            raise ValidationError("Missing '@' symbol in email! ")
        else:
            return email

    def clean_subject(self, *args, **kwargs):
        abuse = ['fake', 'spam', 'idiot', 'theif']
        subject = self.cleaned_data.get('subject')
        for ww in abuse:
            if ww in subject:
                raise ValidationError("Heading containing abusive words")
            else:
                return subject

    def clean_query(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        if  len(query) <= 50:
            raise ValidationError("Your query should be minimum 50 character.")
        else:
            return query