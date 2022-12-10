-- Create Country table --

CREATE TABLE Country
(
  id_country    int       NOT NULL ,
  name_country  char(30)  NOT NULL ,
  primary key (id_country)
);

-- Create Country_data table --

CREATE TABLE Country_data
(
  id_country  int            NOT NULL ,
  year        int            NOT NULL ,
  hdi         decimal        NULL ,
  gdp         bigint         NULL ,
  primary key (id_country, year)
);

-- Create Suicide_data table --

CREATE TABLE Suicide_data
(
  id_country    int     NOT NULL ,
  year          int     NOT NULL ,
  sex           int     NOT NULL ,
  suicide       int     NULL ,
  population    int     NULL ,
  primary key (id_country, year, sex)
);

Create table People
(
  passport      int       not null ,
  id_country    int       not null ,
  sex           int       not null ,
  f_name        char(100) not null ,
  l_name        char(100)     null ,
  m_name        char(100)     null ,
  d_birth       date      not null ,
  d_death       date          null ,
  type_death    int           null ,
  primary key (passport, id_country)
);

Create table Type_death
(
  type_death    int        not null ,
  definition    char(100)  not null ,
  primary key (type_death)
);

-- Define foreign keys --

ALTER TABLE Country_data ADD CONSTRAINT FK_Country_data_Country FOREIGN KEY (id_country) REFERENCES Country (id_country);

ALTER TABLE Suicide_data ADD CONSTRAINT FK_Suicide_data_Country FOREIGN KEY (id_country) REFERENCES Country (id_country);
ALTER TABLE Suicide_data ADD CONSTRAINT FK_Suicide_data_Country_data FOREIGN KEY (id_country, "year") REFERENCES Country_data (id_country, "year");

ALTER TABLE People ADD CONSTRAINT FK_People_Country FOREIGN KEY (id_country) REFERENCES Country (id_country);
ALTER TABLE People ADD CONSTRAINT FK_People_Type_death FOREIGN KEY (type_death) REFERENCES Type_death (type_death);
