import django_filters
from .models import Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    year = django_filters.NumberFilter()
    genre = django_filters.CharFilter(field_name="genre__slug", lookup_expr="exact")
    category = django_filters.CharFilter(
        field_name="category__slug", lookup_expr="exact"
    )

    class Meta:
        model = Title
        fields = [
            "year",
            "name",
            "genre",
            "category",
        ]
