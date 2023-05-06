const _abi = [
    {
        constant: true,
        inputs: [
            {
                name: '',
                type: 'uint256',
            },
        ],
        name: '_posts',
        outputs: [
            {
                name: 'title',
                type: 'string',
            },
            {
                name: 'content',
                type: 'string',
            },
        ],
        payable: false,
        stateMutability: 'view',
        type: 'function',
    },
    {
        constant: false,
        inputs: [
            {
                name: 'index',
                type: 'uint256',
            },
        ],
        name: 'removePost',
        outputs: [],
        payable: false,
        stateMutability: 'nonpayable',
        type: 'function',
    },
    {
        constant: true,
        inputs: [],
        name: 'nPosts',
        outputs: [
            {
                name: '',
                type: 'uint256',
            },
        ],
        payable: false,
        stateMutability: 'view',
        type: 'function',
    },
    {
        constant: true,
        inputs: [
            {
                name: '',
                type: 'uint256',
            },
        ],
        name: '_authors',
        outputs: [
            {
                name: '',
                type: 'address',
            },
        ],
        payable: false,
        stateMutability: 'view',
        type: 'function',
    },
    {
        constant: true,
        inputs: [],
        name: '_flagCaptured',
        outputs: [
            {
                name: '',
                type: 'bool',
            },
        ],
        payable: false,
        stateMutability: 'view',
        type: 'function',
    },
    {
        constant: false,
        inputs: [
            {
                name: 'title',
                type: 'string',
            },
            {
                name: 'content',
                type: 'string',
            },
        ],
        name: 'addPost',
        outputs: [],
        payable: false,
        stateMutability: 'nonpayable',
        type: 'function',
    },
    {
        constant: true,
        inputs: [],
        name: '_owner',
        outputs: [
            {
                name: '',
                type: 'address',
            },
        ],
        payable: false,
        stateMutability: 'view',
        type: 'function',
    },
    {
        constant: true,
        inputs: [],
        name: '_contractId',
        outputs: [
            {
                name: '',
                type: 'string',
            },
        ],
        payable: false,
        stateMutability: 'view',
        type: 'function',
    },
    {
        constant: false,
        inputs: [
            {
                name: 'index',
                type: 'uint256',
            },
            {
                name: 'title',
                type: 'string',
            },
            {
                name: 'content',
                type: 'string',
            },
        ],
        name: 'editPost',
        outputs: [],
        payable: false,
        stateMutability: 'nonpayable',
        type: 'function',
    },
    {
        constant: false,
        inputs: [],
        name: 'captureFlag',
        outputs: [],
        payable: false,
        stateMutability: 'nonpayable',
        type: 'function',
    },
    {
        constant: false,
        inputs: [
            {
                name: 'contractId',
                type: 'string',
            },
        ],
        name: 'initialize',
        outputs: [],
        payable: true,
        stateMutability: 'payable',
        type: 'function',
    },
    {
        payable: true,
        stateMutability: 'payable',
        type: 'fallback',
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                name: 'author',
                type: 'address',
            },
            {
                indexed: true,
                name: 'index',
                type: 'uint256',
            },
        ],
        name: 'PostPublished',
        type: 'event',
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                name: 'author',
                type: 'address',
            },
            {
                indexed: true,
                name: 'index',
                type: 'uint256',
            },
        ],
        name: 'PostEdited',
        type: 'event',
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                name: 'author',
                type: 'address',
            },
            {
                indexed: true,
                name: 'index',
                type: 'uint256',
            },
        ],
        name: 'PostRemoved',
        type: 'event',
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                name: 'capturer',
                type: 'address',
            },
        ],
        name: 'FlagCaptured',
        type: 'event',
    },
];
