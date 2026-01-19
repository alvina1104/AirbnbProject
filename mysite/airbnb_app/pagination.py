from rest_framework.pagination import PageNumberPagination


class PropertyPagination(PageNumberPagination):
    page_size = 5

class CityPagination(PageNumberPagination):
    page_size = 7