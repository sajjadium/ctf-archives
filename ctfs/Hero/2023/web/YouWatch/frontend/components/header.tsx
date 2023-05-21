import { useRouter } from 'next/router'
import Head from 'next/head';

export default function Header() {
    const path  = useRouter().pathname.slice(1,);
    const title = `${path || "index"} | YouWatch`

    return (
    <div>
        <Head>
            <title>{title}</title>
            <link rel="icon" href="/img/ytb.ico" />
        </Head>
    </div>
    );
}