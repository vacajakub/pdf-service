DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'pdf') THEN

      RAISE NOTICE 'Role "pdf" already exists. Skipping.';
   ELSE
      CREATE USER api WITH ENCRYPTED PASSWORD 'pdf';
   END IF;
END
$do$;


DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_database
      WHERE  datname = 'pdf') THEN
      RAISE NOTICE 'DB "pdf" already exists. Skipping.';
   ELSE
      CREATE DATABASE  pdf;
   END IF;
END
$do$;


GRANT ALL PRIVILEGES ON DATABASE pdf TO pdf;




