STRING=string
OBJECT=object
NUMBER=number
ARRAY=array

var_1="\033[38;5;5m"
var_2="\033[38;5;2m"
var_3="\033[38;5;1m"
var_4="\033[38;5;6m"
var_5="\033[38;5;13m"
var_6="\033[38;5;10m"
var_7="\033[38;5;9m"
var_8="\033[38;5;14m"

_var_name_i=8

makeVar() {
    _var_name_i=$((_var_name_i+1))
    var_name="var_$_var_name_i"
    eval "unset $var_name"
}

makeKind() {
    local kind=$1
    local res=$2

    eval $res'=$kind'
}


consumeWhitespace() {
    local input=$1
    local i=$2
    for (( i=i; i < ${#input}; i++ )); do
        if  [[ "${input:$i:1}" != " " && "${input:$i:1}" != "\t" && "${input:$i:1}" != "\n" ]]; then
            resultI=$i
            return
        fi
    done
}

normalizeNumber() {
    local input="$1"
    local res=$2
    local prefix=$3
    local i

    local found_first=0

    eval $res='"$prefix"'
    for (( i=0; i < ${#input}; i++ )); do
        if [[ "${input:$i:1}" = "0" && "$found_first" = "0" ]]; then
            continue
        fi
        found_first=1
        eval $res='${!res}${input:$i:1}'
    done

    if [[ "$found_first" = "0" ]]; then
        eval $res='${!res}0'
    fi
}

getString() {
    local input=$1
    local i=$2
    local res=$3
    declare -Ag $res

    i=$((i+1))
    for (( i=i; i < ${#input}; i++ )); do
        if [[ "${input:$i:1}" = "\\" ]]; then
            echo "Escape characters not supported"
            continue
        fi
        if [[ "${input:$i:1}" = "\"" ]]; then
            resultI=$((i+1))
            return
        fi
        eval $res='"${!res}${input:$i:1}"'
    done

    echo "Invalid string: $2"
}

