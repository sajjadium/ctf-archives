import React from "react";
import Image from "next/image";
import { useRouter } from "next/router";
import { Tooltip } from "react-tooltip";
import useIsMounted from "@/hooks/useIsMounted";

import backIcon from "../public/icons/back.svg";

function BackButton() {
    const router = useRouter();
    const { isMounted } = useIsMounted();

    const onBack = async () => {
        router.push("/frogs");
    };

    return (
        <div
            className="absolute top-[24px] right-24 cursor-pointer"
            data-tooltip-id="back-tooltip"
            data-tooltip-content="Back to frogs"
            onClick={onBack}
        >
            <Image src={backIcon} height={28}/>
            {isMounted && <Tooltip id="back-tooltip" />}
        </div>
    );
}

export default BackButton;
