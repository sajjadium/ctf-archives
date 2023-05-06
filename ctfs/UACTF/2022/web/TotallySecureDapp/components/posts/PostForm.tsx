import { useState, useRef, useLayoutEffect } from 'react';
import { Modal, Stack, TextInput, Textarea, Group, Button } from '@mantine/core';
import { useUser } from 'components/context/UserContext';
import { usePosts } from 'components/context/PostsContext';
import type { Dispatch, SetStateAction } from 'react';
import type { ContractTransaction } from 'ethers';
import type { PostPublishedEvent, PostEditedEvent } from 'ethtypes/TotallySecureDapp';

interface PostFormProps {
    modalOpen: boolean;
    setModalOpen: Dispatch<SetStateAction<boolean>>;
    editingIndex?: number;
}

export default function PostForm(props: PostFormProps) {
    const { modalOpen, setModalOpen, editingIndex } = props;
    const { user } = useUser();
    const { posts, dispatchPosts } = usePosts();
    const [titleErr, setTitleErr] = useState(false);
    const [contentErr, setContentErr] = useState(false);
    const [loading, setLoading] = useState(false);
    const [title, setTitleRef] = useState<HTMLInputElement | null>(null);
    const [content, setContentRef] = useState<HTMLTextAreaElement | null>(null);
    const onSubmit = async () => {
        if (title === null || content === null || !user.contract || !user.provider) return;
        const err = { title: false, content: false };
        if (!title.value) err.title = true;
        if (!content.value) err.content = true;
        setTitleErr(err.title);
        setContentErr(err.content);
        if (err.title || err.content) return;
        setLoading(true);
        try {
            if (editingIndex !== undefined) {
                const tx: ContractTransaction = await user.contract.editPost(
                    editingIndex,
                    title.value,
                    content.value
                );
                const receipt = await tx.wait();
                const editEvents = receipt.events?.filter((e) => {
                    return e.event === 'PostEdited';
                });
                if (editEvents) {
                    const [event] = editEvents as Array<PostEditedEvent>;
                    const { index } = event.args;
                    const newPost = await user.contract._posts(index);
                    dispatchPosts({ editPost: { i: index.toNumber(), post: newPost } });
                }
            } else {
                const tx: ContractTransaction = await user.contract.addPost(
                    title.value,
                    content.value
                );
                const receipt = await tx.wait();
                const publishEvents = receipt.events?.filter((e) => {
                    return e.event === 'PostPublished';
                });
                if (publishEvents) {
                    const [event] = publishEvents as Array<PostPublishedEvent>;
                    const { index } = event.args;
                    const newPost = await user.contract._posts(index);
                    dispatchPosts({ addPost: newPost });
                }
            }
            setModalOpen(false);
        } catch {}
        setLoading(false);
    };
    // Populate existing content when editing
    useLayoutEffect(() => {
        if (editingIndex === undefined || title === null || content === null) return;
        title.value = posts[editingIndex].title;
        content.value = posts[editingIndex].content;
    }, [editingIndex, posts, title, content]);
    return (
        <Modal
            opened={modalOpen}
            onClose={() => {
                setModalOpen(false);
                setLoading(false);
                setTitleErr(false);
                setContentErr(false);
            }}
            title={editingIndex === undefined ? 'New Post' : 'Editing Post'}
            centered
        >
            <Stack>
                <TextInput
                    ref={setTitleRef}
                    label="Title"
                    placeholder="Post title"
                    error={titleErr}
                />
                <Textarea
                    ref={setContentRef}
                    label="Content"
                    placeholder="Post content"
                    error={contentErr}
                />
                <Group position="right">
                    <Button
                        onClick={loading ? () => undefined : () => onSubmit()}
                        loading={loading}
                    >
                        {editingIndex === undefined ? 'Submit post' : 'Submit edit'}
                    </Button>
                </Group>
            </Stack>
        </Modal>
    );
}
