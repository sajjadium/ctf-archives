import { useReducer, createContext, useContext } from 'react';
import type { ReactNode } from 'react';

interface PostsContextProps {
    children: ReactNode;
}

type Post = {
    title: string;
    content: string;
};
type Posts = Array<Post>;
type Data = {
    addPost?: Post;
    unshiftPost?: Post;
    editPost?: { i: number; post: Post };
    removePost?: number;
    clearPosts?: boolean;
};
type PostsDispatch = (data: Data) => void;
type PostsContextT = { posts: Posts; dispatchPosts: PostsDispatch };

function postsReducer(posts: Posts, data: Data): Posts {
    const { addPost, unshiftPost, editPost, removePost, clearPosts } = data;
    if (addPost) {
        return [...posts, addPost];
    } else if (unshiftPost) {
        const newPosts = [...posts];
        newPosts.unshift(unshiftPost);
        return newPosts;
    } else if (editPost) {
        const newPosts = [...posts];
        const { i, post } = editPost;
        newPosts[i] = post;
        return newPosts;
    } else if (removePost !== undefined) {
        const newPosts = [...posts];
        newPosts.splice(removePost, 1);
        return newPosts;
    } else if (clearPosts) return [];
    return posts;
}

const PostsContext = createContext<PostsContextT | undefined>(undefined);

export function usePosts() {
    const context = useContext(PostsContext);
    if (context === undefined) throw new Error('usePosts must be used within a PostsProvider');
    return context;
}

export default function PostsProvider(props: PostsContextProps) {
    const { children } = props;
    const [posts, dispatchPosts] = useReducer(postsReducer, []);
    const value = { posts, dispatchPosts };
    return <PostsContext.Provider value={value}>{children}</PostsContext.Provider>;
}
