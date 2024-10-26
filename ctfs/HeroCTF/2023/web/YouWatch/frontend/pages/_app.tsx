import { Lato } from 'next/font/google';
import { AppProps } from 'next/app'

import "@fortawesome/fontawesome-svg-core/styles.css";
import '../style/normalize.css';
import '../style/skeleton.css';
import '../style/main.css';

const kanit = Lato({
    weight: '400',
    subsets: ['latin'],
});

export default function MyApp({ Component, pageProps }: AppProps) {
    return (
    <div>
        <style jsx global>{`
        body {
            background-color: #F7F7F7;
        }
        * {
            font-family: ${kanit.style.fontFamily};
            font-size: 20px;
        }
        `}</style>
        <Component {...pageProps} />
    </div>
    )
}