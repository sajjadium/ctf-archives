import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import 'react-tooltip/dist/react-tooltip.css'
import Layout from "@/components/Layout";
import "@/styles/globals.css";

export default function App({ Component, pageProps }) {
    return (
        <Layout>
            <Component {...pageProps} />
            <ToastContainer
                position="bottom-left"
                autoClose={3000}
                newestOnTop={true}
                closeOnClick
                pauseOnHover
                theme="light"
            />
        </Layout>
    );
}
