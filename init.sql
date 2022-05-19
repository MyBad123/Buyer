DROP DATABASE "b2b";
CREATE DATABASE b2b;
ALTER ROLE buyer_user SET client_encoding TO 'utf8';
ALTER ROLE buyer_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE buyer_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE b2b TO buyer_user;
\q
