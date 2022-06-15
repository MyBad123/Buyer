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
CREATE TABLE IF NOT EXISTS elements(
    id SERIAL PRIMARY KEY,
    content_element text,
    url text,
    length integer,
    class_ob text,
    id_element text,
    style text,
    enclosure integer,
    href text,
    count integer,
    location_x float,
    location_y float,
    size_width float,
    size_height float,
    path text,
    integer integer,
    float integer,
    n_digits integer,
    presence_of_ruble integer,
    presence_of_vendor integer,
    presence_of_link integer,
    presence_of_at integer,
    has_point integer,
    writing_form integer,
    font_size text,
    font_family text,
    color text,
    distance_btw_el_and_ruble float,
    distance_btw_el_and_article float,
    ratio_coordinate_to_height float,
    hue float,
    saturation float,
    brightness float,
    background text,
    text text,
    source text,
    site_id integer
);
CREATE TABLE IF NOT EXISTS sites(
    id SERIAL PRIMARY KEY,
    url text,
    emails text
);
\q
