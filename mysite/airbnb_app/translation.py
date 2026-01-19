from .models import Country,City,Amenity,Property
from modeltranslation.translator import TranslationOptions,register

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(Amenity)
class AmenityTranslationOptions(TranslationOptions):
    fields = ('amenity_name',)

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title','description','address',)
