#!/bin/bash

source .env

commands=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USERNAME -d $DB_DATABASE -h $DB_HOST -t -c\
	"select 'drop table ' || tablename || ' cascade;' from pg_tables where schemaname='public'")
PGPASSWORD=$DB_PASSWORD psql -U $DB_USERNAME -d $DB_DATABASE -h $DB_HOST -t -c "$commands"

