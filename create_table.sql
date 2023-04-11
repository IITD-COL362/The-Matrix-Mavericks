DROP TABLE IF EXISTS Restaurant;
DROP TABLE IF EXISTS Avg_Cost_for_Two;
DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS Restaurant_Cuisine;
DROP TABLE IF EXISTS City;
DROP TABLE IF EXISTS Country_Currency;
DROP TABLE IF EXISTS Food;
DROP TABLE IF EXISTS Meal;
DROP TABLE IF EXISTS Meal_Type_Details;
DROP TABLE IF EXISTS Currency;
DROP TABLE IF EXISTS User_data;

CREATE TABLE Currency (
    currency_id varchar primary key,
    inr_conversion float not null
) ;

CREATE TABLE Country_Currency (
    country_name varchar primary key,
    currency_id varchar NOT NULL,
	CONSTRAINT fk_country_currency
	FOREIGN KEY(currency_id)
	REFERENCES Currency(currency_id) 
) ;

CREATE TABLE City (
    city_id varchar primary key,
    country_name varchar NOT NULL,
	CONSTRAINT fk_city_country
	FOREIGN KEY(country_name)
	REFERENCES Country_Currency(country_name) 
) ;

CREATE TABLE Rating (
    rating float PRIMARY KEY,
    rating_colour varchar(11) NOT NULL
) ;

CREATE TABLE Avg_Cost_for_Two (
    high int NOT NULL,
    low int NOT NULL,
    price_range varchar(11) NOT NULL,
    primary key (high,low)
) ;

CREATE TABLE Meal_Type_Details (
    meal_type_id varchar(16) primary key,
    meal_type_score int not null
) ;

CREATE TABLE User_data (
    user_id int primary key,
    name varchar not null,
    address varchar,
    city_id varchar,
    mail_id varchar not null,
    phone_number numeric(10,0) not null,
    birthday date,
    sex varchar(1) check (sex in ('M','F','O')),
    weight int,
    account_creation_date date not null,
    CONSTRAINT valid_email CHECK (mail_id ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE TABLE Restaurant (
    restaurant_id int Primary KEY,
    name varchar NOT NULL,
    city_id varchar NOT NULL,
    address varchar NOT NULL,
    latitude float NOT NULL,
    longitude float NOT NULL,
    avg_cost_for_two int ,
    has_table_booking varchar(3) ,
    has_online_delivery varchar(3) ,
    is_delivering_now varchar(3) ,
    switch_to_order_menu varchar(3) ,
    aggregate_rating float check (aggregate_rating >= 0 and aggregate_rating<=5),
    votes int,
	CONSTRAINT fk_res_city
	FOREIGN KEY(city_id)
	REFERENCES City(city_id) 
) ;


CREATE TABLE Restaurant_Cuisine (
    restaurant_id int NOT NULL,
    cuisine_id varchar NOT NULL,
    primary key (restaurant_id,cuisine_id),
	CONSTRAINT fk_res_cus
	FOREIGN KEY(restaurant_id)
	REFERENCES Restaurant(restaurant_id) 
) ;

CREATE TABLE Food (
    food_id int primary key,
    food_name varchar NOT NULL,
    cuisine_id varchar not null,
    calories float ,
    fat float ,
    carbohydrates float ,
    protein float ,
    sodium float ,
    meal_type_id varchar(16) ,
    veg_non_veg varchar(2) check (veg_non_veg in ('V','NV')),
	expected_price int,
	CONSTRAINT fk_food_meal
	FOREIGN KEY(meal_type_id)
	REFERENCES Meal_Type_Details(meal_type_id) 
) ;

CREATE TABLE Meal (
    meal_id int primary key,
    meal_type_id varchar(16) not null,
    person_id int not null,
    meal_time time not null,
    meal_date date not null,
    entry_type varchar(5) not null check (entry_type in ('Self','Track')),
	CONSTRAINT fk_meal_mealtype
	FOREIGN KEY(meal_type_id)
	REFERENCES Meal_Type_Details(meal_type_id) ,
	CONSTRAINT fk_user_userdetail
	FOREIGN KEY(person_id)
	REFERENCES User_data(user_id) 
) ;
