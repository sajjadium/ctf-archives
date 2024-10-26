import React from 'react';
import Image from 'next/image';
import Header from '../components/header'
import Navbar from '../components/navbar'
import authCheck from '../helpers/security/authCheck';
import api from "../helpers/utils/api";

type ContainerProps = {
    pseudo: string;
    email: string;
};

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, true);
    if (red)
        return;
    
    const { cookie } = ctx.req.headers;
    const profile = await api("GET", "/api/profile", {}, cookie, true);
    
    return {
        props: {
            "pseudo": profile.pseudo,
            "email": profile.email
        }
    };
}

export default function Login(props: ContainerProps) {
    const profileImg = Math.floor(Math.random() * 2) ? "/img/mizu.jpeg" : "/img/wortax.jpg"

    return (
    <div>
        <Header />
        <div className="container card mt-100 mb-100">
            <Navbar />
            <h2 className="mb-40">Profile</h2>

            <div className="container mb-40">
                <Image src={profileImg} alt="" width={200} height={200} className="mb-30" /><br />
                <span style={{ fontWeight: "bold" }}>
                    {props.pseudo} <br />
                    {props.email}
                </span>
            </div>
        </div>
    </div>
    );
}