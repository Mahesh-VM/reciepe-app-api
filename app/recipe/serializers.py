from rest_framework import serializers
from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """serializer fro the tag"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_ony_fields = ('id',)
