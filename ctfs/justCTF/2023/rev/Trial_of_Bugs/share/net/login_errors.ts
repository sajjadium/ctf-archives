export const LOGIN_ERROR_INVALID_TOKEN = 'INVALID_TOKEN';
export const LOGIN_ERROR_PLAYER_LIMIT = 'PLAYER_LIMIT';
export const LOGIN_ERROR_SESSION_IP_LIMIT = 'IP_SESSION_LIMIT';
export const LOGIN_ERROR_DATABASE = 'DATABASE';


export const LOGIN_ERROR_TEXT: {[key: string]: string} = {
    [LOGIN_ERROR_INVALID_TOKEN]: 'Invalid game token',
    [LOGIN_ERROR_PLAYER_LIMIT]: 'Too many players on this server. Please try again later (or change your server).',
    [LOGIN_ERROR_SESSION_IP_LIMIT]: 'Too many connections from this IP address.',
    [LOGIN_ERROR_DATABASE]: 'Failed to load data from the database'
}
