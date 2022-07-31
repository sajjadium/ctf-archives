import { useState } from 'react';
import { createStyles, Text, Stack, Box, ActionIcon, Popover, Button } from '@mantine/core';
import { Settings } from 'tabler-icons-react';
import { useUser } from 'components/context/UserContext';
import { usePosts } from 'components/context/PostsContext';
import type { Dispatch, SetStateAction } from 'react';
import type { ContractTransaction } from 'ethers';

interface PostProps {
    index: number;
    title: string;
    content: string;
    setEditing: Dispatch<SetStateAction<number>>;
    setPostFormActive: Dispatch<SetStateAction<boolean>>;
}

const useStyles = createStyles(() => ({
    title: {
        fontWeight: 'bold',
        fontSize: '1.8rem',
    },
    content: {
        fontSize: '1.3rem',
        marginTop: '-1rem',
    },
    settingsButton: {
        position: 'absolute',
        right: '0.5rem',
        top: '0.5rem',
    },
}));

export default function Post(props: PostProps) {
    const { index, title, content, setEditing, setPostFormActive } = props;
    const { classes } = useStyles();
    const { user } = useUser();
    const { dispatchPosts } = usePosts();
    const [active, setActive] = useState(false);
    return (
        <Box
            sx={(theme) => ({
                backgroundColor: theme.colors.dark[8],
                padding: '5px 15px',
                borderRadius: '10px',
            })}
        >
            <Stack spacing="xs">
                <Text className={classes.title}>{title}</Text>
                <Text className={classes.content}>{content}</Text>
                <div className={classes.settingsButton}>
                    <Popover
                        opened={active}
                        onClose={() => setActive(false)}
                        target={
                            <ActionIcon variant="light" onClick={() => setActive(!active)}>
                                <Settings size={16} />
                            </ActionIcon>
                        }
                        width={140}
                        position="bottom"
                        withArrow
                    >
                        <Stack>
                            <Button
                                onClick={() => {
                                    setActive(false);
                                    setPostFormActive(true);
                                    setEditing(index);
                                }}
                                variant="outline"
                            >
                                Edit
                            </Button>
                            <Button
                                onClick={async () => {
                                    setActive(false);
                                    if (!user.contract) return;
                                    const tx: ContractTransaction = await user.contract.removePost(
                                        index
                                    );
                                    await tx.wait();
                                    dispatchPosts({ removePost: index });
                                }}
                                color="red"
                                variant="outline"
                            >
                                Delete
                            </Button>
                        </Stack>
                    </Popover>
                </div>
            </Stack>
        </Box>
    );
}
