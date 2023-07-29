import { isAuthenticated } from "@/utils/helpers";
import Link from "next/link";

export default function Home() {
    return (
        <div className="flex items-center justify-center grow">
            <div className="bg-[#F6F3F7] shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col">
                <h1 className="font-bold text-3xl mb-6 text-center">
                    Welcome to frogshare!
                </h1>
                <p className="px-10 mb-7">
                  Please register or login to get access to our ever growing collection of frogs and share your own.
                </p>

                <div className="flex flex-col items-center mb-6 text-center">
                    <Link
                        href="/login"
                        className="bg-[#14B82A] hover:bg-[#119822] text-white font-bold py-2 px-4 rounded w-[50%] mb-6"
                    >
                        Login
                    </Link>
                    <Link
                        href="/register"
                        className="bg-[#14B82A] hover:bg-[#119822] text-white font-bold py-2 px-4 rounded w-[50%]"
                    >
                        Register
                    </Link>
                </div>
            </div>
        </div>
    );
}

export async function getServerSideProps(context) {
  const authenticated = await isAuthenticated(context.req); 

  if (authenticated) {
      context.res.writeHead(302, { Location: "/frogs" });
      context.res.end();
  }

  return { props: { } };
}