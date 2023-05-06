const { randomInt } = require('crypto');
const { connect, prepare } = require('./db');

const transactions = {};

function generateId() {
    return randomInt(2**48 - 1);
}

module.exports = async (app) => {
    const db = await connect();

    async function makeTransaction(username, txId, asset, amount) {
        const query = prepare('INSERT INTO transactions (id, asset, amount, username) VALUES (:txId, :asset, :amount, :username)', {
            amount,
            asset,
            username,
            txId,
        });
    
        await db.query(query);
    }

    app.get('/api/transactions/:id', async (req, res) => {
        const txId = Number(req.params.id);
        if (!isFinite(txId)) {
            return res.status(400).send('invalid transaction id');
        }

        const transaction = await db.query(prepare('SELECT * FROM transactions WHERE id=:txId', {
            txId,
        }));
        
        if (transaction.rowCount > 0) {
            res.json(transaction.rows[0]);
        } else {
            res.status(404).send('no such transaction');
        }
    });

    app.put('/api/priv/assets/:asset/:action', async (req, res) => {
        const { username } = req.user
        
        const { asset, action } = req.params;
        if (/[^A-z]/.test(asset)) {
            return res.status(400).send('asset name must be letters only');
        }
        const assetTransactions = transactions[asset] ?? (transactions[asset] = {});
        
        const txId = generateId();
        assetTransactions[txId] = action;
        
        try {
            await makeTransaction(username, txId, asset, action === 'buy' ? 1 : -1);
            res.json({ id: txId });
        } catch (error) {
            console.error('db error:', error.message);
            res.status(500).send('transaction failed');
        } finally {
            delete assetTransactions[txId];
        }
    });
};
