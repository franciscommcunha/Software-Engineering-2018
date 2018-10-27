CREATE TABLE temperature (ID serial PRIMARY KEY, room varchar(30),value int, hour varchar(30));
CREATE TABLE CO2 (ID serial PRIMARY KEY, room varchar(30),	value int, hour varchar(30));	
CREATE TABLE humidity (ID serial PRIMARY KEY, room varchar(30),	value int, hour varchar(30));
CREATE TABLE luminosity (ID serial PRIMARY KEY, room varchar(30), value int, hour varchar(30));
CREATE TABLE energy(ID serial PRIMARY KEY,	appliance varchar(30), value int, hour varchar(30));
CREATE TABLE movement(ID serial PRIMARY KEY, local varchar(30), hour varchar(30));
CREATE TABLE event(ID serial PRIMARY KEY, name varchar(30), eventDate date, location varchar(30);

