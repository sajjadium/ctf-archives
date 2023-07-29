import useIsMounted from "@/hooks/useIsMounted";
import axios from "axios";
import Image from "next/image";
import { useRouter } from "next/router";
import React from "react";
import { Tooltip } from "react-tooltip";

import logoutIcon from "../public/icons/logout.svg";


function LogoutButton() {
    const router = useRouter();
    const { isMounted } = useIsMounted();

    const onLogout = async () => {
        await axios.get("/api/auth/logout");
        router.push("/");
    };

    return (
        <div
            className="absolute top-[24px] right-12 cursor-pointer"
            data-tooltip-id="logout-tooltip"
            data-tooltip-content="Logout"
            onClick={onLogout}
        >
            <Image src={logoutIcon} height={28} />
            {isMounted && <Tooltip id="logout-tooltip" />}
        </div>
    );
}

export default LogoutButton;
