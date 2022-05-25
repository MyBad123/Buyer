UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'b2b';
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'b2b' AND pid <> pg_backend_pid();
DROP DATABASE "b2b";
CREATE DATABASE b2b;
ALTER ROLE buyer_user SET client_encoding TO 'utf8';
ALTER ROLE buyer_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE buyer_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE b2b TO buyer_user;
\q
