from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Group(MPTTModel):
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            related_name='childs',
                            null=True,
                            blank=True,
                            db_index=True)
    icon = models.ImageField(upload_to='categories/groups')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True, blank=True)

    @property
    def get_childs_count(self):
        return self.childs.count()

    @property
    def get_elements_count(self):
        return self.elements.count()

    @property
    def get_elements(self):
        return self.elements.filter(moderated=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'Group: {self.name}'


class Element(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True, related_name='elements')
    icon = models.ImageField(upload_to='categories/elements')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    moderated = models.BooleanField(null=True, blank=True, default=None)

    def __str__(self):
        return f'Element {self.name} of Group {self.group.name}'

