from django import forms
from django.db import connection
 
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM country_currency")
    countries = cursor.fetchall()
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM City")
    cities = cursor.fetchall()
ccountry=[('Select','Select')]+[(country[0],country[0]) for country in countries]
ccity=[('Select','Select')]+[(city[0],city[0]) for city in cities]
yes_no=[('Select','Select'),('YES','YES'),('NO','NO')]
rating_choices=[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)]
votes_choices=[(0,0),(100,100),(200,200),(300,300),(400,400),(500,500),(1000,1000),(10000,10000)]
lavg=[(0,0),(100,100),(200,200),(300,300),(400,400),(500,500),(1000,1000),(10000,10000)]
havg=[(100000,100000),(100,100),(200,200),(300,300),(400,400),(500,500),(1000,1000),(10000,10000)]

MEAL_CHOICES= [
    ('Fruits', 'Fruits'),
    ('Wheat based', 'Wheat based'),
    ('Rice based', 'Rice based'),
    ('Meat based', 'Meat based'),
    ('Sea food based', 'Sea food based'),
    ('Salad based', 'Salad based'),
    ('Milk based', 'Milk based'),
    ('Junk food', 'Junk food'),
    ('Vegetarian based', 'Vegetarian based'),
    ('Dessert', 'Dessert'),
    ('Egg based', 'Egg based'),
    ]

class MealCountForm(forms.Form):
    person_id = forms.IntegerField(label='Enter Person ID')
    
class AddMealForm(forms.Form):
    meal_type = forms.CharField(label = 'What type of meal did you eat ? ',widget=forms.Select(choices = MEAL_CHOICES))
    
class UpdateWeightForm(forms.Form):
    new_weight = forms.IntegerField(label='Enter the new weight')
    
class UpdateMailidForm(forms.Form):
    new_mailid = forms.CharField(label='Enter the new mail id')
    
class UpdatePhonenumberForm(forms.Form):
    new_phonenumber = forms.IntegerField(label='Enter the new phone number')
    
class UpdateCityForm(forms.Form):
    new_city = forms.CharField(label='Enter the new city')
    
class UpdateAddressForm(forms.Form):
    new_address = forms.CharField(label='Enter the new address')
    
class LocationForm(forms.Form):
    latitude = forms.FloatField(label = 'Enter your latitude' )
    longitude = forms.FloatField(label = 'Enter your longitude') 

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM Meal_type_details")
    meals = cursor.fetchall()
with connection.cursor() as cursor:
    cursor.execute("SELECT distinct cuisine_id FROM food")
    cuisines = cursor.fetchall()
cveg=[('Select','Select'),('V','V'),('NV','NV')]
ccuisine=[('Select','Select')]+[(cuisine[0],cuisine[0]) for cuisine in cuisines]
cmeal=[('Select','Select')]+[(meal[0],meal[0]) for meal in meals]
crange=[('Select','Select'),('low','low'),('medium','medium'),('high','high')]


# creating a form
class RestForm(forms.Form):
    country = forms.CharField(label = 'country',required = False,widget=forms.Select(choices = ccountry))
    city = forms.CharField(label = 'city',required = False,widget=forms.Select(choices = ccity))
    avgcost1 = forms.IntegerField(label = 'minimum average food cost for two persons' ,required = False, widget=forms.Select(choices= lavg))
    avgcost2 = forms.IntegerField(label = 'maximum average food cost for two persons' ,required = False, widget=forms.Select(choices= havg))
    rating = forms.IntegerField(label = 'minimum rating' ,required = False, widget=forms.Select(choices = rating_choices))
    votes = forms.IntegerField(label = 'minimum votes given' ,required = False, widget=forms.Select(choices= votes_choices))
    htb = forms.CharField(label= 'has table booking' ,required = False, widget=forms.Select(choices = yes_no))
    hod = forms.CharField(label= 'has online delivery' ,required = False, widget=forms.Select(choices = yes_no))
    idn = forms.CharField(label= 'is delevering now' ,required = False, widget=forms.Select(choices = yes_no))
    stom = forms.CharField(label= 'switch to order menu' ,required = False, widget=forms.Select(choices = yes_no))

class FoodForm(forms.Form):
    cuisine = forms.CharField(label = 'cuisine',required = False,widget=forms.Select(choices = ccuisine))
    meal = forms.CharField(label= 'meal type' ,required = False, widget=forms.Select(choices = cmeal))
    veg = forms.CharField(label= 'veg or non-veg' ,required = False, widget=forms.Select(choices = cveg))
    calorie = forms.CharField(label = 'minimum calorie per 100g in kcal' ,required = False, widget=forms.Select(choices= crange))
    carbohydrate = forms.CharField(label = 'minimum carbohydarte per 100g in grams' ,required = False, widget=forms.Select(choices= crange))
    protein = forms.CharField(label = 'minimum protein per 100g in grams' ,required = False, widget=forms.Select(choices = crange))
    fat = forms.CharField(label = 'maximum fat content per 100g' ,required = False, widget=forms.Select(choices= crange))
    sodium = forms.CharField(label = 'minimum sodium content per 100g in milligrams' ,required = False, widget=forms.Select(choices= crange))


class MixForm(forms.Form):
    cuisine = forms.CharField(label = 'cuisine',required = False,widget=forms.Select(choices = ccuisine))
    meal = forms.CharField(label= 'meal type' ,required = False, widget=forms.Select(choices = cmeal))
    veg = forms.CharField(label= 'veg or non-veg' ,required = False, widget=forms.Select(choices = cveg))
    calorie = forms.CharField(label = 'minimum calorie per 100g in kcal' ,required = False, widget=forms.Select(choices= crange))
    carbohydrate = forms.CharField(label = 'minimum carbohydarte per 100g in grams' ,required = False, widget=forms.Select(choices= crange))
    protein = forms.CharField(label = 'minimum protein per 100g in grams' ,required = False, widget=forms.Select(choices = crange))
    fat = forms.CharField(label = 'maximum fat content per 100g' ,required = False, widget=forms.Select(choices= crange))
    sodium = forms.CharField(label = 'minimum sodium content per 100g in milligrams' ,required = False, widget=forms.Select(choices= crange))
    country = forms.CharField(label = 'country',required = False,widget=forms.Select(choices = ccountry))
    city = forms.CharField(label = 'city',required = False,widget=forms.Select(choices = ccity))
    avgcost1 = forms.IntegerField(label = 'minimum average food cost for two persons' ,required = False, widget=forms.Select(choices= lavg))
    avgcost2 = forms.IntegerField(label = 'maximum average food cost for two persons' ,required = False, widget=forms.Select(choices= havg))
    rating = forms.IntegerField(label = 'minimum rating' ,required = False, widget=forms.Select(choices = rating_choices))
    votes = forms.IntegerField(label = 'minimum votes given' ,required = False, widget=forms.Select(choices= votes_choices))
    htb = forms.CharField(label= 'has table booking' ,required = False, widget=forms.Select(choices = yes_no))
    hod = forms.CharField(label= 'has online delivery' ,required = False, widget=forms.Select(choices = yes_no))
    idn = forms.CharField(label= 'is delevering now' ,required = False, widget=forms.Select(choices = yes_no))
    stom = forms.CharField(label= 'switch to order menu' ,required = False, widget=forms.Select(choices = yes_no))
    
class AddRating(forms.Form):
    restaurant = forms.CharField(label='Enter the name of restaurant to rate :')
    rating = forms.IntegerField(label='Enter the rating out of 5 :')
    
