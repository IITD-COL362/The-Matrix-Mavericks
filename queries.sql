--q1--
\set A1 true
\set A2 true
\set A3 true
\set A4 true
\set A5 true
\set A6 true
\set A7 true
\set A8 true
\set A9 true
\set B1 '\'Chokhi Dhani\''
\set B2 '\'Jaipur\''
\set B31 100
\set B32 1000
\set B4 '\'NO\''
\set B5 '\'NO\''
\set B6 '\'NO\''
\set B7 '\'NO\''
\set B8 3
\set B9 100
-- filter restaurants
select * from restaurant where (:A1 or name=:B1) and (:A2 or city_id=:B2) and (:A3 or (avg_cost_for_two>=:B31 and avg_cost_for_two<:B32)) and (:A4 or has_table_booking=:B4) and (:A5 or has_online_delivery=:B5) and (:A6 or is_delivering_now=:B6) and (:A7 or switch_to_order_menu=:B7) and (:A8 or aggregate_rating>=:B8) and (:A9 or votes>=:B9) order by aggregate_rating desc;

--q2--
\set CN '\'India\''
-- filter restaurants based on country
with 
    var as (select * from restaurant where (:A1 or name=:B1) and (:A2 or city_id=:B2) and (:A3 or (avg_cost_for_two>=:B31 and avg_cost_for_two<:B32)) and (:A4 or has_table_booking=:B4) and (:A5 or has_online_delivery=:B5) and (:A6 or is_delivering_now=:B6) and (:A7 or switch_to_order_menu=:B7) and (:A8 or aggregate_rating>=:B8) and (:A9 or votes>=:B9)),
    nvar as (select * from var,city where restaurant.city_id=city.city_id and country_name=:CN)
select * from nvar order by aggregate_rating desc;

--q3--
\set C0 true
\set C1 true
\set C2 true
\set C3 true
\set C4 true
\set C5 true
\set C6 true
\set D7 true
\set D0 '\'Salad\''
\set D1 100
\set D2 100
\set D31 0
\set D32 100
\set D41 0
\set D42 100
\set D5 0
\set D6 '\'Wheat Based\''
\set D7 '\'V\''
-- filter food items based on attributes
select * from food where (:C0 or cuisine_id=:D0) and (:C1 or calories>=:D1) and (:C2 or fat<=:D2) and (:C3 or (carbohydrates>=:D31 and carbohydrates<=:D32)) and (:C4 or (protein>=:D41 and protein<=:D42)) and (:C5 or sodium>=:D5) and (:C6 or meal_type_id=:D6) and (:C7 or veg_non_veg=:D7) order by food_id asc;

--q4--
-- display food items of a given restaurant
\set GR 19687969
with 
    nvar as (select cuisine_id from restaurant_cuisine where restaurant_cuisine.restaurant_id=:GR),
    var2 as (select * from (select * from food,nvar where food.cuisine_id=nvar.cuisine_id) as tvar where (:C0 or cuisine_id=:D0) and (:C1 or calories>=:D1) and (:C2 or fat<=:D2) and (:C3 or (carbohydrates>=:D31 and carbohydrates<=:D32)) and (:C4 or (protein>=:D41 and protein<=:D42)) and (:C5 or sodium>=:D5) and (:C6 or meal_type_id=:D6) and (:C7 or veg_non_veg=:D7)),
select * from var2;


--q5--
--display restuarants with foods having nutrition values
with 
    var as (select * from food where (:C0 or cuisine_id=:D0) and (:C1 or calories>=:D1) and (:C2 or fat<=:D2) and (:C3 or (carbohydrates>=:D31 and carbohydrates<=:D32)) and (:C4 or (protein>=:D41 and protein<=:D42)) and (:C5 or sodium>=:D5) and (:C6 or meal_type_id=:D6) and (:C7 or veg_non_veg=:D7) order by food_id asc),
    nvar as (select cuisine_id,count(*) as noi from var group by cuisine_id),
    fvar as (select restaurant_id,sum(noi) as tnoi from restaurant_cuisine,nvar where restaurant_cuisine.cuisine_id=nvar.cuisine_id group by restaurant_id)
select * from restaurant,fvar where fvar.restaurant_id=restaurant.restaurant_id order by tnoi desc,name asc;



--q6--
\set TL '\'2023-03-17\''

select restaurant_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= :TL group by restaurant_id order by noo desc limit 5;

--q7--

select food_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= :TL group by food_id order by noo desc limit 5;

--q8--
select meal_type_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= :TL group by meal_type_id order by noo desc limit 5;

--q9--
with
    var as (select food_id,count(*) as noo from meal where meal.entry_type='Track' and meal.meal_date >= :TL group by food_id),
    nvar as (select cuisine_id,count(*) as noc from food,var where food.food_id=var.food_id group by cuisine_id order by noc desc limit 5)
select * from nvar;

--q10--
\set X 2
\set date1 '\'2023-04-17\''
\set date2 '\'2023-04-11\''
select count(*) from meal where person_id = :X and entry_type = 'Track' and meal_date >= :date2 and meal_date <= :date1;

--q11--
\set X 2
\set date1 '\'2023-04-17\''
\set date2 '\'2023-04-11\''

with t as 
(select * from meal where person_id = :X and meal_date >= :date2 and meal_date <= :date1)
select sum(meal_type_score) as total_score 
from t,meal_type_details where t.meal_type_id = meal_type_details.meal_type_id;

--q12--
\set X 2
\set date1 '\'2023-04-17\''
\set date2 '\'2023-04-11\''

with t as 
select 1.0*count(*)/7 as avg_meals from meal where person_id = :X and meal_date >= :date2 and meal_date <= :date1;

--q13--
\set X 2

with t as 
(select meal_type_id as meal_type,0 as number_of_meals from meal_type_details
union all
select meal_type_id as meal_type,count(*) from meal where person_id = :X group by meal_type_id),
sum_table as
(select 
(case 
	when sum(number_of_meals)<=0 then 1
	else sum(number_of_meals)
end) as total_meals 
from t),
val_table as
(select meal_type,sum(number_of_meals) as count_meals from t group by meal_type)
select meal_type,100.0*count_meals/total_meals as percent_of_meals from val_table,sum_table;
