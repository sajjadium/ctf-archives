import React, { useState } from 'react'
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Header from '../../../components/header'
import Navbar from '../../../components/navbar'
import Form from '../../../components/form'
import api from '../../../helpers/utils/api';
import authCheck from '../../../helpers/security/authCheck';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faVideo, faKey } from "@fortawesome/free-solid-svg-icons";

type ContainerProps = {
    name: string;
    videoId: string;
    isPrivate: boolean;
};

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, true);
    if (red)
        return;

    const videoId = ctx.params.id;
    const cookies = ctx.req.headers?.cookie;
    const videoInfo = (await api("GET", `/api/videos/getVideoInfos?id=${videoId}`, {}, cookies, true)).data

    return {
        props: {
            "name": videoInfo.name,
            "videoId": videoId,
            "isPrivate": videoInfo.isPrivate ? 1 : 0
        },
    };
}

export default function View(props: ContainerProps) {
    const [name, setName] = useState(props.name);
    const [isChecked, setIsChecked] = useState(props.isPrivate);
    const { push } = useRouter();

    var deleteVideo = (e) => {
        e.preventDefault();
        api("POST", "/api/videos/deleteVideo", { "id": props.videoId })
        push("/studio");
    }

    return (
    <div>
        <Header />
        <div className="container card mt-100 mb-100">
            <Navbar />
            <h2>Edit a video</h2>
            
            <div className="container mb-40">
                <Form method="PUT" action="/api/videos/updateVideo">
                    <div className="mb-20">
                        <input name="id" value={props.videoId} hidden />
                        <FontAwesomeIcon icon={faVideo} className="mr-10" /><input name="name" type="text" placeholder="name" value={name} onChange={(e) => setName(e.target.value)}/><br />
                        <input name="isPrivate" value="off" hidden />
                        <FontAwesomeIcon icon={faKey} className="mr-10" />Private?&nbsp;<input name="isPrivate" type="checkbox" defaultChecked={isChecked} onClick={() => setIsChecked(!isChecked)}/><br />
                    </div>
                    <input className="button-danger mr-20" type="submit" value="Edit"/>
                    <input className="button-danger" type="submit" onClick={deleteVideo} value="Delete"/>
                </Form>

                <p>
                    Want to see the video result? Click <Link href={`/video/view/${props.videoId}`}>here</Link>!
                </p>
            </div>
        </div>
    </div>
    );
}