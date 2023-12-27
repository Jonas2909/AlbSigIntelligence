CREATE TABLE IF NOT EXISTS user_credentials (
    id serial PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

DO $$ 
BEGIN 
  RAISE NOTICE 'Database user_credentials created'; 
END $$;

CREATE TABLE IF NOT EXISTS measurements (
    id serial PRIMARY KEY,
    time_stamp bigint NOT NULL,
    quantity int,
    mac_address macaddr

);

CREATE TABLE IF NOT EXISTS mac_addresses (
    id serial PRIMARY KEY,
    mac VARCHAR(100) NOT NULL,
    time_stamp bigint NOT NULL
);

INSERT INTO user_credentials (firstname,lastname, username, password) VALUES ('samplefirstname', 'samplelastname', 'sampleuser', 'samplepassword');
INSERT INTO user_credentials (firstname,lastname, username, password) VALUES ('jonas', 'reinecke', 'username', 'password');

INSERT INTO measurements (time_stamp, quantity) VALUES (1701174250, 25);
INSERT INTO measurements (time_stamp, quantity) VALUES (1701176250, 15);

INSERT INTO mac_addresses (mac, time_stamp) VALUES ('00-1D-60-4A-8C-CB', 1703696400);
INSERT INTO mac_addresses (mac, time_stamp) VALUES ('01-1D-60-4A-8C-CB',  1703523600);

GRANT ALL ON user_credentials TO postgres;
GRANT ALL ON measurements TO postgres;
GRANT ALL ON mac_addresses TO postgres;
