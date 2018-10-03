from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from categories.models import Group, Element


class ElementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'group', 'icon', 'name', 'description')

    def create(self, validated_data):
        group_id = self.context['view'].kwargs['id']
        group = Group.objects.get(id=group_id)
        validated_data.update({'group': group})
        element = Element.objects.create(**validated_data)
        return element


class ElementsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Element
        fields = ('id', 'icon', 'name', 'description')


class GroupSerializer(serializers.ModelSerializer):
    subgroups_count = serializers.IntegerField(source='get_childs_count', read_only=True)
    elements_count = serializers.IntegerField(source='get_elements_count', read_only=True)
    elements = ElementsListSerializer(many=True, source='get_elements')
    subgroups = serializers.ListSerializer(source="childs", child=RecursiveField())

    class Meta:
        model = Group
        fields = ('id', 'icon', 'name', 'description', 'elements_count', 'elements', 'subgroups_count', 'subgroups')
