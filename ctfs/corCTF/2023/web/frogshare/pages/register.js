import axios from "axios";
import { useForm } from "react-hook-form";
import { ErrorMessage } from "@hookform/error-message";
import { useRouter } from "next/router";
import { toast } from "react-toastify";

export default function Register() {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors },
        setError,
    } = useForm();

    const router = useRouter();

    const onSubmit = async ({ username, password }) => {
        try {
            const res = await axios.post("/api/auth/register", {
                username,
                password,
            });
            if (res.status === 200) {
                toast("Registration successful!", { type: "success" });
                router.push("/login");
            }
        } catch (error) {
            setError("username", {
                type: "manual",
                message: error?.response?.data?.msg,
            });
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
                                maxLength: {
                                    value: 20,
                                    message: "Max 20 characters",
                                },
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
                    <div className="mb-4">
                        <label
                            className="block text-grey-darker text-sm font-bold mb-2"
                            htmlFor="password"
                        >
                            Password
                        </label>
                        <input
                            className="bg-inherit shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="password"
                            type="password"
                            placeholder="******************"
                            {...register("password", {
                                required: true,
                                minLength: {
                                    value: 8,
                                    message: "Min 8 characters",
                                },
                            })}
                        />
                        <ErrorMessage
                            errors={errors}
                            name="password"
                            render={({ message }) => (
                                <p className="text-red-500 mt-2">{message}</p>
                            )}
                        />
                    </div>
                    <div className="mb-6">
                        <label
                            className="block text-grey-darker text-sm font-bold mb-2"
                            htmlFor="password-confirm"
                        >
                            Password confirmation
                        </label>
                        <input
                            className="bg-inherit shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="password-confirm"
                            type="password"
                            placeholder="******************"
                            {...register("password-confirm", {
                                required: true,
                                minLength: {
                                    value: 8,
                                    message: "Min 8 characters",
                                },
                                validate: (val) => {
                                    if (watch("password") !== val) {
                                        return "Your passwords do no match";
                                    }
                                },
                            })}
                        />
                        <ErrorMessage
                            errors={errors}
                            name="password-confirm"
                            render={({ message }) => (
                                <p className="text-red-500 mt-2">{message}</p>
                            )}
                        />
                    </div>
                    <div className="flex items-center justify-between">
                        <input
                            className="bg-[#14B82A] hover:bg-[#119822] text-white font-bold py-2 px-4 rounded"
                            value="Sign Up"
                            type="submit"
                        />
                    </div>
                </form>
            </div>
        </div>
    );
}
