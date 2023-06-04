module challenge::baby_otter_challenge {
    
    // [*] Import dependencies
    use std::vector;

    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{TxContext};

    // [*] Error Codes
    const ERR_INVALID_CODE : u64 = 31337;
 
    // [*] Structs
    struct Status has key, store {
        id : UID,
        solved : bool,
    }

    // [*] Module initializer
    fun init(ctx: &mut TxContext) {
        transfer::public_share_object(Status {
            id: object::new(ctx),
            solved: false
        });
    }

    // [*] Local functions
    fun gt() : vector<u64> {

        let table : vector<u64> = vector::empty<u64>();
        let i = 0;

        while( i < 256 ) {
            let tmp = i;
            let j = 0;

            while( j < 8 ) {
                if( tmp & 1 != 0 ) {
                    tmp = tmp >> 1;
                    tmp = tmp ^ 0xedb88320;
                } else {
                    tmp = tmp >> 1;
                };

                j = j+1;
            };

            vector::push_back(&mut table, tmp);
            i = i+1;
        };

        table
    }

    fun hh(input : vector<u8>) : u64 {

        let table : vector<u64> = gt();
        let tmp : u64 = 0xffffffff;
        let input_length = vector::length(&input);
        let i = 0;

        while ( i < input_length ) {
            let byte : u64 = (*vector::borrow(&mut input, i) as u64);

            let index = tmp ^ byte;
            index = index & 0xff;

            tmp = tmp >> 8;
            tmp = tmp ^ *vector::borrow(&mut table, index);

            i = i+1;
        };

        tmp ^ 0xffffffff
    }
 
    // [*] Public functions
    public entry fun request_ownership(status: &mut Status, ownership_code : vector<u8>, _ctx: &mut TxContext) {

        let ownership_code_hash : u64 = hh(ownership_code);
        assert!(ownership_code_hash == 1725720156, ERR_INVALID_CODE);
        status.solved = true;

    }

    public entry fun is_owner(status: &mut Status) {
        assert!(status.solved == true, 0);
    }

}
