CREATE TABLE IF NOT EXISTS public.urls
(
    id bigint NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT urls_pkey PRIMARY KEY (id)
)
