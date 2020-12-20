from rest_framework import serializers
from shorty.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = "__all__"
        read_only_fields = ("author", "accessed_at", "created_at", "times_accessed")

    def create(self, validated_data):
        request = self.context["request"]

        if request.user.is_authenticated:
            author = request.user
        else:
            author = None

        return ShortURL.objects.create(author=author, **validated_data)