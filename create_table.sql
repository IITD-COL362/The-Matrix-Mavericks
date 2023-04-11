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
DROP TABLE IF EXISTS User;


CREATE TABLE Restaurant (
    restaurant_id int Primary KEY,
    name varchar NOT NULL,
    city_id varchar NOT NULL,
    address varchar NOT NULL,
    latitude float NOT NULL,
    longitude float NOT NULL,
    avg_cost_for_two int NOT NULL,
    has_table_booking varchar(3) NOT NULL,
    has_online_delivery varchar(3) NOT NULL,
    is_delivering_now varchar(3) NOT NULL,
    switch_to_order_menu varchar(3) NOT NULL,
    aggregate_rating int NOT NULL,
    votes int NOT NULL
) ;

CREATE TABLE Avg_Cost_for_Two (
    high int NOT NULL,
    low int NOT NULL,
    price_range varchar(11) NOT NULL,
    primary key (high,low)
) ;

CREATE TABLE Rating (
    rating int PRIMARY KEY,
    rating_colour varchar NOT NULL
) ;

CREATE TABLE Restaurant_Cuisine (
    restaurant_id int NOT NULL,
    cuisine_id varchar NOT NULL,
    primary key (restaurant_id,cuisine_id)
) ;

CREATE TABLE City (
    city_id varchar primary key,
    country_name varchar NOT NULL
) ;

CREATE TABLE Country_Currency (
    country_name varchar primary key,
    currency_id varchar NOT NULL
) ;

CREATE TABLE Food (
    food_id int primary key,
    food_name varchar NOT NULL,
    cuisine_id varchar not null,
    calories int not null,
    fat int not null,
    carbohydrates int not null,
    protein int not null,
    sodium int not null,
    meal_type_id varchar not null,
    veg_non_veg varchar(2) not null
) ;

CREATE TABLE Meal (
    meal_id int primary key,
    meal_type_id varchar not null,
    person_id int not null,
    meal_time time not null,
    meal_date date not null,
    entry_type varchar(5) not null
) ;

CREATE TABLE Meal_Type_Details (
    meal_type_id varchar primary key,
    meal_type_score int not null
) ;


CREATE TABLE Currency (
    currency_id varchar primary key,
    inr_conversion float not null
) ;


CREATE TABLE User (
    user_id int primary key,
    name varchar not null,
    address varchar not null,
    city_id varchar not null,
    mail_id varchar not null,
    phone_number numeric(10,0) not null,
    birthday date not null,
    sex varchar(1) not null,
    weight int not null,
    account_creation_date date not null
) ;