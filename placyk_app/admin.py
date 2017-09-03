from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Quarter, Pground, Child, Parent, Visit, Message

admin.site.register(Quarter)
admin.site.register(Pground)
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(Visit)
admin.site.register(Message)
"""
class ProfileInline(admin.StackedInline):
    model = Parent
    can_delete = False
    verbose_name_plural = 'Parents'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
"""

