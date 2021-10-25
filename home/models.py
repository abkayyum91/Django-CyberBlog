from django.db import models
from django.contrib.humanize.templatetags import humanize
# Create your models here.


# Contact Model
class ContactModel(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    query = models.CharField(max_length=700)
    date = models.DateTimeField(auto_now_add=True)

    def get_date(self):
        return humanize.naturaltime(self.date)

    def query_snipet(self):
        return self.query[:30] + '...'

    def subject_snipet(self):
        return self.subject[:20] + '...'



# Customers email
class newslater(models.Model):
    email = models.EmailField(max_length=150)
    date = models.DateField(auto_now_add=True)

    def get_date(self):
        return humanize.naturalday(self.date)