#!/usr/bin/env bash

function print_header() {
    printf '#%.0s' {1..72}; echo
    echo -e "# $1"
    printf '#%.0s' {1..72}; echo
}

print_header "DROP TABLES EXT_OVAPI_NL_LINES and OVAPI_NL_LINES"
bq --location=eu query --use_legacy_sql=false < ./src/libraries/sql/ddl/reset_tables.sql

source run_ddl.sh
