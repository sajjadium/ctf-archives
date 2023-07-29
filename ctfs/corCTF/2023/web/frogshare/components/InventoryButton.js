import useIsMounted from "@/hooks/useIsMounted";
import Image from "next/image";
import { useRouter } from "next/router";
import React from "react";
import { Tooltip } from "react-tooltip";

import inventoryIcon from "../public/icons/idek.svg";

function InventoryButton({ frogId }) {
    const router = useRouter();
    const { isMounted } = useIsMounted();

    const onNavigateToFrog = async () => {
        router.push(`/frogs/${frogId}`);
    };

    return (
        <div
            className="absolute top-[24px] right-24 cursor-pointer"
            data-tooltip-id="inventory-tooltip"
            data-tooltip-content="My frog"
            onClick={onNavigateToFrog}
        >
            <Image src={inventoryIcon} height={28}/>
            {isMounted && <Tooltip id="inventory-tooltip" />}
        </div>
    );
}

export default InventoryButton;
