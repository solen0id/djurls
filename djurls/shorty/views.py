from rest_framework.generics import ListCreateAPIView
from shorty.filters import IsAuthenticatedUserFilterBackend
from shorty.models import ShortURL
from shorty.serializers import ShortURLSerializer


class ShortURLListCreateAPI(ListCreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    filter_backends = [IsAuthenticatedUserFilterBackend]
