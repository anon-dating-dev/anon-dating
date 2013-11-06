/*
Users
*/

CREATE SEQUENCE users_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE TABLE IF NOT EXISTS users
(
  id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  external_id character varying NOT NULL UNIQUE,
  city_id integer NOT NULL,
  city_name character varying NOT NULL,
  gender smallint NOT NULL,
  profile json NOT NULL,
  CONSTRAINT users_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

/*
Relationships
*/

CREATE SEQUENCE relationships_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE TABLE IF NOT EXISTS relationships
(
  id integer NOT NULL DEFAULT nextval('relationships_id_seq'::regclass),
  first_id integer NOT NULL references users,
  second_id integer NOT NULL references users,
  level integer NOT NULL DEFAULT 1,
  CONSTRAINT relationships_pkey PRIMARY KEY (id),
  CONSTRAINT relationships_first_id_second_id_key UNIQUE (first_id, second_id)
)
WITH (
  OIDS=FALSE
);

CREATE SEQUENCE messages_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

CREATE TABLE IF NOT EXISTS massages
(
  id integer NOT NULL DEFAULT nextval('relationships_id_seq'::regclass),
  recipient_id integer NOT NULL references users,
  sender_id integer NOT NULL references users,
  text text NOT NULL,
  creation_date timestamp without time zone NOT NULL,
  CONSTRAINT massages_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
