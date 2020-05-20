from rest_framework import mixins, viewsets
from core.models import Tag, Ingredient
from recipe import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BaseReciepeAttrViewset(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    """Base class for further model viewsets"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """override existing queryset"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """perform the object creation and save"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseReciepeAttrViewset):
    """Manage the tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseReciepeAttrViewset):
    """Manage the ingredient for recipe in the database."""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
