import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import Link from 'next/link'
import {SetStateAction, useState} from "react";


const a = async (setv: { (value: SetStateAction<string>): void; (arg0: string): any; }) => {
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: "same-origin",
    };
    // @ts-ignore
    fetch('/api/auth', requestOptions)
        .then(res => {
            if(res.status != 200)
                return new Promise((_, __) => {
                    throw new Error('cant resolve.');
                })
            return res.json()
        })
        .then(b => {
            // @ts-ignore
            setv(b.body)
        })
        .catch(e => setv(''));
}

const Home: NextPage = () => {
    let [v, setV] = useState<string>('');
    a(setV);
    return (
    <div>
      <Head>
        <title>Customer Support</title>
        <meta name="description" content="UMDCTF Custoemr Support" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="bg-black h-screen w-screen">
          <div className="relative h-screen flex justify-end bg-black flex-col">
              <Image
                  src="/cb.png"
                  layout="fill"
                  alt="GitHub"
                  objectFit="cover"
                  objectPosition="center"
                  className="h-screen"
              />
              <div
                  className="z-10
        bg-black/60 w-screen
        flex flex-col
        space-y-10
        py-10
        backdrop-blur-md
        @moz-document:bg-red-900/90
      "
              >
                  {v && <p className="text-red-600 text-center">{v}</p>}
                  <h1 className="text-white text-2xl text-center">
                      Contact us for services we can provide!
                  </h1>
                  <Link href="/contact" passHref>
                  <button
                      type="button"
                      className={`inline-flex items-center px-6 py-3 border border-transparent
       text-base font-medium rounded-md shadow-sm text-white bg-indigo-700
       hover:brightness-[90%] focus:outline-none focus:ring-2 focus:ring-offset-2
       focus:ring-indigo-500 w-fit justify-self-center mx-auto`}
                  >
                      Contact Us
                  </button>
                  </Link>
              </div>
          </div>

      </main>

    </div>
    )
}

export default Home
