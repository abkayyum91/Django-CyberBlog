from django.contrib import admin
from home.models import ContactModel, newslater
# Register your models here.



# customer email for newslater
@admin.register(newslater)
class newslaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'get_date']


# Contact us model
@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject_snipet', 'query_snipet', 'get_date']
    search_fields = ('email', 'name')
    list_filter = ['date']