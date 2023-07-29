import Document, { Html, Head, Main, NextScript } from "next/document";
import { NextStrictCSP } from "next-strict-csp";

const HeadCSP = process.env.NODE_ENV === "production" ? NextStrictCSP : Head;

class CustomDocument extends Document {
    render() {

        return (
            <Html>
                <HeadCSP>
                    {process.env.NODE_ENV === "production" && (
                        <meta httpEquiv="Content-Security-Policy" />
                    )}
                </HeadCSP>
                <body>
                    <Main />
                    <NextScript />
                </body>
            </Html>
        );
    }
}
export default CustomDocument;
