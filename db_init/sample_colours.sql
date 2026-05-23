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

INSERT INTO public.colours (id, name, colourvalue) VALUES (1, 'black', NULL);
INSERT INTO public.colours (id, name, colourvalue) VALUES (2, 'white', NULL);
INSERT INTO public.colours (id, name, colourvalue) VALUES (3, 'beige', NULL);
INSERT INTO public.colours (id, name, colourvalue) VALUES (4, 'red', NULL);
INSERT INTO public.colours (id, name, colourvalue) VALUES (5, 'royalblue', NULL);
INSERT INTO public.colours (id, name, colourvalue) VALUES (6, 'green', NULL);
INSERT INTO public.colours (id, name, colourvalue) VALUES (7, 'skyblue', NULL);
INSERT INTO public.colours (id, name, colourvalue) VALUES (8, 'pink', NULL);


--
-- Name: colours_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bruno
--

SELECT pg_catalog.setval('public.colours_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

\unrestrict C8sUVfhZOzGAaafIwd4lasYwCxrZpgNsNgPIA7uUgewduTTAAqHwP8z6fa4vJdy

