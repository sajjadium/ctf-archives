source ./helpers.sh

parseString() {
    local input=$1
    local i=$2
    local res=$3
    declare -Ag $res

    makeVar
    eval ${res}'[_type]=$var_name'
    makeKind "STRING" $var_name

    getString "$input" "$i" "$res"

    local task_i
    local result_str="${!res}"
    for (( task_i=0; task_i < ${#result_str}; task_i++ )); do
        if [[ "${result_str:$task_i:5}" = "task " ]]; then
            local suffix="${result_str:$((task_i+5)):$((${#result_str}-task_i-5))}"
            if [[ "$((suffix > 0))" = "1" && "$((suffix <= 8))" = "1" ]]; then
                local color=$var_name
                normalizeNumber "$suffix" $color "var_"
                eval ${res}'[_color]=${color}'
            fi
        fi
    done
}

parseNumber() {
    local input=$1
    local i=$2
    local res=$3
    declare -Ag "$res"

    makeVar
    local kind_var=$var_name
    eval ${res}'[_type]=$kind_var'
    makeKind "NUMBER" $kind_var


    for (( i=i; i < ${#input}; i++ )); do
        if [[ "${input:$i:1}" =~ [0-9] ]]; then
            eval $res='"${!res}${input:$i:1}"'
        else
            break
        fi
    done

    normalizeNumber "${!res}" "$res" ""
    resultI=$i

}

parseArray() {
    local input=$1
    local i=$2
    local res=$3
    declare -Ag $res

    makeVar
    local kind_var=$var_name
    eval ${res}'[_type]=$kind_var'
    makeKind "ARRAY" $kind_var

    i=$((i+1))
    local index=0
    for (( i=i; i < ${#input}; i++ )); do
        consumeWhitespace "$input" "$i"
        i=$resultI

        if [[ "${input:$i:1}" = "]" ]]; then
            resultI=$((i+1))
            return
        fi

        makeVar
        local next_val=$var_name

        parser "$input" "$i" "$next_val"
        i=$resultI
        eval ${res}'[$index]=${next_val}'
        index=$((index+1))

        consumeWhitespace "$input" "$i"
        i=$resultI

        if [[ "${input:$i:1}" = "," ]]; then
            continue
        fi

        if [[ "${input:$i:1}" = "]" ]]; then
            resultI=$((i+1))
            return
        fi

        echo "Invalid array at char $2 (${input:$i:1})"
        echo "Case 1"
    done

    echo "Invalid array at char $2"
    echo "Case 2"
}

parseObject() {
    local input=$1
    local i=$2
    local res=$3
    declare -Ag $res

    makeVar
    local kind_var=$var_name
    eval ${res}'[_type]=$kind_var'
    makeKind "OBJECT" $kind_var


    i=$((i+1))
    for (( i=i; i < ${#input}; i++ )); do
        consumeWhitespace "$input" "$i"
        i=$resultI

        if [[ "${input:$i:1}" = "}" ]]; then
            resultI=$((i+1))
            return
        fi

        makeVar
        local next_key=$var_name
        makeVar
        local next_val=$var_name

        parseString "$input" "$i" "$next_key"
        i=$resultI

        consumeWhitespace "$input" "$i"
        i=$resultI

        if [[ "${input:$i:1}" != ":" ]]; then
            echo "Bad object definition at char $2 (expected : got ${input:$i:1})"
            return
        fi
        i=$((i+1))

        consumeWhitespace "$input" "$i"
        i=$resultI

        parser "$input" "$i" "$next_val"
        i=$resultI

        consumeWhitespace "$input" "$i"
        i=$resultI

        eval ${res}'["${next_key}"]="${next_val}"'

        if [[ "${input:$i:1}" = "," ]]; then
            continue
        fi

        if [[ "${input:$i:1}" = "}" ]]; then
            resultI=$((i+1))
            return
        fi

        echo "Invalid object at char $2 (${input:$i:1})"
    done

    echo "Invalid object at char $2"
}

parser() {
    local input=$1
    local i=$2
    local res=$3
    for (( i=i; i<${#input}; i++ )); do
        consumeWhitespace "$input" "$i"
        i=$resultI

        if [[ "${input:$i:1}" = "\"" ]]; then
            parseString "$input" "$i" "$res"
            return
        fi
        if [[ "${input:$i:1}" =~ [0-9] ]]; then
            parseNumber "$input" "$i" "$res"
            return
        fi
        if [[ "${input:$i:1}" = "[" ]]; then
            parseArray "$input" "$i" "$res"
            return
        fi
        if [[ "${input:$i:1}" = "{" ]]; then
            parseObject "$input" "$i" "$res"
            return
        fi

        echo "Unexpected token at char $i (${input:$i:1})"
        return
    done
}
