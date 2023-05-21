import React, { useState, useEffect } from 'react'
import Header from '../components/header'
import Navbar from '../components/navbar'
import Video from '../components/video'
import api from '../helpers/utils/api'
import authCheck from '../helpers/security/authCheck';

type ContainerProps = {
    pseudo: string;
    email: string;
};

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, true);
    if (red)
        return;

    const cookies = ctx.req.headers.cookie;
    const profile = await api("GET", "/api/profile", {}, cookies, true);

    return {
        props: {
            "pseudo": profile.pseudo,
            "email": profile.email
        },
    };
}

export default function Studio(props: ContainerProps) {
    const [videos, setVideos] = useState([]);
    const fetchVideo = async () => {
        return await api("GET", "/api/videos/myVideos");
    }

    var groupArray = (arr, groupSize) => {
        var result = [];
        for (var i = 0; i < arr.length; i += groupSize)
            result.push(arr.slice(i, i+groupSize));
        return result;
    }

    useEffect(() => {
        fetchVideo().then((d) => {
            setVideos(groupArray(d.data, 3));
        });
    }, []);

    return (
    <div>
        <Header />

        <div className="container card mt-100 mb-100">
            <Navbar />
            <h2 className="mb-40">Studio</h2>

            <div className="container mb-40">
                {videos.map((vRow) => {
                    return (
                        <div className="row">
                            {vRow.map((v) => {
                                return (
                                    <span className="four columns ml-20 mr-20 mb-20">
                                        <Video studio={true} id={v.id} name={v.name} chatId={v.chatId} private={v.isPrivate} pseudo={props.pseudo} />
                                    </span>
                                );
                            })}
                        </div>
                    );
                })}
            </div>
        </div>
    </div>
    );
}