#!/bin/bash

if [ "${1}" = "" ]; then
    echo "ERROR: an option (create, read, or delete) is required as the first argument"
    exit 1
fi

if [ "${1}" = "create" ]; then
    python3 create.py $2 $3 $4 $5
    exit 0
fi

if [ "${1}" = "read" ]; then
    python3 read.py $2
    exit 0
fi

if [ "${1}" = "update" ]; then
    python3 update.py $2 $3 $4 $5
    exit 0
fi

if [ "${1}" = "delete" ]; then
    python3 delete.py $2
    exit 0
fi

echo "ERROR: invalid option $1, expected create, read, or delete"
exit 1

