import Document, { Html, Head, Main, NextScript } from 'next/document';
import { ServerStyles, createStylesServer } from '@mantine/next';
import type { DocumentContext, DocumentInitialProps } from 'next/document';

const stylesServer = createStylesServer();

export default class _Document extends Document {
    static async getInitialProps(ctx: DocumentContext): Promise<DocumentInitialProps> {
        const initialProps = await Document.getInitialProps(ctx);
        return {
            ...initialProps,
            styles: [
                <>
                    {initialProps.styles}
                    <ServerStyles html={initialProps.html} server={stylesServer} />
                </>,
            ],
        };
    }

    render() {
        return (
            <Html>
                <Head />
                <body>
                    <Main />
                    <NextScript />
                </body>
            </Html>
        );
    }
}
