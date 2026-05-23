--
-- PostgreSQL database dump
--

\restrict 7y5gHLh7y965H9nPr6opE75oBSmH3hsGoYks29QCf18C8o86OwDtdLrhRZLkD1c

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

INSERT INTO public.locations (id, buildinglevel, name) VALUES (1, 2, '35');
INSERT INTO public.locations (id, buildinglevel, name) VALUES (2, 1, '24');
INSERT INTO public.locations (id, buildinglevel, name) VALUES (3, 1, '21');


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bruno
--

SELECT pg_catalog.setval('public.locations_id_seq', 3, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 7y5gHLh7y965H9nPr6opE75oBSmH3hsGoYks29QCf18C8o86OwDtdLrhRZLkD1c

