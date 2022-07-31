import { useEffect, useState } from 'react';
import { Timeline, Modal } from '@mantine/core';
import { useUser } from 'components/context/UserContext';
import { usePosts } from 'components/context/PostsContext';
import Post from './Post';
import PostForm from './PostForm';

export default function Posts() {
    const { user } = useUser();
    const [editing, setEditing] = useState(0);
    const [postFormActive, setPostFormActive] = useState(false);
    const { posts, dispatchPosts } = usePosts();
    useEffect(() => {
        dispatchPosts({ clearPosts: true });
        const getPosts = async () => {
            if (!user.contract) return;
            const nPosts = await user.contract.nPosts();
            for (let i = nPosts.sub(1).toBigInt(); i >= 0; i--) {
                const post = await user.contract._posts(i);
                dispatchPosts({ unshiftPost: post });
            }
        };
        getPosts();
    }, [user, dispatchPosts]);
    return (
        <>
            <PostForm
                modalOpen={postFormActive}
                setModalOpen={setPostFormActive}
                editingIndex={editing}
            />
            <Timeline bulletSize={20} pt="lg">
                {posts
                    .slice(0)
                    .reverse()
                    .map((post, i) => (
                        <Timeline.Item key={`post-${i}`}>
                            <Post
                                index={posts.length - i - 1}
                                title={post.title}
                                content={post.content}
                                setEditing={setEditing}
                                setPostFormActive={setPostFormActive}
                            />
                        </Timeline.Item>
                    ))}
            </Timeline>
        </>
    );
}
