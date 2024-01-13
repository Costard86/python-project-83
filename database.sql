CREATE TABLE IF NOT EXISTS public.urls
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT urls_pkey PRIMARY KEY (id)
);

CREATE TABLE url_checks(
    id serial PRIMARY KEY,
    url_id int REFERENCES urls (id) ON DELETE CASCADE,
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at timestamp
);