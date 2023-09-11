
import { InferGetServerSidePropsType } from 'next';


const Note = ({ data }: InferGetServerSidePropsType<typeof getServerSideProps>) => {


    return (<main className='w-screen h-screen bg-white flex flex-col items-center justify-start pt-10'>
        <h1 className='text-6xl text-emerald-700 font-bold'>PrivN0te</h1>
        <div className='border-2 border-gray-400 rounded-lg w-[700px] h-[400px]' dangerouslySetInnerHTML={{ __html: data?.note ?? "This note has been destroyed OR does not exist" }} >
        </div>
    </main>
    )
}

export default Note;

export async function getServerSideProps(context: any) {

    const secret: any = process.env.NEXT_PUBLIC_SECRET;
    const msg: any = process.env.NEXT_PUBLIC_MESSAGE;   

    function requestProfile(str1: string) {
        let sum = 0;
        for (let i = 0; i < str1.length; i++) {
            sum += str1.charCodeAt(i);
        }
        return sum + parseInt(secret);
    }

    const noteId = context.params!.note_id;
    let res = await fetch("http://express-noobgramer:8080/api/priv/" + noteId, {

        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `${requestProfile(msg)}`
        },
    })
    let data = await res.json();
    return { props: { data } }

}