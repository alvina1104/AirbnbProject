from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class Country(models.Model):
    country_name = models.CharField(max_length=100,unique=True)
    country_image = models.ImageField(upload_to='city_images')

    def __str__(self):
        return self.country_name

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(80)], null=True,
                                           blank=True)
    phone_number = PhoneNumberField()
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    RoleChoices = (
        ('host', 'host'),
        ('guest', 'guest'),
        ('owner', 'owner'))
    user_role = models.CharField(max_length=20, choices=RoleChoices, default='client')
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name},{self.user_role}'


class City(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name


class Amenity(models.Model):
    amenity_image = models.ImageField(upload_to='amenity_images/')
    amenity_name = models.CharField(max_length=50)

    def __str__(self):
        return self.amenity_name

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='city_property')
    address = models.CharField(max_length=100)
    PropertyChoices = (
    ('apartment', 'apartment'),
    ('house', 'house'),
    ('studio', 'studio'),
    ('hostel', 'hostel'))
    property_type = models.CharField(max_length=20, choices=PropertyChoices)
    amenity = models.ManyToManyField(Amenity)
    max_guests = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        reviews = self.property_review.all()
        if reviews.exists():
            return round(sum(i.rating for i in reviews) / reviews.count(), 1)
        return 0

    def get_count_person(self):
        return self.property_review.count()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='property_images')
    property_image = models.ImageField(upload_to='property_images')

    def __str__(self):
        return f'{self.property},{self.property_image}'


class Booking(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='bookings')
    guest = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    StatusChoices = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('cancelled', 'cancelled'))
    status = models.CharField(max_length=20, choices=StatusChoices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property},{self.guest},'

class Review(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='property_review')
    guest = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i))for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.guest},{self.rating}'


