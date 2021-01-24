from rest_framework import serializers

from djurls.shorty.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source="author.username", allow_blank=True, read_only=True
    )
    short_key = serializers.CharField(read_only=True)

    class Meta:
        model = ShortURL
        fields = "__all__"
        read_only_fields = (
            "accessed_at",
            "author",
            "created_at",
            "short_key",
            "times_accessed",
        )

    def create(self, validated_data):
        request = self.context["request"]

        if request.user.is_authenticated:
            author = request.user
        else:
            author = None

        return ShortURL.objects.create(author=author, **validated_data)
