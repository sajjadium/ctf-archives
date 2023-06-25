import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
      <meta httpEquiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self' https://fonts.gstatic.com/; script-src 'self'  https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/; frame-src 'self' https://www.google.com/recaptcha/ https://recaptcha.google.com/recaptcha/" />
      </Head>

      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
