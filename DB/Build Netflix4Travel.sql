USE Test;

DROP TABLE IF EXISTS locations_table;
CREATE TABLE locations_table (
    dummy int(11) NOT NULL,
    location_id int(11) NOT NULL,
    location_name varchar(255)

    );

LOAD DATA LOCAL INFILE 'C:/Users/lzeng/Documents/GitHub/Netflix4Travel/DB/locations_table.csv' INTO TABLE locations_table FIELDS TERMINATED BY ',' IGNORE 1 LINES;

DROP TABLE IF EXISTS users_table;
CREATE TABLE users_table (
    dummy int(11) NOT NULL,
    user_id int(11) NOT NULL,
    username varchar(255)

    );

LOAD DATA LOCAL INFILE 'C:/Users/lzeng/Documents/GitHub/Netflix4Travel/DB/users_table.csv' INTO TABLE users_table FIELDS TERMINATED BY ',' IGNORE 1 LINES;

DROP TABLE IF EXISTS ratings_table;
CREATE TABLE ratings_table (
    dummy int(11) NOT NULL,
    user_id int(11) NOT NULL,
    location_id int(11) NOT NULL,
    rating int(3)

    );

LOAD DATA LOCAL INFILE 'C:/Users/lzeng/Documents/GitHub/Netflix4Travel/DB/ratings.csv' INTO TABLE ratings_table FIELDS TERMINATED BY ',' IGNORE 1 LINES;