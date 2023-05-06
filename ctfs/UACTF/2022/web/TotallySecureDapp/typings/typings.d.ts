export {};

declare global {
    interface Window {
        ethereum?: import('@metamask/providers').MetaMaskInpageProvider;
    }
}
