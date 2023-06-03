import {
    ID_LOGIN_REQUEST, ID_LOGIN_WHITELIST_KEY,
    ID_RPC_QUEUE_EXECUTE_DONE,
    ID_RPC_SHARED_EXECUTE
} from "./packet_ids";


const DO_RPC_SERVER_SCHEMA = {
    oneOf: [
        {
            type: 'array',
            items: [
                {
                    const: 'DialogueModel.completeDialogue'
                }
            ],
            minItems: 1,
            additionalItems: false
        },
        {
            type: 'array',
            items: [
                {
                    const: 'DialogueModel.completeChoice'
                },
                {
                    type: 'number'
                }
            ],
            minItems: 2,
            additionalItems: false
        },

        {
            type: 'array',
            items: [
                {
                    const: 'MapManager.clientTilesetLoaded'
                },
                {
                    type: 'string'
                }
            ],
            minItems: 2,
            additionalItems: false
        },
        {
            type: 'array',
            items: [
                {
                    const: 'MapManager.clientSpritesheetLoaded'
                },
                {
                    type: 'string'
                }
            ],
            minItems: 2,
            additionalItems: false
        },
        {
            type: 'array',
            items: [
                {
                    const: 'MapManager.tick'
                }
            ],
            minItems: 1,
            additionalItems: false
        },

        {
            type: 'array',
            items: [
                {
                    const: 'InputManager.setKey'
                },
                {
                    type: 'number'
                },
                {
                    type: 'number'
                },
                {
                    type: 'boolean'
                }
            ],
            minItems: 4,
            additionalItems: false
        }
    ]
}

export const NET_SERVER_SCHEMA: any = {
    definitions: {
        'RpcServerData': DO_RPC_SERVER_SCHEMA
    },

    anyOf: [
        {
            type: 'array',
            items: [
                {
                    type: 'integer',
                    const: ID_RPC_SHARED_EXECUTE
                },
                {
                    '$ref': '#/definitions/RpcServerData'
                }
            ],
            minItems: 2,
            additionalItems: false
        },
        {
            type: 'array',
            items: [
                {
                    type: 'integer',
                    const: ID_RPC_QUEUE_EXECUTE_DONE
                },
                {
                    type: 'null'
                }
            ],
            minItems: 2,
            additionalItems: false
        },

        {
            type: 'array',
            items: [
                {
                    type: 'integer',
                    const: ID_LOGIN_REQUEST
                },
                {
                    type: ["string", "null"]
                }
            ],
            minItems: 2,
            additionalItems: false
        },
        {
            type: 'array',
            items: [
                {
                    type: 'integer',
                    const: ID_LOGIN_WHITELIST_KEY
                },
                {
                    type: "string"
                }
            ],
            minItems: 2,
            additionalItems: false
        }
    ]
};
