from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Group, Element


# admin.site.register(Group, MPTTModelAdmin)
@admin.register(Group)
class GroupAdmin(MPTTModelAdmin):
    readonly_fields = ('childs', 'elements')
    mptt_level_indent = 20

    def childs(self, instance):
        return instance.get_childs_count

    def elements(self, instance):
        return instance.get_elements_count


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    pass
