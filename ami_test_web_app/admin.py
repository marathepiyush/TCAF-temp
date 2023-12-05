from django.contrib import admin
from .models import Dimensions, Categories, Questions, UserInfo, UserCategories, UserResponse, \
    Project, Org, ProjectOrgChoices, InitiativeTraceability, InitiativeDetail, FinalInitiatives, \
    UploadedFile
# Register your models here.

admin.site.register(Dimensions)
admin.site.register(Categories)
admin.site.register(Questions)
admin.site.register(UserInfo)
admin.site.register(UserCategories)
admin.site.register(UserResponse)
admin.site.register(Org)
admin.site.register(Project)
admin.site.register(ProjectOrgChoices)
admin.site.register(InitiativeTraceability)
admin.site.register(InitiativeDetail)
admin.site.register(FinalInitiatives)
admin.site.register(UploadedFile)