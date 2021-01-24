from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.request import Request

from djurls.shorty.filters import IsAuthenticatedUserFilterBackend
from djurls.shorty.models import ShortURL
from djurls.shorty.serializers import ShortURLSerializer
from djurls.shorty.utils import decode_custom_base


class ShortURLListCreateAPI(ListCreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    filter_backends = [IsAuthenticatedUserFilterBackend]


class ShortURLRedirectView(RetrieveAPIView):
    queryset = ShortURL.objects.all()

    def get_object(self) -> ShortURL:
        queryset = self.filter_queryset(self.get_queryset())

        short_key = self.kwargs.get("short_key")
        short_url = get_object_or_404(queryset, pk=decode_custom_base(short_key))

        self.check_object_permissions(self.request, short_url)
        return short_url

    def retrieve(self, request: Request, *args, **kwargs) -> HttpResponseRedirect:
        instance = self.get_object()

        # We pass along any query parameters from the request
        url = instance.url
        query_params = urlencode(request.query_params, safe="?&")
        redirect_url = f"{url.rstrip('?')}?{query_params}" if query_params else url

        return HttpResponseRedirect(redirect_url)
