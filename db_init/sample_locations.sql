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

INSERT INTO public.locations (id, building_level, name) VALUES (1, -1, '03');
INSERT INTO public.locations (id, building_level, name) VALUES (2, -1, '02');
INSERT INTO public.locations (id, building_level, name) VALUES (3, -1, '01');
INSERT INTO public.locations (id, building_level, name) VALUES (4, -1, 'kantorek siłowni');
INSERT INTO public.locations (id, building_level, name) VALUES (5, -1, 'siłownia');
INSERT INTO public.locations (id, building_level, name) VALUES (6, -1, 'szatnia przy siłowni');
INSERT INTO public.locations (id, building_level, name) VALUES (7, -1, 'inf2');
INSERT INTO public.locations (id, building_level, name) VALUES (8, -1, '04');
INSERT INTO public.locations (id, building_level, name) VALUES (9, -1, 'inf1');
INSERT INTO public.locations (id, building_level, name) VALUES (10, -1, 'hallway');
INSERT INTO public.locations (id, building_level, name) VALUES (11, 0, 'gim1');
INSERT INTO public.locations (id, building_level, name) VALUES (12, 0, 'aerobik');
INSERT INTO public.locations (id, building_level, name) VALUES (13, 0, 'dzeidziniec');
INSERT INTO public.locations (id, building_level, name) VALUES (14, 0, 'kantyna');
INSERT INTO public.locations (id, building_level, name) VALUES (15, 0, '13C');
INSERT INTO public.locations (id, building_level, name) VALUES (16, 0, '13B');
INSERT INTO public.locations (id, building_level, name) VALUES (17, 0, '13A');
INSERT INTO public.locations (id, building_level, name) VALUES (18, 0, '13');
INSERT INTO public.locations (id, building_level, name) VALUES (19, 0, 'biblioteka');
INSERT INTO public.locations (id, building_level, name) VALUES (20, 0, 'czytelnia');
INSERT INTO public.locations (id, building_level, name) VALUES (21, 0, 'gabinet psychologa');
INSERT INTO public.locations (id, building_level, name) VALUES (22, 0, 'gabinet pedagoga');
INSERT INTO public.locations (id, building_level, name) VALUES (23, 0, 'sekretariat');
INSERT INTO public.locations (id, building_level, name) VALUES (24, 0, '5');
INSERT INTO public.locations (id, building_level, name) VALUES (25, 0, 'pokój nauczycieli angielskiego');
INSERT INTO public.locations (id, building_level, name) VALUES (26, 0, '3');
INSERT INTO public.locations (id, building_level, name) VALUES (27, 0, '2');
INSERT INTO public.locations (id, building_level, name) VALUES (28, 0, '1');
INSERT INTO public.locations (id, building_level, name) VALUES (29, 0, 'hallway');
INSERT INTO public.locations (id, building_level, name) VALUES (30, 1, '26');
INSERT INTO public.locations (id, building_level, name) VALUES (31, 1, '25');
INSERT INTO public.locations (id, building_level, name) VALUES (32, 1, '24');
INSERT INTO public.locations (id, building_level, name) VALUES (33, 1, 'pokój nauczycieli matematyki');
INSERT INTO public.locations (id, building_level, name) VALUES (34, 1, '23');
INSERT INTO public.locations (id, building_level, name) VALUES (35, 1, 'pokój nauczycieli fizyki');
INSERT INTO public.locations (id, building_level, name) VALUES (36, 1, '22');
INSERT INTO public.locations (id, building_level, name) VALUES (37, 1, '21');
INSERT INTO public.locations (id, building_level, name) VALUES (38, 1, '20');
INSERT INTO public.locations (id, building_level, name) VALUES (39, 1, '19');
INSERT INTO public.locations (id, building_level, name) VALUES (40, 1, 'pokój nauczycieli biologii');
INSERT INTO public.locations (id, building_level, name) VALUES (41, 1, '17');
INSERT INTO public.locations (id, building_level, name) VALUES (42, 1, '18');
INSERT INTO public.locations (id, building_level, name) VALUES (43, 1, '16');
INSERT INTO public.locations (id, building_level, name) VALUES (44, 1, '15');
INSERT INTO public.locations (id, building_level, name) VALUES (45, 1, '14');
INSERT INTO public.locations (id, building_level, name) VALUES (46, 1, 'hallway');
INSERT INTO public.locations (id, building_level, name) VALUES (47, 2, '37');
INSERT INTO public.locations (id, building_level, name) VALUES (48, 2, '36');
INSERT INTO public.locations (id, building_level, name) VALUES (49, 2, '35');
INSERT INTO public.locations (id, building_level, name) VALUES (50, 2, 'sekretariat');
INSERT INTO public.locations (id, building_level, name) VALUES (51, 2, 'pokój nauczycielski');
INSERT INTO public.locations (id, building_level, name) VALUES (52, 2, 'aula');
INSERT INTO public.locations (id, building_level, name) VALUES (53, 2, '32');
INSERT INTO public.locations (id, building_level, name) VALUES (54, 2, '29');
INSERT INTO public.locations (id, building_level, name) VALUES (55, 2, '31');
INSERT INTO public.locations (id, building_level, name) VALUES (56, 2, '28');
INSERT INTO public.locations (id, building_level, name) VALUES (57, 2, '27');
INSERT INTO public.locations (id, building_level, name) VALUES (58, 2, 'hallway');


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bruno
--

SELECT pg_catalog.setval('public.locations_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

\unrestrict BlTsxHr7hgf9IAnX99KxJtJiktMqkW8MYo84TwY70IagL2T9QRZrWf7pvWEjbmJ

