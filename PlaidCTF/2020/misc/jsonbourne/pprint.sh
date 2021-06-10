#!/usr/bin/env bash

source ./parser.sh

RED="\e[38;5;1m"
GREEN="\e[38;5;2m"
YELLOW="\e[38;5;3m"
BLUE="\e[38;5;4m"
PURPLE="\e[38;5;5m"

CLEAR="\e[0m"

TAB="  "

indent() {
    local res=$1
    local d=$2
    local t=0
    for (( t=0; t < $d; t++ )); do
        eval $res='"${!res}${TAB}"'
    done
}

printString() {
    local strval=$1
    local d=$2
    local res=$3
    local color=$4

    local override_color
    eval 'override_color=${'$strval'[_color]}'

    if [[ "$override_color" != "" ]]; then
        local color_var="${!override_color}"
        color="${!color_var}"
    fi

    eval $res='"${!res}${color}\"${!strval}\"${CLEAR}"'
}

printNumber() {
    local numval=$1
    local d=$2
    local res=$3

    eval $res='${!res}${GREEN}${numval}${CLEAR}'
}


printArray() {
    local array=$1
    local d=$2
    local res=$3
    local len
    local i=0
    eval 'len=${#'$array'[@]}'
    len=$((len-1))
    eval $res='"${!res}[\\n"'
    for (( i=i; i < $len; i++ )); do
        indent "$res" $((d+1))
        makeVar
        local next_res=$var_name
        local next_val
        eval 'next_val=${'$array'['$i']}'
        print "$next_val" $((d+1)) "$res"
        if [[ "$i" = "$((len-1))" ]]; then
            eval $res='"${!res}\\n"'
        else
            eval $res='"${!res},\\n"'
        fi
    done
    indent "$res" $d
    eval $res='"${!res}]"'
}

printObject() {
    local obj=$1
    local d=$2
    local res=$3
    local keys
    local key
    local len
    local i=0

    eval 'keys=("${!'$obj'[@]}")'
    eval 'len=${#'$obj'[@]}'
    eval $res='"${!res}{\\n"'

    for key in "${keys[@]}"; do
        if [[ "${key}" = "_type" ]]; then
            continue
        fi

        indent "$res" $((d+1))

        printString "${key}" $d "${res}" "$BLUE"

        eval $res='"${!res}: "'

        makeVar
        local next_res=$var_name
        local next_val
        eval 'next_val=${'$obj'[${key}]}'
        print "$next_val" $((d+1)) "$res"
        if [[ "$i" = "$((len-2))" ]]; then
            eval $res='"${!res}\\n"'
        else
            eval $res='"${!res},\\n"'
        fi

        i=$((i+1))
    done
    indent "$res" $d
    eval $res='"${!res}}"'
}

print() {
    local kind_key
    local kind
    eval 'kind_key=${'$1'["_type"]}'
    eval 'kind=${!'$kind_key'}'
    local d=$2
    local res=$3
    if [[ "$kind" = "$STRING" ]]; then
        printString "$1" "$d" "$res" "$YELLOW"
    fi

    if [[ "$kind" = "$NUMBER" ]]; then
        local numptr
        eval 'numptr=${'$1'[0]}'
        printNumber $numptr $d $res
    fi

    if [[ "$kind" = "$ARRAY" ]]; then
        printArray $1 $d $res
    fi

    if [[ "$kind" = "$OBJECT" ]]; then
        printObject $1 $d $res
    fi
}

pprint() {
    unset result
    unset pretty_result
    pretty_result=""
    parser "$1" 0 result
    print result 0 pretty_result
    echo -e "$pretty_result"
}

read input
pprint "$input"
