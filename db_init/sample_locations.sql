--
-- PostgreSQL database dump
--

\restrict BlTsxHr7hgf9IAnX99KxJtJiktMqkW8MYo84TwY70IagL2T9QRZrWf7pvWEjbmJ

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
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: bruno
--

INSERT INTO public.locations (id, building_level, name) VALUES (1, 2, '35');
INSERT INTO public.locations (id, building_level, name) VALUES (2, 1, '24');
INSERT INTO public.locations (id, building_level, name) VALUES (3, 1, '21');
INSERT INTO public.locations (id, building_level, name) VALUES (4, -1, 'inf1');


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bruno
--

SELECT pg_catalog.setval('public.locations_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

\unrestrict BlTsxHr7hgf9IAnX99KxJtJiktMqkW8MYo84TwY70IagL2T9QRZrWf7pvWEjbmJ

