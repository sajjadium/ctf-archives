import React from "react";
import axios from "axios";
import Image from "next/image";
import { useRouter } from "next/router";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import Popup from "reactjs-popup";
import useIsMounted from "@/hooks/useIsMounted";
import FrogForm from "./FrogForm";

import addIcon from "../public/icons/add.svg";

function ShareButton() {
    const router = useRouter();
    const { isMounted } = useIsMounted();

    const onShare = async (data, setError) => {
        try {
            data.svgProps = {
                height: parseFloat(data.height),
                width: parseFloat(data.width),
                ...(data.viewbox && {
                    viewbox: data.viewbox,
                }),
            };
            delete data.height;
            delete data.width;
            delete data.viewbox;

            const res = await axios.post("/api/frogs", data);
            if (res.status == 200) {
                toast(
                    "Thanks for sharing, your frog will be visible after admin approval!",
                    { type: "info" }
                );
                router.push(`/frogs/${res.data.id}`);
                return true;
            }
        } catch (error) {
            const message = error?.response?.data?.msg;

            if (message) {
                setError("url", {
                    type: "manual",
                    message,
                });
            }
            return false;
        }
    };

    return (
        <>
            <div
                className="absolute right-4 bottom-4"
                data-tooltip-id="share-tooltip"
                data-tooltip-content="Share a frog"
            >
                <Popup
                    trigger={
                        <div className="bg-[#14B82A] rounded-full shadow-md text-center h-[64px] w-[64px] cursor-pointer">
                            <div className="flex justify-center items-center h-full w-full">
                                <Image src={addIcon} height={32} />
                            </div>
                        </div>
                    }
                    modal
                >
                    {(close) => (
                        <FrogForm
                            onSubmit={async (data, setError) => {
                                if (await onShare(data, setError)) {
                                    close();
                                }
                            }}
                        />
                    )}
                </Popup>
            </div>
            { isMounted && <Tooltip id="share-tooltip" /> }
        </>
    );
}

export default ShareButton;
