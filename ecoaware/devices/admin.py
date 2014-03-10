from django.contrib import admin
from .models import Device, CustomUser, TagRFID, FieldActivity, DeviceCategory, DevelopedActivity, Question, User_Question
    
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'category')
    #list_filter = ('category',)
    search_fields = ('name',)
    #filter_horizontal = ('fdactivity',)
    #raw_id_fields = ('category',)
    
class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser
        

class TagRFIDAdmin(admin.ModelAdmin):
    class Meta:
        model = TagRFID

admin.site.register(DevelopedActivity)
admin.site.register(FieldActivity)
admin.site.register(DeviceCategory)
admin.site.register(TagRFID, TagRFIDAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Question)
admin.site.register(User_Question)
