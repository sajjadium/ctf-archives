import { useState } from 'react';
import Head from 'next/head';
import { createStyles, Header, Text, Center } from '@mantine/core';
import Posts from 'components/posts/Posts';
import PostsHeader from 'components/posts/PostsHeader';
import PostForm from 'components/posts/PostForm';
import ConnectModal from 'components/connector/ConnectModal';
import type { NextPage } from 'next';

const useStyles = createStyles((theme) => ({
    header: {
        backgroundColor: theme.colors.dark[9],
        borderBottom: 0,
    },
    heading: {
        fontWeight: 'bold',
        letterSpacing: '-2px',
        wordSpacing: '5px',
        fontSize: '2.5rem',
        paddingLeft: '20px',
    },
    mainContent: {
        width: '50vw',
        textAlign: 'left',
        paddingTop: '3rem',
    },
}));

const Home: NextPage = () => {
    const [modalOpen, setModalOpen] = useState(false);
    const { classes } = useStyles();
    return (
        <>
            <Head>
                <title>Totally Secure Dapp</title>
                <meta name="description" content="Trust me it's secure" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <Header className={classes.header} height={70}>
                <Center>
                    <Text className={classes.heading}>Totally Secure Dapp</Text>
                </Center>
            </Header>
            <ConnectModal />
            <PostForm modalOpen={modalOpen} setModalOpen={setModalOpen} />
            <Center>
                <main className={classes.mainContent}>
                    <PostsHeader setModalOpen={setModalOpen} />
                    <Posts />
                </main>
            </Center>
        </>
    );
};

export default Home;
