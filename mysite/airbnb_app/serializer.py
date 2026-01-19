from .models import (Country,UserProfile,City,Amenity,Property,
                     PropertyImage,Booking,Review)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name','username','password','phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name','last_name','user_image','user_role']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','user_image']

class UserProfilePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_image','first_name','last_name','date_registered']

class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','city_name']

class CityPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']

class AmenityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['amenity_image','amenity_name']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    guest = UserProfileReviewSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = Review
        fields = ['guest','rating','comment','created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating']

class PropertyListSerializer(serializers.ModelSerializer):
    property_image = PropertyImageSerializer(many=True,read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_person = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['id','property_type','property_image','title','price','get_avg_rating',]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_person(self, obj):
        return obj.get_count_person()

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'



class CityDetailSerializer(serializers.ModelSerializer):
    city_property = PropertyListSerializer(many=True,read_only=True)
    class Meta:
        model = City
        fields = ['id','city_name','city_property',]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class PropertyDetailSerializer(serializers.ModelSerializer):
    city = CityPropertySerializer()
    country = CountryListSerializer()
    property_images = PropertyImageSerializer(many=True,read_only=True)
    user = UserProfilePropertySerializer(read_only=True)
    property_review= ReviewSerializer(many=True,read_only=True)
    amenity = AmenityListSerializer(many=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    get_avg_rating = serializers.SerializerMethodField()
    get_count_person = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['id','property_type','property_images','title','city','country','address',
                  'price','max_guests','bedrooms','bathrooms','is_active','created_at','user',
                  'amenity','get_avg_rating','get_count_person','description','property_review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_person(self, obj):
        return obj.get_count_person()


