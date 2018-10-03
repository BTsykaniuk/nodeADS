from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import GroupSerializer, ElementCreateSerializer
from categories.models import Group


class GroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.root_nodes()


class ElementCreateAPIView(CreateAPIView):
    serializer_class = ElementCreateSerializer
