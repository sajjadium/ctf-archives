import Frog from "@/components/Frog";
import LogoutButton from "@/components/LogoutButton";
import EditButton from "@/components/EditButton";
import {
    getFrogById,
    getSessionCookie,
    getUserBySession,
} from "@/utils/helpers";
import BackButton from "@/components/BackButton";

export default function Frogs({ isAuthor, frog }) {
    return (
        <>
            <div className="flex items-evenly flex-wrap m-auto h-fit">
                {frog ? (
                    <Frog frog={frog} key={frog.id} />
                ) : null}
            </div>
            {isAuthor && <EditButton frog={frog} />}
            <BackButton />
            <LogoutButton />
        </>
    );
}

export async function getServerSideProps(context) {
    let user = null;

    const session = getSessionCookie(context.req);

    if (session) {
        user = await getUserBySession(session);
    }

    if (!user) {
        return {
            redirect: {
                destination: "/",
                permanent: false,
            },
        };
    }

    const frogId = context.params.id;
    const frog = await getFrogById(frogId, user.username, user.is_admin);

    if (!frog) {
        return {
            redirect: {
                destination: "/frogs",
                permanent: false,
            },
        };
    }

    return {
        props: {
            frog,
            isAuthor: user.username === frog.creator,
        },
    };
}
