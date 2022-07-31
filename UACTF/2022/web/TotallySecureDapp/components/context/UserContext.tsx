import { createContext, useReducer, useContext } from 'react';
import { providers } from 'ethers';
import type { ReactNode } from 'react';
import type { TotallySecureDapp } from 'ethtypes/TotallySecureDapp';

interface UserContextProps {
    children: ReactNode;
}

type UserState = {
    active: boolean;
    noWallet?: boolean;
    provider?: providers.Web3Provider;
    address?: string;
    chainId?: number;
    contract?: TotallySecureDapp;
};
type UserData = Partial<UserState>;
type UserDispatch = (action: UserData) => void;
type UserContextT = { user: UserState; dispatchUser: UserDispatch };

function userReducer(user: UserState, data: UserData): UserState {
    return { ...user, ...data };
}

const UserContext = createContext<UserContextT | undefined>(undefined);

export function useUser() {
    const context = useContext(UserContext);
    if (context === undefined) throw new Error('useUser must be used within a UserProvider');
    return context;
}

export default function UserProvider(props: UserContextProps) {
    const { children } = props;
    const [user, dispatchUser] = useReducer(userReducer, { active: false });
    const value = { user, dispatchUser };
    return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}
