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

INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (1, 'black', 'Black', 'Czarny', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (2, 'white', 'White', 'Biały', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (3, 'grey', 'Gray', 'Szary', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (4, 'beige', 'Beige', 'Beżowy', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (5, 'red', 'Red', 'Czerwony', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (6, 'orange', 'Orange', 'Pomarańczowy', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (7, 'yellow', 'Yellow', 'Żółty', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (8, 'green', 'Green', 'Zielony', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (9, 'royalblue', 'Blue', 'Niebieski', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (10, 'purple', 'Purple', 'Fioletowy', NULL);
INSERT INTO public.colours (id, name, display_name, display_name_pl, colour_value) VALUES (11, 'pink', 'Pink', 'Różowy', NULL);


--
-- Name: colours_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bruno
--

SELECT pg_catalog.setval('public.colours_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

\unrestrict C8sUVfhZOzGAaafIwd4lasYwCxrZpgNsNgPIA7uUgewduTTAAqHwP8z6fa4vJdy

