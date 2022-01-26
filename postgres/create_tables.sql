-- Creation of country table
CREATE TABLE IF NOT EXISTS country (
  country_id INT NOT NULL,
  country_name varchar(450) NOT NULL,
  PRIMARY KEY (country_id)
);

-- Creation of city table
CREATE TABLE IF NOT EXISTS city (
  city_id INT NOT NULL,
  city_name varchar(450) NOT NULL,
  country_id INT NOT NULL,
  PRIMARY KEY (city_id),
  CONSTRAINT fk_country
      FOREIGN KEY(country_id) 
	  REFERENCES country(country_id)
);

-- Creation of user table
CREATE TABLE IF NOT EXISTS users (
  user_id INT NOT NULL,
  name varchar(250) NOT NULL,
  PRIMARY KEY (user_id)
);
