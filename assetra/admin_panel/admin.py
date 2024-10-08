from django.contrib import admin
from .models import User, Referral, Blog, Category, Tag
from django.contrib.sessions.models import Session

# Register your models here.
admin.site.register(User)
admin.site.register(Referral)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date', 'get_decoded_data']

    def get_decoded_data(self, obj):
        return obj.get_decoded()
    get_decoded_data.short_description = 'Session Data'

