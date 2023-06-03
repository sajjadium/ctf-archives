import {useEffect, useState} from "react";
import {ObservableField} from "../../share/util/observable_field";

export function useObservableField<T>(f?: ObservableField<T>|null|undefined) {
    const [value, setValue] = useState(f?.get());
    useEffect(() => {
        if (value !== f?.get())
            setValue(f?.get());
        f?.addCallback(setValue);
        return () => f?.removeCallback(setValue);
    }, [f]);
    return f?.get();
}
