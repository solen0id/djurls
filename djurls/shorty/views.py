from rest_framework.generics import ListCreateAPIView

from djurls.shorty.filters import IsAuthenticatedUserFilterBackend
from djurls.shorty.models import ShortURL
from djurls.shorty.serializers import ShortURLSerializer


class ShortURLListCreateAPI(ListCreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    filter_backends = [IsAuthenticatedUserFilterBackend]
