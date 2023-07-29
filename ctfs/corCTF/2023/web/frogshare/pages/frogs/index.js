import Frog from "@/components/Frog";
import ShareButton from "@/components/ShareButton";
import LogoutButton from "@/components/LogoutButton";
import InventoryButton from "@/components/InventoryButton";
import { getFrogs, getSessionCookie, getUserBySession } from "@/utils/helpers";

export default function Frogs({ isAuthenticated, frogs, sharedFrog }) {

    return (
        <>
            <div className="flex items-evenly flex-wrap m-auto h-fit">
                {frogs?.map((frog) => (
                    <Frog frog={frog} key={frog.id} />
                ))}
            </div>
            {sharedFrog ? (
                <InventoryButton frogId={sharedFrog} />
            ) : (
                <ShareButton />
            )}
            {isAuthenticated && <LogoutButton />}
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

    const frogs = await getFrogs();

    return {
        props: {
            frogs,
            isAuthenticated: !!user,
            sharedFrog: user.shared_frog,
        },
    };
}
