import axios from "axios";
import { ErrorMessage } from "@hookform/error-message";
import { useRouter } from "next/router";
import { useForm } from "react-hook-form";
import { toast } from "react-toastify";

export default function Login() {
    const {
        register,
        handleSubmit,
        setError,
        formState: { errors },
    } = useForm();
    const router = useRouter();

    const onSubmit = async ({ username, password }) => {
        try {
            await axios.post("/api/auth/login", {
                username,
                password,
            });
            toast(`Welcome ${username}!`, { type: "success" });
            router.push("/frogs");
        } catch (error) {
            const message = error?.response?.data?.msg;

            if (message) {
                setError("username", {
                    type: "manual",
                    message,
                });
            }
        }
    };

    return (
        <div className="flex items-center justify-center grow">
            <div className="bg-[#F6F3F7] shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col">
                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="mb-4">
                        <label
                            className="block text-grey-darker text-sm font-bold mb-2"
                            htmlFor="username"
                        >
                            Username
                        </label>
                        <input
                            className="bg-inherit shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="username"
                            type="text"
                            placeholder="Username"
                            {...register("username", {
                                required: true,
                            })}
                        />
                        <ErrorMessage
                            errors={errors}
                            name="username"
                            render={({ message }) => (
                                <p className="text-red-500 mt-2">{message}</p>
                            )}
                        />
                    </div>
                    <div className="mb-6">
                        <label
                            className="block text-grey-darker text-sm font-bold mb-2"
                            htmlFor="password"
                        >
                            Password
                        </label>
                        <input
                            className="bg-inherit shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker mb-3"
                            id="password"
                            type="password"
                            placeholder="******************"
                            {...register("password", {
                                required: true,
                            })}
                        />
                    </div>
                    <div className="flex items-center justify-between">
                        <input
                            className="bg-[#14B82A] hover:bg-[#119822] text-white font-bold py-2 px-4 rounded"
                            value="Sign In"
                            type="submit"
                        />
                    </div>
                </form>
            </div>
        </div>
    );
}
