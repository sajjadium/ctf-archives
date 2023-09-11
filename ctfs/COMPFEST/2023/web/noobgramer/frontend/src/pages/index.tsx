import Head from 'next/head'
import { useState } from 'react'

const secret: any = process.env.NEXT_PUBLIC_SECRET;
const msg: any = process.env.NEXT_PUBLIC_MESSAGE;


function requestProfile(str1: string) {
  let sum = 0;
  for (let i = 0; i < str1.length; i++) {
    sum += str1.charCodeAt(i);
  }
  return sum + parseInt(secret);
}



export default function Home() {

  const [result, setResult] = useState("")

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    let note: string = e.target[0]!.value;
    
    let res = await fetch("/api/priv", {
      
      method : "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": `${requestProfile(msg)}`
      },
      body: JSON.stringify({ note: note })
    })

    let data = await res.json();
    if (res.status == 200) {
      console.log(data)
      setResult(`your note has been made at ${window.location.origin}/note/${data.id}`)
    } else {
      alert(data.message);
    }
  }

  return (
    <>
      <Head>
        <title>PRivN0tes</title>
        <meta name="description" content="create destructible anda secure note" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className='w-screen h-screen bg-white flex flex-col items-center justify-start pt-10'>
        <h1 className='text-6xl text-emerald-700 font-bold'>PrivN0te</h1>
        <p className='text-xl font-semibold text-gray-700 tracking-wider mt-5'>create note that will be deleted after the first read!</p>
        <p className='p-4 rounded-md bg-emerald-100 text-center'>{result}</p>
        <form method='POST' onSubmit={handleSubmit} className='mt-4 flex flex-col items-end gap-y-2'>
          <textarea name='note' className='border-2 border-gray-400 rounded-lg w-[700px] h-[400px]' style={{ resize: "none" }}>
          </textarea>
          <button type='submit' className='py-2 px-3 rounded-md bg-blue-500 text-white font-semibold hover:bg-blue-700'>create</button>
        </form>
      </main>
    </>
  )
}
