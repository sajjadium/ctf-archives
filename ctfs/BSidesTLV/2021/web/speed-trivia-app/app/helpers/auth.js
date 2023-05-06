const jwt  = require('jsonwebtoken')
const uuid = require('uuid-random');

const { db, NON_ZERO, DEFAULT_TTL } = require('./db_ops')

const ACCESS_TOKEN_SECRET = process.env.JWT_SECRET || 'demo-env-secret'



// auth utils 

function genJWT(userObj) {
    return jwt.sign(userObj, ACCESS_TOKEN_SECRET, { expiresIn: `${DEFAULT_TTL}s` }); 
}

async function is_active(gameId) {
    const score = await db.get_field(gameId, db.FIELDS.SCORE);
    if(score < NON_ZERO) {
        return false;
    } else {
        return true;
    }
}

// auth controllers / middlewares

async function start_session (req, res, next) {
    const gameObj = { gameId: uuid() };
    const accessToken = genJWT(gameObj);
    await db.new_game(gameObj.gameId);
    return res.json({ accessToken: accessToken })
}

async function validate_jwt(req, res, next) {
    const authHeader = req.headers['authorization']
    const token = authHeader && authHeader.split(' ')[1]
    if (token == null) return res.sendStatus(401)
    
    await jwt.verify(token, ACCESS_TOKEN_SECRET, async (err, user) => {
        if(!err) {
            const live_session = await is_active(user.gameId);
            console.log(`LIVE SESSION :: ` , live_session)
            if (!live_session) {
                res.status(403);
                return res.json({error: 'session is over'});
            } else { // session still exists in the DB
                req.user = user;
                return next();
            }
        } else { // invalid JWT
            res.status(403)
            return res.json({error: 'invalid/expired JWT'})
        }
    });
    return ;
  }


const authControls = {
    validate_jwt,
    start_session,
 }

module.exports = { authControls }