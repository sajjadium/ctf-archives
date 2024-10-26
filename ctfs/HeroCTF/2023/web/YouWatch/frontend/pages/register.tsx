import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import Header from '../components/header'
import Form from '../components/form'
import authCheck from '../helpers/security/authCheck';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faKey, faEnvelope } from "@fortawesome/free-solid-svg-icons";

export async function getServerSideProps(ctx) {
    const red = await authCheck(ctx, false);
    if (red)
        return;
    return { props: {} };
}

export default function Login() {
    return (
    <div>
        <Header />
        <div className="login-container card mt-300">
            <div className="row">
                <h1 className="mt-40 mb-40">
                    <Image src="/img/ytb.png" className="mr-10" alt="" width={50} height={35} /> YouWatch
                </h1>

                <Form method="POST" action="/api/register">
                    <div className="mb-20">
                        <FontAwesomeIcon icon={faUser} className="mr-10" /><input name="pseudo" type="text" placeholder="pseudo" /><br />
                        <FontAwesomeIcon icon={faEnvelope} className="mr-10" /><input name="email" type="email" placeholder="email" /><br />
                        <FontAwesomeIcon icon={faKey} className="mr-10" /><input name="password" type="password" placeholder="password" /><br />
                    </div>
                    <input className="button-danger" type="submit" value="Register" /><br />
                </Form>

                <p className="mb-40">
                    You already have an account? Login <Link href="/login">here</Link>!
                </p>
            </div>
        </div>
    </div>
    );
}