import { useState, useEffect } from 'react';
import { Contract, providers } from 'ethers';
import { Modal, Button } from '@mantine/core';
import { useUser } from 'components/context/UserContext';
import { isServer } from 'util/ssr';
import { TotallySecureDapp__factory as factory } from 'ethtypes/factories/TotallySecureDapp__factory';
import type { TotallySecureDapp } from 'ethtypes/TotallySecureDapp';

type ContractAddress = Record<string, string>;

const CHAIN_ID = 3; // Ropsten, https://docs.metamask.io/guide/ethereum-provider.html#chain-ids

export default function ConnectModal() {
    const { user, dispatchUser } = useUser();
    const [modalOpen, setModalOpen] = useState(isServer ? false : !user.active);
    const [fetchErr, setFetchErr] = useState('');
    const connect = async () => {
        if (isServer) return;
        if (typeof window.ethereum === 'undefined') {
            dispatchUser({ active: false, noWallet: true });
            return;
        }
        window.ethereum.request({ method: 'eth_requestAccounts' }).then(async (accounts) => {
            const account = (accounts as Array<string>)[0];
            const provider = new providers.Web3Provider(
                window.ethereum as unknown as providers.ExternalProvider
            );
            const { chainId } = await provider.getNetwork();
            const active = chainId === CHAIN_ID;
            const contractAddress = await getContractAddr(account);
            const contract = new Contract(contractAddress, factory.abi, provider.getSigner());
            dispatchUser({
                active: active,
                noWallet: false,
                provider: provider,
                address: account,
                chainId: chainId,
                contract: contract as TotallySecureDapp,
            });
            setModalOpen(!active);
        });
    };
    const setChain = async () => {
        if (isServer || typeof window.ethereum === 'undefined') return;
        window.ethereum
            .request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: `0x${CHAIN_ID}` }],
            })
            .catch((err) => {
                // Chain not added to MetaMask
                if (err.code === 4902) return;
            });
    };
    const getContractAddr = async (usrAddr: string): Promise<string> => {
        const storageValue = window.localStorage.getItem('contract-addresses');
        const addresses: ContractAddress = storageValue === null ? {} : JSON.parse(storageValue);
        if (addresses[usrAddr]) return addresses[usrAddr];
        const res = await window.fetch(`/api/contract/${usrAddr}`);
        const { contractAddress, id, error } = await res.json();
        if (!res.ok) {
            setFetchErr(error);
            return '';
        }
        setFetchErr('');
        addresses[usrAddr] = contractAddress;
        window.localStorage.setItem('contract-addresses', JSON.stringify(addresses));
        window.localStorage.setItem('user-id', id);
        return contractAddress;
    };
    // Show modal when disconnected / on wrong network
    useEffect(() => {
        const onAccountsChanged = async (accounts: Array<string>) => {
            {
                const n = accounts.length;
                const active = !!n && user.chainId === CHAIN_ID;
                const contractAddress = await getContractAddr(accounts[0]);
                const contract = new Contract(
                    contractAddress,
                    factory.abi,
                    user.provider?.getSigner()
                );
                dispatchUser({
                    active: active,
                    address: accounts[0],
                    contract: contract as TotallySecureDapp,
                });
                setModalOpen(!active);
            }
        };
        const onChainChanged = (chainId: string) => {
            const id = parseInt(chainId);
            const active = !!user.address && id === CHAIN_ID;
            dispatchUser({ active: active, chainId: id });
            setModalOpen(!active);
        };
        window.ethereum?.on('accountsChanged', onAccountsChanged as any);
        window.ethereum?.on('chainChanged', onChainChanged as any);
        return () => {
            window.ethereum?.removeListener('accountsChanged', onAccountsChanged);
            window.ethereum?.removeListener('chainChanged', onChainChanged);
        };
    }, [user, dispatchUser]);
    // Try to connect to wallet on page load
    useEffect(() => {
        connect();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    return (
        <>
            <Modal
                opened={modalOpen}
                onClose={() => {
                    if (user.active) setModalOpen(false);
                }}
                title={
                    /* eslint-disable indent */
                    user.noWallet
                        ? 'Please install MetaMask wallet'
                        : !user.address
                        ? 'Please connect your MetaMask wallet'
                        : 'Please set your network to Ropsten'
                    /* eslint-enable indent */
                }
                withCloseButton={false}
                centered
            >
                <Button
                    onClick={
                        /* eslint-disable indent */
                        user.noWallet
                            ? () => window.open('https://metamask.io/', '_blank')
                            : !user.address
                            ? connect
                            : setChain
                        /* eslint-enable indent */
                    }
                >
                    {
                        /* eslint-disable indent */
                        user.noWallet
                            ? 'Get MetaMask'
                            : !user.address
                            ? 'Connect wallet'
                            : 'Change chain'
                        /* eslint-enable indent */
                    }
                </Button>
            </Modal>
            <Modal
                opened={!!fetchErr.length}
                onClose={() => undefined}
                title={`Server responded with error ${fetchErr}`}
                withCloseButton={false}
                centered
            >
                <Button onClick={isServer ? () => undefined : () => window.location.reload()}>
                    Reload page
                </Button>
            </Modal>
        </>
    );
}
