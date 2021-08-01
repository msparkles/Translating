#!/bin/sh

function find_latest_recursively() {
    read in
    echo $(find $in -type f -printf '%TY%Tm%Td%TH%TM\n' | sort -n | tail -1) $in
}

function change_time() {
    read -r time file
    touch -t $time $file
}

function find_and_change_time() {
    while read -r line; do
        echo $line | find_latest_recursively | change_time
    done
}

find ./docs -type d \
| awk '{ print length, $0 }' \
| sort -n -s -r \
| cut -d" " -f2- \
| find_and_change_time
