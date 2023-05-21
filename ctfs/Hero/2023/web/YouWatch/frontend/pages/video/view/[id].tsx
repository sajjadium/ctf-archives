import React, { useEffect, useState } from "react";
import Header from '../../../components/header'
import Navbar from '../../../components/navbar'
import Form from '../../../components/form'
import Message from '../../../components/message'
import api from '../../../helpers/utils/api'
import authCheck from '../../../helpers/security/authCheck';

type ContainerProps = {
    pseudo: string;
    email: string;
    name: string;
    videoId: string;
    videoData: string;
    chatId: string;
    chat: Array<string>;
};

type Users = {
    pseudo: string;
}

type Chat = {
    content: string
    users: Users;
}

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, true);
    if (red)
        return;

    const videoId = ctx.params.id;
    const cookies = ctx.req.headers?.cookie;
    const profile = await api("GET", "/api/profile", {}, cookies, true);
    const videoInfo = (await api("GET", `/api/videos/getVideoInfos?id=${videoId}`, {}, cookies, true)).data
    const videoData = (await api("GET", `/api/videos/loadVideo?id=${videoId}`, {}, cookies, true))
    const chat = await api("GET", `/api/chats/getChat?chatId=${videoInfo.chatId}`, {}, cookies, true);

    return {
        props: {
            "pseudo": profile.pseudo,
            "email": profile.email,
            "name": videoInfo.name,
            "videoId": videoId,
            "videoData": videoData.data,
            "chatId": videoInfo.chatId,
            "chat": chat.data
        },
    };
}

export default function View(props: ContainerProps) {
    const [msg, setMsg] = useState("");
    const [chat, setChat] = useState(props.chat);

    var updateChat = async (res) => {
        var chat = (await api("GET", `/api/chats/getChat?chatId=${props.chatId}`)).data;
        setChat(chat);
        setMsg("");
    }

    return (
    <div>
        <Header />
        <div className="container card mt-100 mb-100">
            <Navbar />
            <h2>{props.name}</h2>
            <video className="mb-20" width="80%" height="650" controls>
                <source src={`data:video/mp4;base64,${props.videoData}`} type="video/mp4" />
            </video> 

            <div className="container mb-40" style={{ textAlign: "left" }}>
                <h3>Description</h3>
                <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam quae sapiente at omnis doloribus expedita laboriosam, voluptatem quis quam quasi itaque, sequi sit deleniti ex a ea accusantium id beatae.
                </p>
            </div>

            <div className="container mb-40" style={{ textAlign: "left" }}>
                <div className="row">
                    <h3>Comments</h3>
                </div>

                <div className="row">
                    <Form method="POST" action="/api/chats/sendMessage" callback={updateChat}>
                        <textarea name="content" cols={50} style={{ height: "150px" }} value={msg} onChange={(e) => { setMsg(e.target.value) }}></textarea> <br />
                        <input name="chatId" value={props.chatId} hidden /> <br />
                        <input className="button-danger" type="submit" value="Submit"/>
                    </Form>
                </div>

                <div className="row">
                    {chat.map((c) => {
                        return (
                            <Message content={(c as unknown as Chat).content} pseudo={(c as unknown as Chat).users.pseudo} />
                        );
                    })}
                </div>
            </div>
        </div>
    </div>
    );
}