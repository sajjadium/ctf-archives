-- Make sure tenants can change table ownership

CREATE DOMAIN whoami AS NAME
CHECK (VALUE = CURRENT_USER);

CREATE PROCEDURE chown (_tbl regclass, _owner regrole, _caller whoami DEFAULT CURRENT_USER)
    LANGUAGE plpgsql
    SECURITY DEFINER
AS $$
DECLARE
    current_owner regrole;
BEGIN
    SELECT tableowner FROM pg_tables WHERE tablename = _tbl::text
        INTO current_owner;

    IF (_caller::text != current_owner::text) THEN
        RAISE EXCEPTION 'Only the current owner (%) can change table ownership!', current_owner;
    ELSE
        EXECUTE format('ALTER TABLE %s OWNER TO %s', _tbl, _owner);
    END IF;
END
$$;
