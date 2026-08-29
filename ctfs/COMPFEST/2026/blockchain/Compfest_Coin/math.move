module challenge::math;

public fun mul_div_floor(value: u128, numerator: u128, denominator: u128): u128 {
    if (denominator == 0) {
        0
    } else {
        value * numerator / denominator
    }
}

public fun apply_fee_floor(amount: u64, fee_bps: u64): u64 {
    if (fee_bps == 0) {
        amount
    } else {
        ((amount as u128) - (amount as u128) * (fee_bps as u128) / 10000) as u64
    }
}

public fun min(a: u64, b: u64): u64 {
    if (a < b) { a } else { b }
}

public fun bytes_lt(left: &vector<u8>, right: &vector<u8>): bool {
    let mut i = 0;
    let left_len = left.length();
    let right_len = right.length();
    while (i < left_len && i < right_len) {
        if (left[i] < right[i]) { return true };
        if (left[i] > right[i]) { return false };
        i = i + 1;
    };
    left_len < right_len
}

public fun join_key(mut left: vector<u8>, right: vector<u8>): vector<u8> {
    left.push_back(124);
    left.append(right);
    left
}

public fun same_bytes(left: &vector<u8>, right: &vector<u8>): bool {
    left == right
}
