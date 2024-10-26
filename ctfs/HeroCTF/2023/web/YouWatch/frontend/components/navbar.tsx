import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import api from "../helpers/utils/api";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faVideo, faPlus, faHouse, faRightFromBracket } from "@fortawesome/free-solid-svg-icons";

export default function Navbar() {
    const { push } = useRouter();

    var logout = async () => {
        await api("GET", "/api/logout")
        push("/login")
    }

    return (
    <div className="row mt-40 mb-100">
        <div className="three columns" style={{textAlign: "left"}}>
            <FontAwesomeIcon icon={faRightFromBracket} size="xl" className="logout-button ml-60" onClick={logout} />
        </div>
        <div className="six columns">
            <h1>
                <Image src="/img/ytb.png" className="mr-10" alt="" width={50} height={35} /> YouWatch
            </h1>
        </div>
        <div className="three columns" style={{textAlign: "right"}}>
            <Link href="/" style={{ color: "black" }}>
                <FontAwesomeIcon icon={faHouse} size="xl" className="mr-20" />
            </Link>
            <Link href="/profile" style={{ color: "black" }}>
                <FontAwesomeIcon icon={faUser} size="xl" className="mr-20" />
            </Link>
            <Link href="/studio" style={{ color: "black" }}>
                <FontAwesomeIcon icon={faVideo} size="xl" className="mr-20" />
            </Link>
            <Link href="/upload" style={{ color: "black" }}>
                <FontAwesomeIcon icon={faPlus} size="xl" className="mr-60" />
            </Link>
        </div>
    </div>
    );
}