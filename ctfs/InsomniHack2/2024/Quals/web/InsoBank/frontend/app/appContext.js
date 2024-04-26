import { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export function AppWrapper({ children }) {
  let sharedState = {'API_ROOT': 'http://localhost:5000'}
	const [userid, setUserid] = useState(null);
	const [jwt, setJwt] = useState(null);
	const API_ROOT = "http://localhost:5000";
  return (
    <AppContext.Provider value={{ userid, setUserid, API_ROOT, jwt, setJwt }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  return useContext(AppContext);
}
