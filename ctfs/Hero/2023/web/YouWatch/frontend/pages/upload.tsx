import React, { useState } from "react";
import Header from '../components/header'
import Navbar from '../components/navbar'
import Form from '../components/form'
import authCheck from '../helpers/security/authCheck';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faVideo, faKey } from "@fortawesome/free-solid-svg-icons";

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, true);
    if (red)
        return;
    return { props: {} };
}

export default function Upload() {
    const [isChecked, setIsChecked] = useState(false);

    var clickHandler = (e) => {
        document.getElementById("upload").click();
    }

    return (
    <div>
        <Header />
        <div className="container card mt-100 mb-100">
            <Navbar />
            <h2 className="mb-40">Upload a new video</h2>

            <div className="container mb-40">
                <Form method="POST" action="/api/videos/uploadVideo">
                    <div className="mb-20">
                        <FontAwesomeIcon icon={faVideo} className="mr-10" /><input name="name" type="text" placeholder="name" /><br />
                        <span className="upload" onClick={clickHandler}>
                            <p className="mt-80">Click here to select the video to upload.</p>
                        </span>
                        <input name="video" id="upload" type="file" hidden /><br />
                        <input name="isPrivate" value="off" hidden />
                        <FontAwesomeIcon icon={faKey} className="mr-10" />Private?&nbsp;<input name="isPrivate" type="checkbox" defaultChecked={isChecked} onClick={() => setIsChecked(!isChecked)}/><br />
                    </div>
                    <input className="button-danger" type="submit" value="Upload"/><br />
                </Form>
            </div>
        </div>
    </div>
    );
}