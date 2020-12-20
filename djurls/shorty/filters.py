from rest_framework.filters import BaseFilterBackend


class IsAuthenticatedUserFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            return queryset.filter(author=request.user)
        else:
            return queryset.none()
