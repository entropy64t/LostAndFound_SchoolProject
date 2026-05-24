--
-- PostgreSQL database dump
--

\restrict yvwVGFGNS7P5FhVR0ysy1asJEyFp0ttSISgh55qmerKIEoI7cY0wXXDsIABBiZU

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
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.grades (id, name) VALUES (1, 'Staff');

INSERT INTO public.grades (id, name) VALUES (2, '1A');
INSERT INTO public.grades (id, name) VALUES (3, '1B');
INSERT INTO public.grades (id, name) VALUES (4, '1C');
INSERT INTO public.grades (id, name) VALUES (5, '1D');
INSERT INTO public.grades (id, name) VALUES (6, '1E');
INSERT INTO public.grades (id, name) VALUES (7, '1F');
INSERT INTO public.grades (id, name) VALUES (8, '1G');
INSERT INTO public.grades (id, name) VALUES (9, '1H');

INSERT INTO public.grades (id, name) VALUES (10, '2A');
INSERT INTO public.grades (id, name) VALUES (11, '2B');
INSERT INTO public.grades (id, name) VALUES (12, '2C');
INSERT INTO public.grades (id, name) VALUES (13, '2D');
INSERT INTO public.grades (id, name) VALUES (14, '2E');
INSERT INTO public.grades (id, name) VALUES (15, '2F');
INSERT INTO public.grades (id, name) VALUES (16, '2G');
INSERT INTO public.grades (id, name) VALUES (17, '2H');

INSERT INTO public.grades (id, name) VALUES (18, '3A');
INSERT INTO public.grades (id, name) VALUES (19, '3B');
INSERT INTO public.grades (id, name) VALUES (20, '3C');
INSERT INTO public.grades (id, name) VALUES (21, '3D');
INSERT INTO public.grades (id, name) VALUES (22, '3E');
INSERT INTO public.grades (id, name) VALUES (23, '3F');
INSERT INTO public.grades (id, name) VALUES (24, '3G');
INSERT INTO public.grades (id, name) VALUES (25, '3H');

INSERT INTO public.grades (id, name) VALUES (26, '4A');
INSERT INTO public.grades (id, name) VALUES (27, '4B');
INSERT INTO public.grades (id, name) VALUES (28, '4C');
INSERT INTO public.grades (id, name) VALUES (29, '4D');
INSERT INTO public.grades (id, name) VALUES (30, '4E');
INSERT INTO public.grades (id, name) VALUES (31, '4F');
INSERT INTO public.grades (id, name) VALUES (32, '4G');
INSERT INTO public.grades (id, name) VALUES (33, '4H');


--
-- Name: grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grades_id_seq', 5, true);


--
-- PostgreSQL database dump complete
--

\unrestrict yvwVGFGNS7P5FhVR0ysy1asJEyFp0ttSISgh55qmerKIEoI7cY0wXXDsIABBiZU

