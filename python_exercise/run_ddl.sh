#!/usr/bin/env bash

function print_header() {
    printf '#%.0s' {1..72}; echo
    echo -e "# $1"
    printf '#%.0s' {1..72}; echo
}

print_header "CREATE SCHEMA"
bq --location=eu query --use_legacy_sql=false < ./src/libraries/sql/ddl/create_schema.sql

print_header "CREATE TABLE OVAPI_NL_LINES"
bq --location=eu query --use_legacy_sql=false < ./src/libraries/sql/ddl/OVAPI_NL_LINES.sql
