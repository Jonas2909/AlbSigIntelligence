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
    quantity int
);

CREATE TABLE IF NOT EXISTS mac_addresses (
    id serial PRIMARY KEY,
    hashed_mac_address VARCHAR(64) NOT NULL, -- length of 64 because of SHA256
    time_stamp bigint NOT NULL
);

INSERT INTO user_credentials (firstname,lastname, username, password) VALUES ('samplefirstname', 'samplelastname', 'sampleuser', 'samplepassword');
INSERT INTO user_credentials (firstname,lastname, username, password) VALUES ('jonas', 'reinecke', 'username', 'password');

INSERT INTO measurements (time_stamp, quantity) VALUES (1701174250, 25);
INSERT INTO measurements (time_stamp, quantity) VALUES (1701176250, 15);

INSERT INTO mac_addresses (hashed_mac_address, time_stamp) VALUES ('e140ef2f06fc2fac86f1e446149b890f6b762da78b7b3109df6cc49c9b29dec1', 1702915589);
INSERT INTO mac_addresses (hashed_mac_address, time_stamp) VALUES ('a56b61402f0913c69785a9df529f78658dcae766f619f3129b07bb6c5861578d',  1703174789);

GRANT ALL ON user_credentials TO postgres;
GRANT ALL ON measurements TO postgres;
GRANT ALL ON mac_addresses TO postgres;
