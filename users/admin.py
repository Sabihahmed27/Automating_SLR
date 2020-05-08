from django.contrib import admin
from .models import Profile
from .models import Articles,DatabaseSearch_Datatable

# Register your models here.
admin.site.register(Profile)
admin.site.register(Articles)
admin.site.register(DatabaseSearch_Datatable)