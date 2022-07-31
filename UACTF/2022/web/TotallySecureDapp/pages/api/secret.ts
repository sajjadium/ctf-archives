import admin from 'firebase-admin';
import { Contract, getDefaultProvider } from 'ethers';
import { parseEther } from 'ethers/lib/utils';
import { TotallySecureDapp__factory as factory } from 'ethtypes/factories/TotallySecureDapp__factory';
import type { NextApiRequest, NextApiResponse } from 'next';
import type { TotallySecureDapp } from 'ethtypes/TotallySecureDapp';

type ReqData = {
    userAddress: string;
    contractAddress: string;
    userId: string;
};

type ResData = {
    flag?: string;
    error?: string;
};

export default async function handler(req: NextApiRequest, res: NextApiResponse<ResData>) {
    const { userAddress, contractAddress, userId } = req.body as ReqData;
    try {
        admin.initializeApp({
            credential: admin.credential.cert(
                JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT_KEY ?? '')
            ),
        });
    } catch {}
    const db = admin.firestore();
    try {
        const provider = getDefaultProvider('ropsten', {
            etherscan: process.env.ETHERSCAN_API_KEY,
        });
        const contract = new Contract(contractAddress, factory.abi, provider) as TotallySecureDapp;
        const owner = await contract._owner();
        const flagCaptured = await contract._flagCaptured();
        const balance = await provider.getBalance(contractAddress);
        if (owner === userAddress && flagCaptured && balance.gt(parseEther('0.005'))) {
            const ids = db.collection('users').doc('ids');
            if (!ids) {
                res.status(500).json({ error: 'Failed to load ids' });
                return;
            }
            const id = (await ids.get()).get(userAddress.toLowerCase());
            if (id !== userId) {
                res.status(401).json({ error: 'Unauthorised' });
                return;
            }
            const flag = process.env.FLAG;
            res.status(200).json({ flag: flag });
            return;
        }
        res.status(401).json({
            error: 'Unauthorised (This might also just be a Ropsten error. Retry this API request a couple times if you think you got it)',
        });
    } catch (err) {
        if ('code' in (err as any) && (err as any).code === 'CALL_EXCEPTION')
            res.status(500).json({
                error:
                    'Internal Error. The server failed to fetch data from the smart contract. ' +
                    'There is a very high chance this is simply because the contract is on the ' +
                    'Ropsten testnet which is unstable (this may happen quite often). Keep ' +
                    'sending API requests, one should eventually work',
            });
        else
            res.status(500).json({
                error: 'Internal error. Were the correct user and contract addresses and id supplied?',
            });
    }
}
