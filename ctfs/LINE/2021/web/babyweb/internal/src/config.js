import { v4 as uuidv4 } from 'uuid';

let CONFIG = {};
CONFIG.secret = uuidv4();
CONFIG.admin = {
    username: process.env['USERNAME_ADMIN'],
    password: process.env['PASSWORD_ADMIN']
}
CONFIG.header = {
    username: process.env['USERNAME_HEADER'],
    password: process.env['PASSWORD_HEADER']
}
CONFIG.flag = process.env['FLAG']

export { CONFIG };
