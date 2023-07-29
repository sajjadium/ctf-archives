import Head from "next/head";
import NavBar from "./NavBar";

export default function Layout({ children }) {
    return (
        <>
            <Head>
                <title>frogshare</title>
                <meta name="description" content="Yes We Frog" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <NavBar />
            <main className="bg-[#EDE7EF] min-h-[calc(100vh-76px)] px-10 py-8 flex justify-center">
                {children}
            </main>
        </>
    );
}
