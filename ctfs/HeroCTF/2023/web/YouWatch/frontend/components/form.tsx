import React from 'react';
import Error from '../components/error'
import api from '../helpers/utils/api'

type ContainerProps = {
    children: React.ReactNode;
    method: string;
    action: string;
    callback?: Function;
};

export default function Form(props: ContainerProps) {
    const [errorMsg, setErrorMsg] = React.useState(null);

    var b64blob = (blob) => {
        return new Promise((resolve, _) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve((reader.result as string).replace("data:video/mp4;base64,", ""));
          reader.readAsDataURL(blob);
        });
    }

    var submitForm = async (e) => {
        e.preventDefault();
        const data = new FormData(e.target);
        var formData = (Object.fromEntries(data.entries()) as Object);

        const fileUpload = (document.getElementById("upload") as HTMLInputElement);
        if (fileUpload && fileUpload.files[0]) {
            formData[fileUpload.name] = await b64blob(fileUpload.files[0]);
        } else if (formData["video"]) {
            delete formData["video"];
        }
    
        if (formData["isPrivate"])
            formData["isPrivate"] = formData["isPrivate"] === "on" ? 1 : 0;

        var res = await api(props.method, props.action, formData);

        if (res.error) {
            setErrorMsg(<Error errorCode={res.code} errorMsg={res.error} type="error" />);
        }

        if (res.ok) {
            setErrorMsg(<Error errorCode={res.code} errorMsg={res.ok} type="success" />);
        }
        
        if (props.callback) {
            props.callback(res);
        }
    }

    return (
    <div>
        <form onSubmit={submitForm}>
            {props.children}
        </form>
        
        {errorMsg}
    </div>
    )
}