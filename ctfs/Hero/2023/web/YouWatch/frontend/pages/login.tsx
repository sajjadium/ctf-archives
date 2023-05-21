import React from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Image from 'next/image';
import Header from '../components/header'
import Form from '../components/form'
import authCheck from '../helpers/security/authCheck';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faKey } from "@fortawesome/free-solid-svg-icons";

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, false);
    if (red)
        return;
    return { props: {} };
}

export default function Login() {
    const router = useRouter();

    var loggedCallback = (res) => {
        if (res.code === 200)
            router.push("/");
    }

    return (
    <div>
        <Header />
        <div className="login-container card mt-300">
            <h1 className="mt-40 mb-40">
                <Image src="/img/ytb.png" className="mr-10" alt="" width={50} height={35} /> YouWatch
            </h1>

            <Form method="POST" action="/api/login" callback={loggedCallback}>
                <div className="mb-20">
                    <FontAwesomeIcon icon={faUser} className="mr-10" /><input name="pseudo" id="pseudo" type="text" placeholder="pseudo" /><br />
                    <FontAwesomeIcon icon={faKey} className="mr-10" /><input name="password" id="password" type="password" placeholder="password" /><br />
                </div>
                <input className="button-danger" type="submit" id="submit" value="Login"/><br />
            </Form>

            <p className="mb-40">
                You are new on the plateform? Create an account <Link href="/register">here</Link>!
            </p>
        </div>
    </div>
    );
}