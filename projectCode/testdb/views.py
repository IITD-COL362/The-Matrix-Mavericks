from django.shortcuts import render
from django.db import connection
from django.utils import timezone, dateformat
from .forms import MealCountForm,RestForm,FoodForm,MixForm, AddMealForm , UpdateWeightForm, UpdateAddressForm, UpdateCityForm, UpdateMailidForm, UpdatePhonenumberForm , LocationForm, AddRating , AddRest
import datetime
import math

def city_list(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM City")
		cities = cursor.fetchall()

	return render(request, 'city_list.html', {'cities': cities})

def meal_count(request):
	if request.method == 'POST':
		form = MealCountForm(request.POST)
		if form.is_valid():
			person_id = form.cleaned_data['person_id']
			with connection.cursor() as cursor:
				cursor.execute(f"SELECT COUNT(*) FROM Meal WHERE Person_id={person_id}")
				meal_count = cursor.fetchone()[0]
			return render(request, 'meal_count_result.html', {'meal_count': meal_count})
	else:
		form = MealCountForm()
	return render(request, 'meal_count.html', {'form': form})

def trending(request):
	# meal_date = dateformat.format(timezone.now().date(),'\'Y-m-d\'')
	meal_date = '\'2022-03-13\''
	with connection.cursor() as cursor:
		cursor.execute(f"select restaurant.restaurant_id, restaurant.name, noo from (select restaurant_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= {meal_date} group by restaurant_id order by noo desc limit 5) as t, restaurant where restaurant.restaurant_id = t.restaurant_id")
		top5a = cursor.fetchall()
	with connection.cursor() as cursor:
		cursor.execute(f"select food.food_id, food_name, noo from (select food_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= {meal_date} group by food_id order by noo desc limit 5) as t, food where food.food_id = t.food_id")
		top5b = cursor.fetchall()
	with connection.cursor() as cursor:
		cursor.execute(f"select meal_type_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= {meal_date} group by meal_type_id order by noo desc limit 5")
		top5c = cursor.fetchall()
	with connection.cursor() as cursor:
		cursor.execute(f"with var as (select food_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= {meal_date} group by food_id), nvar as (select cuisine_id,count(*) as noc from food,var where food.food_id=var.food_id group by cuisine_id order by noc desc limit 5) select * from nvar")
		top5d = cursor.fetchall()      
	return render(request, 'trending.html', {'top5a': top5a,'top5b': top5b,'top5c': top5c,'top5d': top5d})

def restaurant_detail(request, restaurant_id):
	with connection.cursor() as cursor:
		cursor.execute(f"select * from restaurant where restaurant_id='{restaurant_id}'")
		restaurant = cursor.fetchall()
	return render(request, 'restaurant_detail.html', {'restaurant': restaurant})

def menu(request, restaurant_id):
	with connection.cursor() as cursor:
		cursor.execute(f"select food.* from food, restaurant_cuisine where restaurant_id='{restaurant_id}' and food.cuisine_id=restaurant_cuisine.cuisine_id")
		menu = cursor.fetchall()
	return render(request, 'menu.html', {'menu': menu})

def dashboard(request):
	enddate = dateformat.format(timezone.now().date(),'\'Y-m-d\'')
	startdate = dateformat.format(timezone.now() - datetime.timedelta(days=7),'\'Y-m-d\'')
	personid = request.user 
	with connection.cursor() as cursor:
		cursor.execute(f"select count(*) from meal where person_id = '{personid}' and entry_type = 'Track' and meal_date >= {startdate} and meal_date <= {enddate};")
		tracked_meals = cursor.fetchone()[0]
	with connection.cursor() as cursor:
		cursor.execute(f"with t as (select * from meal where person_id = '{personid}' and meal_date >= {startdate} and meal_date <= {enddate}) select sum(meal_type_score) as total_score from t,meal_type_details where t.meal_type_id = meal_type_details.meal_type_id")
		user_score = cursor.fetchone()[0]
	with connection.cursor() as cursor:
		cursor.execute(f"select 1.0*count(*)/7 as avg_meals from meal where person_id = '{personid}' and meal_date >= {startdate} and meal_date <= {enddate}")
		avg_meals = cursor.fetchone()[0]
		avg_meals = round(avg_meals,2)
	context = {
		'tracked_meals': tracked_meals,
		'user_score': user_score,
		'avg_meals': avg_meals,
	}
	return render(request, 'dashboard.html', context)

				
def add_meal(request):
	mealtime = timezone.localtime(timezone.now()).strftime('\'%H:%M:%S\'')
	mealdate = dateformat.format(timezone.now().date(),'\'Y-m-d\'')
	if request.method == 'POST':
		form = AddMealForm(request.POST)
		if form.is_valid():
			meal_type = form.cleaned_data['meal_type']
			with connection.cursor() as cursor:
				cursor.execute("SELECT COUNT(*) FROM MEAL")
				curr_max = cursor.fetchone()[0]
			next_max = curr_max+1
			print(next_max)
			with connection.cursor() as cursor:
				cursor.execute(f"INSERT INTO MEAL VALUES ({next_max},'{meal_type}','{request.user}',{mealtime},{mealdate},'Self',NULL,NULL)")
			return render(request, 'successful.html')
	else:
		form = AddMealForm()
	return render(request, 'add_meal.html', {'form': form})

def track_meal(request,restaurant_id,food_id,meal_type):
	mealtime = timezone.localtime(timezone.now()).strftime('\'%H:%M:%S\'')
	mealdate = dateformat.format(timezone.now().date(),'\'Y-m-d\'')
	with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM MEAL")
		curr_max = cursor.fetchone()[0]
	next_max = curr_max+1
	print(next_max)
	with connection.cursor() as cursor:
		cursor.execute(f"INSERT INTO MEAL VALUES ({next_max},'{meal_type}','{request.user}',{mealtime},{mealdate},'Track',{restaurant_id},{food_id})")
	return render(request, 'successful.html')

def statistics_user(request):
	personid = request.user
	with connection.cursor() as cursor:
		cursor.execute(f"with t as (select meal_type_id as meal_type,0 as number_of_meals from meal_type_details union all select meal_type_id as meal_type,count(*) from meal where person_id = '{personid}' group by meal_type_id),sum_table as (select (case when sum(number_of_meals)<=0 then 1 else sum(number_of_meals) end) as total_meals from t), val_table as (select meal_type,sum(number_of_meals) as count_meals from t group by meal_type) select meal_type,ROUND(100.0 * count_meals / total_meals, 2) as percent_of_meals from val_table,sum_table")
		data = cursor.fetchall()
	return render(request,'stats.html',{'data': data })

def profile_user(request):
	personid = request.user
	with connection.cursor() as cursor:
		cursor.execute(f"select * from user_data where user_id = '{personid}'")
		data = cursor.fetchall()
	return render(request,'profile.html',{'data': data})
		
# # update address,city,mailid,phonenumber,weight
def update_weight(request):
	personid = request.user
	if request.method == 'POST':
		form = UpdateWeightForm(request.POST)
		if form.is_valid():
			new_weight = form.cleaned_data['new_weight']
			with connection.cursor() as cursor:
				cursor.execute(f"update user_data set weight = {new_weight} where user_id='{personid}'")
			return render(request,'successful.html',{'form':form})
	else:
		form = UpdateWeightForm()
	return render(request,'update_weight.html',{'form':form})

def update_address(request):
	personid = request.user
	if request.method == 'POST':
		form = UpdateAddressForm(request.POST)
		if form.is_valid():
			new_address = form.cleaned_data['new_address']
			with connection.cursor() as cursor:
				cursor.execute(f"update user_data set address = '{new_address}' where user_id='{personid}'")
			return render(request,'successful.html',{'form':form})
	else:
		form = UpdateAddressForm()
	return render(request,'update_address.html',{'form':form})

def update_city(request):
	personid = request.user
	if request.method == 'POST':
		form = UpdateCityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['new_city']
			with connection.cursor() as cursor:
				cursor.execute(f"update user_data set city_id = '{new_city}' where user_id='{personid}'")
			return render(request,'successful.html',{'form':form})
	else:
		form = UpdateCityForm()
	return render(request,'update_city.html',{'form':form})

def update_mailid(request):
	personid = request.user
	if request.method == 'POST':
		form = UpdateMailidForm(request.POST)
		if form.is_valid():
			new_mailid = form.cleaned_data['new_mailid']
			with connection.cursor() as cursor:
				cursor.execute(f"update user_data set mailid = '{new_mailid}' where user_id='{personid}'")
			return render(request,'successful.html',{'form':form})
	else:
		form = UpdateMailidForm()
	return render(request,'update_mailid.html',{'form':form})

def update_phonenumber(request):
	personid = request.user
	if request.method == 'POST':
		form = UpdatePhonenumberForm(request.POST)
		if form.is_valid():
			new_phonenumber = form.cleaned_data['new_phonenumber']
			with connection.cursor() as cursor:
				cursor.execute(f"update user_data set phone_number = {new_phonenumber} where user_id='{personid}'")
			return render(request,'successful.html',{'form':form})
	else:
		form = UpdatePhonenumberForm()
	return render(request,'update_phonenumber.html',{'form':form})

def homepage(request):
	return render(request, 'homepage.html')

def restaurants_nearme(request):
	if request.method == 'POST':
		form = LocationForm(request.POST)
		if form.is_valid():
			latitude = form.cleaned_data['latitude']
			longitude = form.cleaned_data['longitude']
			with connection.cursor() as cursor:
				cursor.execute(f"SELECT restaurant_id, name, 6371 * 2 * ASIN(SQRT(POWER(SIN((RADIANS({longitude}) - RADIANS(latitude)) / 2), 2) +COS(RADIANS({longitude})) * COS(RADIANS(latitude)) *POWER(SIN((RADIANS({latitude}) - RADIANS(longitude)) / 2), 2))) AS distance_in_km FROM restaurant ORDER BY distance_in_km ASC LIMIT 50")
				restaurant_list = cursor.fetchall()
			return render(request,'restaurant_list.html',{'restaurant_list':restaurant_list})
	else:
		form = LocationForm()
	return render(request,'lat_long.html',{'form':form})

is_name=True
is_city=True
is_avgcost=True
is_htb=True
is_hod=True
is_idn=True
is_stom=True
is_rating=True
is_votes=True
fname='Chokhi Dhani'
fcity='Jaipur'
favgcost1=0
favgcost2=100
fhtb='Yes'
fhod='Yes'
fidn='Yes'
fstom='Yes'
frating=1
fvotes=100
fcountry='India'

is_cuisine=True
is_calorie=True
is_fat=True
is_carbohydrate=True
is_protein=True
is_sodium=True
is_meal=True
is_veg=True
fcuisine='Salad'
fcalorie1=0
fcalorie2=0
ffat1=0
ffat2=0
fcarbohydrate1=0
fcarbohydrate2=0
fprotein1=0
fprotein2=0
fsodium1=0
fsodium2=0
fmeal='Wheat Based'
fveg='V'

def filter_food(request):
	global is_calorie,is_carbohydrate,is_protein,is_fat,is_sodium,is_cuisine,is_meal,is_veg
	global fcalorie1,fcalorie2,ffat1,ffat2,fcarbohydrate1,fcarbohydrate2,fprotein1,fprotein2,fsodium1,fsodium2,fmeal,fveg,fcuisine
	if request.method=='POST' :
		form=FoodForm(request.POST)
		if form.is_valid():
			fcuisine=form.cleaned_data['cuisine']
			fcalorie=form.cleaned_data['calorie']
			ffat=form.cleaned_data['fat']
			fprotein=form.cleaned_data['protein']
			fcarbohydrate=form.cleaned_data['carbohydrate']
			fsodium=form.cleaned_data['sodium']
			fveg=form.cleaned_data['veg']
			fmeal=form.cleaned_data['meal']
			if (fcuisine=='Select') :
				is_cuisine=True
			else :
				is_cuisine=False
			if fmeal=='Select' :
				is_meal=True
			else :
				is_meal=False
			if (fveg=='Select') :
				is_veg=True
			else :
				is_veg=False
			if (fprotein=='Select') :
				is_protein=True
			elif fprotein=='low':
				is_protein=False
				fprotein1=0
				fprotein2=11
			elif fprotein=='medium':
				is_protein=False
				fprotein1=11
				fprotein2=30
			else :
				is_protein=False
				fprotein1=30
				fprotein2=100
			if (fcarbohydrate=='Select') :
				is_carbohydrate=True
			elif fcarbohydrate=='low':
				is_carbohydrate=False
				fcarbohydrate1=0
				fcarbohydrate2=20
			elif fcarbohydrate=='medium':
				is_carbohydrate=False
				fcarbohydrate1=20
				fcarbohydrate2=40
			else :
				is_carbohydrate=False
				fcarbohydrate1=40
				fcarbohydrate2=100
			if (ffat=='Select') :
				is_fat=True
			elif ffat=='low':
				is_fat=False
				ffat1=0
				ffat2=10
			elif ffat=='medium':
				is_fat=False
				ffat1=10
				ffat2=30
			else :
				is_fat=False
				ffat1=30
				ffat2=100
			if (fcalorie=='Select') :
				is_calorie=True
			elif fcalorie=='low':
				is_calorie=False
				fcalorie1=0
				fcalorie2=220
			elif fcalorie=='medium':
				is_calorie=False
				fcalorie1=220
				fcalorie2=440
			else :
				is_calorie=False
				fcalorie1=440
				fcalorie2=10000
			if (fsodium=='Select') :
				is_sodium=True
			elif fsodium=='low':
				is_sodium=False
				fsodium1=0
				fsodium2=395
			elif fsodium=='medium':
				is_sodium=False
				fsodium1=395
				fsodium2=1000
			else :
				is_sodium=False
				fsodium1=1000
				fsodium2=10000
			with connection.cursor() as cursor:
				cursor.execute(f"select * from food where ({is_cuisine} or cuisine_id='{fcuisine}') and ({is_calorie} or (calories>={fcalorie1} and calories<={fcalorie2})) and ({is_fat} or (fat<={ffat2} and fat>={ffat1})) and ({is_carbohydrate} or (carbohydrates>={fcarbohydrate1} and carbohydrates<={fcarbohydrate2})) and ({is_protein} or (protein>={fprotein1} and protein<={fprotein2})) and ({is_sodium} or (sodium>={fsodium1} and sodium<={fsodium2})) and ({is_meal} or meal_type_id='{fmeal}') and ({is_veg} or veg_non_veg='{fveg}') order by food_id asc")
				foods = cursor.fetchall()
			render(request,'food.html',{'form':form,'foods':foods})
	else:
		form = FoodForm()
		foods={}
	return render(request,'food.html',{'form':form,'foods':foods})

def filter_restaurant(request):
	global is_city,is_avgcost,is_hod,is_htb,is_idn,is_stom,is_rating,is_name,is_votes
	global fcity,favgcost1,favgcost2,frating,fvotes,fname,fhtb,fhod,fidn,fstom,fcountry
	global is_calorie,is_carbohydrate,is_protein,is_fat,is_sodium,is_cuisine,is_meal,is_veg
	global fcalorie1,fcalorie2,ffat1,ffat2,fcarbohydrate1,fcarbohydrate2,fprotein1,fprotein2,fsodium1,fsodium2,fmeal,fveg,fcuisine
	if request.method == 'POST':
		form = RestForm(request.POST)
		if form.is_valid():
			fcountry=form.cleaned_data['country']
			fcity = form.cleaned_data['city']
			frating = form.cleaned_data['rating']
			favgcost1 = form.cleaned_data['avgcost1']
			favgcost2 = form.cleaned_data['avgcost2']
			fvotes = form.cleaned_data['votes']
			fhtb = form.cleaned_data['htb']
			fhod = form.cleaned_data['hod']
			fidn = form.cleaned_data['idn']
			fstom = form.cleaned_data['stom']
			if (fcity=='Select') :
				is_city=True
			else :
				is_city=False
			if (frating=='Select') :
				is_rating=True
			else :
				is_rating=False
			if (fvotes=='Select') :
				is_votes=True
			else :
				is_votes=False
			if (favgcost1=='Select') :
				is_avgcost=True
			else :
				is_avgcost=False
			if (fhtb=='Select') :
				is_htb=True
			else :
				is_htb=False
			if (fhod=='Select') :
				is_hod=True
			else :
				is_hod=False
			if (fidn=='Select') :
				is_idn=True
			else :
				is_idn=False
			if (fstom=='Select') :
				is_stom=True
			else :
				is_stom=False
			restaurants={}
			if (fcountry=='Select') :
				with connection.cursor() as cursor:
					cursor.execute(f"select * from restaurant where ({is_name} or name='{fname}') and ({is_city} or city_id='{fcity}') and ({is_avgcost} or (avg_cost_for_two>={favgcost1} and avg_cost_for_two<{favgcost2})) and ({is_htb} or has_table_booking='{fhtb}') and ({is_hod} or has_online_delivery='{fhod}') and ({is_idn} or is_delivering_now='{fidn}') and ({is_stom} or switch_to_order_menu='{fstom}') and ({is_rating} or aggregate_rating>={frating}) and ({is_votes} or votes>={fvotes}) order by aggregate_rating desc")
					restaurants = cursor.fetchall()
			else :
				with connection.cursor() as cursor:
					cursor.execute(f"with var as (select * from restaurant where ({is_name} or name='{fname}') and ({is_city} or city_id='{fcity}') and ({is_avgcost} or (avg_cost_for_two>={favgcost1} and avg_cost_for_two<{favgcost2})) and ({is_htb} or has_table_booking='{fhtb}') and ({is_hod} or has_online_delivery='{fhod}') and ({is_idn} or is_delivering_now='{fidn}') and ({is_stom} or switch_to_order_menu='{fstom}') and ({is_rating} or aggregate_rating>={frating}) and ({is_votes} or votes>={fvotes}) order by aggregate_rating desc),nvar as (select * from var,city where var.city_id=city.city_id and country_name='{fcountry}') select * from nvar order by aggregate_rating desc")
					restaurants = cursor.fetchall()
			render(request,'filter_rest.html',{'form':form,'restaurants':restaurants})
			# Do something with attribute and filter
	else:
		form = RestForm()
		restaurants={}
	return render(request,'filter_rest.html',{'form':form,'restaurants':restaurants})

def filter_mix(request) :
	global is_city,is_avgcost,is_hod,is_htb,is_idn,is_stom,is_rating,is_name,is_votes
	global fcity,favgcost1,favgcost2,frating,fvotes,fname,fhtb,fhod,fidn,fstom,fcountry
	global is_calorie,is_carbohydrate,is_protein,is_fat,is_sodium,is_cuisine,is_meal,is_veg
	global fcalorie1,fcalorie2,ffat1,ffat2,fcarbohydrate1,fcarbohydrate2,fprotein1,fprotein2,fsodium1,fsodium2,fmeal,fveg,fcuisine
	if request.method == 'POST':
		form = MixForm(request.POST)
		if form.is_valid() :
			fcountry=form.cleaned_data['country']
			fcity = form.cleaned_data['city']
			frating = form.cleaned_data['rating']
			favgcost1 = form.cleaned_data['avgcost1']
			favgcost2 = form.cleaned_data['avgcost2']
			fvotes = form.cleaned_data['votes']
			fhtb = form.cleaned_data['htb']
			fhod = form.cleaned_data['hod']
			fidn = form.cleaned_data['idn']
			fstom = form.cleaned_data['stom']
			fcuisine=form.cleaned_data['cuisine']
			fcalorie=form.cleaned_data['calorie']
			ffat=form.cleaned_data['fat']
			fprotein=form.cleaned_data['protein']
			fcarbohydrate=form.cleaned_data['carbohydrate']
			fsodium=form.cleaned_data['sodium']
			fveg=form.cleaned_data['veg']
			fmeal=form.cleaned_data['meal']
			if (fcity=='Select') :
				is_city=True
			else :
				is_city=False
			if (frating=='Select') :
				is_rating=True
			else :
				is_rating=False
			if (fvotes=='Select') :
				is_votes=True
			else :
				is_votes=False
			if (favgcost1=='Select') :
				is_avgcost=True
			else :
				is_avgcost=False
			if (fhtb=='Select') :
				is_htb=True
			else :
				is_htb=False
			if (fhod=='Select') :
				is_hod=True
			else :
				is_hod=False
			if (fidn=='Select') :
				is_idn=True
			else :
				is_idn=False
			if (fstom=='Select') :
				is_stom=True
			else :
				is_stom=False
			if (fcuisine=='Select') :
				is_cuisine=True
			else :
				is_cuisine=False
			if fmeal=='Select' :
				is_meal=True
			else :
				is_meal=False
			if (fveg=='Select') :
				is_veg=True
			else :
				is_veg=False
			if (fprotein=='Select') :
				is_protein=True
			elif fprotein=='low':
				is_protein=False
				fprotein1=0
				fprotein2=11
			elif fprotein=='medium':
				is_protein=False
				fprotein1=11
				fprotein2=30
			else :
				is_protein=False
				fprotein1=30
				fprotein2=100
			if (fcarbohydrate=='Select') :
				is_carbohydrate=True
			elif fcarbohydrate=='low':
				is_carbohydrate=False
				fcarbohydrate1=0
				fcarbohydrate2=20
			elif fcarbohydrate=='medium':
				is_carbohydrate=False
				fcarbohydrate1=20
				fcarbohydrate2=40
			else :
				is_carbohydrate=False
				fcarbohydrate1=40
				fcarbohydrate2=100
			if (ffat=='Select') :
				is_fat=True
			elif ffat=='low':
				is_fat=False
				ffat1=0
				ffat2=10
			elif ffat=='medium':
				is_fat=False
				ffat1=10
				ffat2=30
			else :
				is_fat=False
				ffat1=30
				ffat2=100
			if (fcalorie=='Select') :
				is_calorie=True
			elif fcalorie=='low':
				is_calorie=False
				fcalorie1=0
				fcalorie2=220
			elif fcalorie=='medium':
				is_calorie=False
				fcalorie1=220
				fcalorie2=440
			else :
				is_calorie=False
				fcalorie1=440
				fcalorie2=10000
			if (fsodium=='Select') :
				is_sodium=True
			elif fsodium=='low':
				is_sodium=False
				fsodium1=0
				fsodium2=395
			elif fsodium=='medium':
				is_sodium=False
				fsodium1=395
				fsodium2=1000
			else :
				is_sodium=False
				fsodium1=1000
				fsodium2=10000
			restaurants={}
			if (fcountry=='Select') :
				with connection.cursor() as cursor:
					cursor.execute(f"with var as (select * from food where ({is_cuisine} or cuisine_id='{fcuisine}') and ({is_calorie} or (calories>={fcalorie1} and calories<={fcalorie2})) and ({is_fat} or (fat<={ffat2} and fat>={ffat1})) and ({is_carbohydrate} or (carbohydrates>={fcarbohydrate1} and carbohydrates<={fcarbohydrate2})) and ({is_protein} or (protein>={fprotein1} and protein<={fprotein2})) and ({is_sodium} or (sodium>={fsodium1} and sodium<={fsodium2})) and ({is_meal} or meal_type_id='{fmeal}') and ({is_veg} or veg_non_veg='{fveg}') order by food_id asc),nvar as (select cuisine_id,count(*) as noi from var group by cuisine_id),fvar as (select restaurant_id,sum(noi) as tnoi from restaurant_cuisine,nvar where restaurant_cuisine.cuisine_id=nvar.cuisine_id group by restaurant_id),tvar as (select * from (select * from restaurant,fvar where restaurant.restaurant_id=fvar.restaurant_id) as tab where ({is_name} or name='{fname}') and ({is_city} or city_id='{fcity}') and ({is_avgcost} or (avg_cost_for_two>={favgcost1} and avg_cost_for_two<{favgcost2})) and ({is_htb} or has_table_booking='{fhtb}') and ({is_hod} or has_online_delivery='{fhod}') and ({is_idn} or is_delivering_now='{fidn}') and ({is_stom} or switch_to_order_menu='{fstom}') and ({is_rating} or aggregate_rating>={frating}) and ({is_votes} or votes>={fvotes}) order by aggregate_rating desc) select * from tvar order by tnoi desc,name asc")
					restaurants = cursor.fetchall()
			else :
				with connection.cursor() as cursor:
					cursor.execute(f"with var as (select * from food where ({is_cuisine} or cuisine_id='{fcuisine}') and ({is_calorie} or (calories>={fcalorie1} and calories<={fcalorie2})) and ({is_fat} or (fat<={ffat2} and fat>={ffat1})) and ({is_carbohydrate} or (carbohydrates>={fcarbohydrate1} and carbohydrates<={fcarbohydrate2})) and ({is_protein} or (protein>={fprotein1} and protein<={fprotein2})) and ({is_sodium} or (sodium>={fsodium1} and sodium<={fsodium2})) and ({is_meal} or meal_type_id='{fmeal}') and ({is_veg} or veg_non_veg='{fveg}') order by food_id asc),nvar as (select cuisine_id,count(*) as noi from var group by cuisine_id),fvar as (select restaurant_id,sum(noi) as tnoi from restaurant_cuisine,nvar where restaurant_cuisine.cuisine_id=nvar.cuisine_id group by restaurant_id),tvar as (select * from (select * from restaurant,fvar where restaurant.restaurant_id=fvar.restaurant_id) as tab where ({is_name} or name='{fname}') and ({is_city} or city_id='{fcity}') and ({is_avgcost} or (avg_cost_for_two>={favgcost1} and avg_cost_for_two<{favgcost2})) and ({is_htb} or has_table_booking='{fhtb}') and ({is_hod} or has_online_delivery='{fhod}') and ({is_idn} or is_delivering_now='{fidn}') and ({is_stom} or switch_to_order_menu='{fstom}') and ({is_rating} or aggregate_rating>={frating}) and ({is_votes} or votes>={fvotes}) order by aggregate_rating desc) select * from tvar order by tnoi desc,name asc")
					restaurants = cursor.fetchall()
			render(request,'mix.html',{'form':form,'restaurants':restaurants})
			# Do something with attribute and filter
	else:
		form = MixForm()
		restaurants={}
	return render(request,'mix.html',{'form':form,'restaurants':restaurants})

def rate_restaurant(request,restaurant_id):
	if request.method == 'POST':
		form = AddRating(request.POST)
		if form.is_valid():
			added_rating = form.cleaned_data['rating']
			with connection.cursor() as cursor:
				cursor.execute(f"SELECT votes,aggregate_rating from restaurant where restaurant_id = '{restaurant_id}'")
				data = cursor.fetchall()
				votes = data[0][0]
				rating = data[0][1]
			new_votes = votes+1
			new_rating = (votes*rating+added_rating)/new_votes
			with connection.cursor() as cursor:
				cursor.execute(f"update restaurant set votes = {new_votes} where restaurant_id = '{restaurant_id}'")
				cursor.execute(f"update restaurant set aggregate_rating = {new_rating} where restaurant_id = '{restaurant_id}'")
			return render(request,'successful.html',{'form':form})
	else:
		form = AddRating()
	return render(request,'rating.html',{'form':form})

def check_prime(a):
	b = math.floor(math.sqrt(a))
	for i in range(2,b+1):
		if(a%i==0):
			return False
	return True


def add_restaurant(request):
	if request.method == 'POST':
		form = AddRest(request.POST)
		if form.is_valid():
			with connection.cursor() as cursor:
				cursor.execute("SELECT MAX(RESTAURANT_ID) FROM MEAL")
				curr_max = cursor.fetchone()[0]
			next_max = curr_max+1
			restaurant_name = form.cleaned_data['name']
			city = form.cleaned_data['city']
			address = form.cleaned_data['address']
			latitude = form.cleaned_data['latitude']
			longitude = form.cleaned_data['longitude']
			avg_cost_for_two = form.cleaned_data['avg_cost_for_two']
			htb = form.cleaned_data['htb']
			hod = form.cleaned_data['hod']
			idn = form.cleaned_data['idn']
			stom = form.cleaned_data['stom']
			cuisines = form.cleaned_data['cuisines']
			cuisines_list = cuisines.split(',')
			verification_number = form.cleaned_data['verification_number']
			if(check_prime(verification_number)):
				with connection.cursor() as cursor:
					cursor.execute(f"INSERT INTO RESTAURANT VALUES ({next_max},'{restaurant_name}','{city}','{address}',{latitude},{longitude},{avg_cost_for_two},'{htb}','{hod}','{idn}','{stom}',0,0)")
				for i in range(0,len(cuisines_list)):
					with connection.cursor() as cursor:
						cursor.execute(f"INSERT INTO RESTAURANT_CUISINE VALUES ({next_max},'{cuisines_list[i]}')")
				return render(request, 'successful.html')
			else:
				return render(request,'verification.html')
	else:
		form = AddRest()
	return render(request, 'add_rest.html', {'form': form})


	 
