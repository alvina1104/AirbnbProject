from django_filters import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'property_type': ['exact'],
            'city': ['exact'],
            'max_guests': ['exact'],
            'amenity': ['exact'],
            'price': ['gt', 'lt', 'gte', 'lte']

        }
