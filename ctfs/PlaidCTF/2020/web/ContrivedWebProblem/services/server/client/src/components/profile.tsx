import * as React from "react";

import { UserContext } from "../contexts/user";
import { rest } from "../actions/rest";
import { base64ArrayBuffer } from "../utils/array";
import { useHistory } from "../utils/utils";

import "./profile.scss";

export default () => {
    let { data: user, refresh } = React.useContext(UserContext);
    let [ profile, setProfile ] = React.useState("");
    let [ counter, setCounter ] = React.useState(0);
    let history = useHistory();

    const uploadFile = async (files: FileList) => {
        let firstFile = files[0] as any;
        let image: ArrayBuffer = await firstFile.arrayBuffer();
        let encodedImage = base64ArrayBuffer(image);
        await rest("/profile", [], {
            image: encodedImage,
        });
        await refresh();
        setCounter(counter + 1);
    }

    const uploadPath = async () => {
        await rest("/profile", [], {
            url: profile,
        });
        await refresh();
        setCounter(counter + 1);
    }

    if (user === null) return <></>;

    if (user.kind === "none") {
        history.push("/login");
        return <></>;
    }

    return (
        <div className="profile">
            <h1>{user.name}'s Profile</h1>
            <div className="pure-form profile-form">
                <div className="profile-pic">
                {
                    user?.profile ? <img src={`/api/image?url=${user.profile}#${counter}`}/> : undefined
                }
                </div>
                <input type="file" id="profile-upload" className="pure-button" onChange={(e) => e.target.files ? uploadFile(e.target.files) : undefined}/>
                <label htmlFor="profile-upload" className="file-label btn teal btn-large pure-button">Upload file</label>
                <input type="text" onChange={(e) => setProfile(e.target.value)} value={profile}/>
                <input type="button" className="set-button pure-button larg-btn teal btn" onClick={uploadPath} value={"Set Profile Picture"}/>
            </div>
        </div>
    )
}