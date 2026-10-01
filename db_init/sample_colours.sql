--
-- PostgreSQL database dump
--

\restrict C8sUVfhZOzGAaafIwd4lasYwCxrZpgNsNgPIA7uUgewduTTAAqHwP8z6fa4vJdy

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: colours; Type: TABLE DATA; Schema: public; Owner: bruno
--


insert into public.colours (name, display_name, display_name_pl, colour_hex_value) values 
    ('black', 'Black', 'Czarny', '#111111'),
    ('white', 'White', 'Biały', '#ffeeff'),
    ('grey', 'Gray', 'Szary', '#999999'),
    ('beige', 'Beige', 'Beżowy', '#fbe4b5'),
    ('red', 'Red', 'Czerwony', '#d41f1f'),
    ('orange', 'Orange', 'Pomarańczowy', '#e88d1e'),
    ('yellow', 'Yellow', 'Żółty', '#ffef3a'),
    ('green', 'Green', 'Zielony', '#268800'),
    ('royalblue', 'Blue', 'Niebieski', '#230383'),
    ('purple', 'Purple', 'Fioletowy', '#811cb7'),
    ('pink', 'Pink', 'Różowy', '#e868d9');

--
-- Name: colours_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bruno
--

SELECT pg_catalog.setval('public.colours_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

\unrestrict C8sUVfhZOzGAaafIwd4lasYwCxrZpgNsNgPIA7uUgewduTTAAqHwP8z6fa4vJdy

