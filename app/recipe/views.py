from rest_framework import mixins, viewsets
from core.models import Tag
from recipe import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage the tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """override existing queryset"""
        return self.queryset.filter(user=self.request.user).order_by("-name")
