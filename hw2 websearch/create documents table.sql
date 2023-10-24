-- Table: public.documents

-- DROP TABLE IF EXISTS public.documents;

CREATE TABLE IF NOT EXISTS public.documents
(
    dnumb integer NOT NULL,
    dtext text COLLATE pg_catalog."default" NOT NULL,
    dtitle text COLLATE pg_catalog."default" NOT NULL,
    ddate text COLLATE pg_catalog."default" NOT NULL,
    numb_chars integer NOT NULL,
    catid integer NOT NULL,
    CONSTRAINT documents_pkey PRIMARY KEY (dnumb)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to postgres;