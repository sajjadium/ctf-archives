import { useState, useEffect } from 'react'

function useIsMounted() {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    return { isMounted: mounted };
}

export default useIsMounted;
