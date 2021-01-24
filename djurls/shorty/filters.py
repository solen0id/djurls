from rest_framework.filters import BaseFilterBackend


class IsAuthenticatedUserFilterBackend(BaseFilterBackend):
    """
    Filters a queryset based on the user making the request.

    """

    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            return queryset.filter(author=request.user)
        else:
            return queryset.none()
