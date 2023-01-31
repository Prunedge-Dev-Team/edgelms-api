from django_filters import rest_framework as df_filters
from .models import Professional


class ProfessionFilter(df_filters.FilterSet):
    search = df_filters.CharFilter(method='filter_search')
    
    
    @staticmethod
    def filter_search(queryset, name, value):
        return queryset.filter(name__icontains=value)
    
    class Meta:
        model = Professional
        fields = ['name']
