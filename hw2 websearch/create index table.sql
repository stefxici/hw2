-- Table: public.index

-- DROP TABLE IF EXISTS public.index;

CREATE TABLE IF NOT EXISTS public.index
(
    count integer,
    tterm text COLLATE pg_catalog."default",
    ddnum integer,
    CONSTRAINT ddnum FOREIGN KEY (ddnum)
        REFERENCES public.documents (dnumb) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT tterm FOREIGN KEY (tterm)
        REFERENCES public.terms (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.index
    OWNER to postgres;