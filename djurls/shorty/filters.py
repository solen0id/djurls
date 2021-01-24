from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request
from rest_framework.views import View


class IsAuthenticatedUserFilterBackend(BaseFilterBackend):
    """
    Filters a queryset based on the user making the request.

    """

    def filter_queryset(
        self, request: Request, queryset: QuerySet, view: View
    ) -> QuerySet:
        if request.user.is_authenticated:
            return queryset.filter(author=request.user)
        else:
            return queryset.none()
