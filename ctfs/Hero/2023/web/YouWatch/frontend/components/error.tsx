import { useState, useEffect } from "react";

type ContainerProps = {
    errorCode: string;
    errorMsg: string;
    type: string;
};

export default function Error(props: ContainerProps) {
    useEffect(() => {
        var error = (document.getElementById("error") as HTMLInputElement);
        error.checked = false;
    })

    return (
        <label className="mb-30">
            <input id="error" type="checkbox" className="alertCheckbox" autoComplete="off" />
            <div className={`alert ${props.type}`}>
                <span className="alertClose">X</span>
                <span className="alertText">[{props.errorCode}] {props.errorMsg}</span>
            </div>
        </label>
    )
}