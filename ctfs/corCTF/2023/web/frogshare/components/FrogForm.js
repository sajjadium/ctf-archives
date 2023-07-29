import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import "reactjs-popup/dist/index.css";

function FrogForm({ initialFrog, onSubmit }) {
    const {
        register,
        handleSubmit,
        formState: { errors },
        setError,
        setValue
    } = useForm();
    const [customViewbox, setCustomViewbox] = useState(!!initialFrog?.viewbox);

    useEffect(() => {
        if (initialFrog) {
            const { name, img: url, height, width, viewbox } = initialFrog;
            setValue("name", name);
            setValue("url", url);
            setValue("height", height);
            setValue("width", width);
            viewbox && setValue("viewbox", viewbox);
        }
    },[]);

    const onHandleSubmit = (data) => onSubmit(data, setError);

    return (
        <form onSubmit={handleSubmit(onHandleSubmit)} className="p-4">
            <div className="mb-6">
                <label
                    htmlFor="name"
                    className="block mb-2 text-sm font-medium text-gray-900 "
                >
                    Name
                </label>
                <input
                    id="name"
                    {...register("name", {
                        required: "A name is required",
                    })}
                    className="bg-white-50 border border-gray-300 text-sm rounded-lg focus:ring-green-500 focus:border-ring-500 block w-full p-2.5"
                    placeholder="some frog"
                />
                {errors.name && (
                    <p className="text-red-500 text-xs pt-2">
                        {errors.name.message}
                    </p>
                )}
            </div>
            <div className="mb-6">
                <label
                    htmlFor="url"
                    className="block mb-2 text-sm font-medium text-gray-900 "
                >
                    SVG url
                </label>
                <input
                    id="url"
                    {...register("url", {
                        required: "URL is required",
                        pattern: {
                            value: /^https:\/\/.*\.svg$/,
                            message: "Invalid SVG URL",
                        },
                    })}
                    className="bg-white-50 border border-gray-300 text-sm rounded-lg focus:ring-green-500 focus:border-ring-500 block w-full p-2.5"
                    placeholder={
                        "https://ctf.cor.team/2023-ctf/frogs/mellow-frog.svg"
                    }
                />
                {errors.url && (
                    <p className="text-red-500 text-xs pt-2">
                        {errors.url.message}
                    </p>
                )}
            </div>
            <div className="mb-6">
                <label
                    htmlFor="height"
                    className="block mb-2 text-sm font-medium text-gray-900 "
                >
                    Height
                </label>
                <input
                    id="height"
                    {...register("height", {
                        required: "Height is required",
                        pattern: {
                            value: /^\d+$/,
                            message: "Height must be a number",
                        },
                    })}
                    className="bg-white-50 border border-gray-300 text-sm rounded-lg focus:ring-green-500 focus:border-ring-500 block w-full p-2.5"
                    placeholder={64}
                />
                {errors.height && (
                    <p className="text-red-500 text-xs pt-2">
                        {errors.height.message}
                    </p>
                )}
            </div>
            <div className="mb-6">
                <label
                    htmlFor="width"
                    className="block mb-2 text-sm font-medium text-gray-900"
                >
                    Width
                </label>
                <input
                    id="width"
                    {...register("width", {
                        required: "Width is required",
                        pattern: {
                            value: /^\d+$/,
                            message: "Width must be a number",
                        },
                    })}
                    className="bg-white-50 border border-gray-300 text-sm rounded-lg focus:ring-green-500 focus:border-ring-500 block w-full p-2.5"
                    placeholder={64}
                />
                {errors.width && (
                    <p className="text-red-500 text-xs pt-2">
                        {errors.width.message}
                    </p>
                )}
            </div>
            <div className={customViewbox ? "mb-2" : "mb-6"}>
                <div
                    className="flex items-center w-fit"
                    onClick={() => setCustomViewbox((c) => !c)}
                >
                    <input
                        className="mr-2 cursor-pointer"
                        type="checkbox"
                        checked={customViewbox}
                        onChange={() => {}}
                    />
                    <label
                        htmlFor="use-viewbox"
                        className="block text-sm font-medium text-gray-900 cursor-pointer"
                    >
                        Use custom viewbox
                    </label>
                </div>
            </div>
            {customViewbox && (
                <div className="mb-6">
                    <label
                        htmlFor="viewbox"
                        className="block mb-2 text-sm font-medium text-gray-900"
                    >
                        Viewbox
                    </label>
                    <input
                        id="viewbox"
                        {...register("viewbox", {
                            required: "Viewbox is required",
                            pattern: {
                                value: /^\d+\s\d+\s\d+\s\d+$/,
                                message:
                                    "Viewbox format must be: number number number number",
                            },
                        })}
                        className="bg-white-50 border border-gray-300 text-sm rounded-lg focus:ring-green-500 focus:border-ring-500 block w-full p-2.5"
                        placeholder={"0 0 64 64"}
                    />
                    {errors.viewbox && (
                        <p className="text-red-500 text-xs pt-2">
                            {errors.viewbox.message}
                        </p>
                    )}
                </div>
            )}
            <input
                type="submit"
                className="text-white bg-[#14B82A] hover:bg-[#119822] focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
            />
        </form>
    );
}

export default FrogForm;
