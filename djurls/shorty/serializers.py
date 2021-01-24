from rest_framework import serializers

from djurls.shorty.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source="author.username", allow_blank=True, read_only=True
    )
    redirect_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = (
            "accessed_at",
            "author",
            "created_at",
            "redirect_url",
            "url",
            "times_accessed",
        )
        read_only_fields = (
            "accessed_at",
            "author",
            "created_at",
            "redirect_url",
            "times_accessed",
        )

    def create(self, validated_data: dict) -> ShortURL:
        request = self.context["request"]

        if request.user.is_authenticated:
            author = request.user
        else:
            author = None

        return ShortURL.objects.create(author=author, **validated_data)

    def get_redirect_url(self, short_url: ShortURL) -> str:
        request = self.context.get("request")
        host = request.get_host()

        return f"{host}/r/{short_url.short_key}"
