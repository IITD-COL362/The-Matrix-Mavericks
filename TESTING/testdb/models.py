from django.db import models
# Create your models here.
class Currency(models.Model):
    currency_id = models.CharField(max_length=255, primary_key=True)
    inr_conversion = models.FloatField()

class CountryCurrency(models.Model):
    country_name = models.CharField(max_length=255, primary_key=True)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)

class City(models.Model):
    city_id = models.CharField(max_length=255, primary_key=True)
    country_name = models.ForeignKey(CountryCurrency, on_delete=models.CASCADE)

class Rating(models.Model):
    rating = models.FloatField(primary_key=True)
    rating_colour = models.CharField(max_length=11)

class AvgCostForTwo(models.Model):
    high = models.IntegerField()
    low = models.IntegerField()
    price_range = models.CharField(max_length=11, primary_key=True)

class MealTypeDetails(models.Model):
    meal_type_id = models.CharField(max_length=16, primary_key=True)
    meal_type_score = models.IntegerField()

class UserData(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    mail_id = models.CharField(max_length=255)
    phone_number = models.DecimalField(max_digits=10, decimal_places=0)
    birthday = models.DateField()
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    weight = models.IntegerField()
    account_creation_date = models.DateField()

class Restaurant(models.Model):
    restaurant_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    avg_cost_for_two = models.IntegerField()
    has_table_booking = models.CharField(max_length=3)
    has_online_delivery = models.CharField(max_length=3)
    is_delivering_now = models.CharField(max_length=3)
    switch_to_order_menu = models.CharField(max_length=3)
    aggregate_rating = models.FloatField()
    votes = models.IntegerField()

class RestaurantCuisine(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    cuisine_id = models.CharField(max_length=255)

class Food(models.Model):
    food_id = models.IntegerField(primary_key=True)
    food_name = models.CharField(max_length=255)
    cuisine_id = models.CharField(max_length=255)
    calories = models.FloatField()
    fat = models.FloatField()
    carbohydrates = models.FloatField()
    protein = models.FloatField()
    sodium = models.FloatField()
    meal_type_id = models.ForeignKey(MealTypeDetails, on_delete=models.CASCADE)
    veg_non_veg = models.CharField(max_length=2, choices=[('V', 'Veg'), ('NV', 'Non-Veg')])
    expected_price = models.IntegerField()

class Meal(models.Model):
    meal_id = models.IntegerField(primary_key=True)
    meal_type_id = models.ForeignKey(MealTypeDetails, on_delete=models.CASCADE)
    person_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    meal_time = models.TimeField()
    meal_date = models.DateField()
    entry_type = models.CharField(max_length=5, choices=[('Self', 'Self'), ('Track', 'Track')])

