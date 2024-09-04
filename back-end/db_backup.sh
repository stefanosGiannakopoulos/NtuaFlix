#!/bin/bash

OUTPUT_SQL=db_dump.sql

source .env

PGPASSWORD=$DB_PASSWORD pg_dump -U $DB_USERNAME -d $DB_DATABASE -h $DB_HOST -c --if-exists --no-acl --no-owner >$OUTPUT_SQL

