import React, { useMemo } from "react";
import { useRouter } from "next/router";
import Image from 'next/image';
import Popup from "reactjs-popup";
import FrogForm from "./FrogForm";
import axios from "axios";
import { toast } from "react-toastify";

import editIcon from "../public/icons/edit.svg";

function EditButton({ frog }) {
    const router = useRouter();
    
    const initialFrog = useMemo(() => {
        if (!frog) return null;
        let tempFrog = { ...frog, ...JSON.parse(frog.svgProps) };
        delete tempFrog.svgProps;
        return tempFrog;
    }, [JSON.stringify(frog)]);

    const onEdit = async (data, setError) => {
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
            const res = await axios.patch(`/api/frogs?id=${frog.id}`, data);

            if (res.status === 200) {
                toast("Frog updated!", { type: "info" });
                router.reload();
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
        <div className="absolute right-4 bottom-4">
            <Popup
                trigger={
                    <div className="bg-[#FF7E19] rounded-full shadow-md h-[64px] w-[64px] cursor-pointer">
                        <div className="flex justify-center items-center h-full">
                            <Image src={editIcon} height={32} />
                        </div>
                    </div>
                }
                modal
            >
                {(close) => (
                    <FrogForm
                        initialFrog={initialFrog}
                        onSubmit={async (data, setError) => {
                            if (await onEdit(data, setError)) {
                                close();
                            }
                        }}
                    />
                )}
            </Popup>
        </div>
    );
}

export default EditButton;
