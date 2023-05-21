import React, { useState, useEffect } from 'react'
import Header from '../components/header'
import Navbar from '../components/navbar'
import Video from '../components/video'
import api from '../helpers/utils/api'
import authCheck from '../helpers/security/authCheck';

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, true);
    if (red)
        return;
    return { props: {} };
}

export default function Index() {
    const [videos, setVideos] = useState([]);
    const fetchVideo = async (filter="") => {
        return await api("GET", `/api/videos/getVideos?name=${filter}`);
    }

    const updateVideos = (search="") => {
        fetchVideo(search).then((d) => {
            if (d.data === "No videos found") {
                setVideos([]);
            } else {
                setVideos(groupArray(d.data, 3));
            }
        });
    }

    var groupArray = (arr, groupSize) => {
        var result = [];
        for (var i = 0; i < arr.length; i += groupSize)
            result.push(arr.slice(i, i+groupSize));
        return result;
    }

    useEffect(updateVideos, []);
    return (
        <div>
            <Header />
            <div className="container card mt-100 mb-100">
                <Navbar />
                <h2 className="mb-40">Search a video</h2>

                <input type="text" className="mb-40" onKeyUp={(e) => {
                    var search = (e.target as HTMLInputElement).value
                    updateVideos(search);
                }} style={{ width:"70%" }}/>

                <div className="container mb-40">
                    {videos.map((vRow) => {
                        return (
                            <div className="row">
                                {vRow.map((v) => {
                                    return (
                                        <span className="four columns ml-20 mr-20 mb-20">
                                            <Video studio={false} id={v.id} name={v.name} chatId={v.chatId} private={v.isPrivate} pseudo={v.users?.pseudo}/>
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