--
-- PostgreSQL database dump
--

\restrict MfW6dT96XCnpyvYbybRhsM2hW77JwLSg4K2HhapucgzMQLZQMlSaZJJGDZVLkLl

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
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: bruno
--

INSERT INTO public.categories (id, name, name_pl) VALUES (1, 'Umbrella', 'Parasol');
INSERT INTO public.categories (id, name, name_pl) VALUES (2, 'Coat / Jacket', 'Kurtka');
INSERT INTO public.categories (id, name, name_pl) VALUES (3, 'Phone', 'Telefon');
INSERT INTO public.categories (id, name, name_pl) VALUES (4, 'Other', 'Inne');


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bruno
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

\unrestrict MfW6dT96XCnpyvYbybRhsM2hW77JwLSg4K2HhapucgzMQLZQMlSaZJJGDZVLkLl

