import { HeaderHome } from "../components"
import { useState, useEffect } from "react";
import { address, headers_post } from "../lib/utils";
import Cookies from 'universal-cookie';

export default function Home() {
  const cookies = new Cookies();
  const [infos, setInfos] = useState()
  const [totp,setTotp] = useState(undefined)
  const enableTOTP = (e)=>{
    fetch(address+'/enable_totp', {
      method: 'POST',
      headers: headers_post()
    }).then((response=>response.json())).then((json)=>{
      setTotp(json.totp_url)
    })
  }
  const disableTOTP = (e)=>{
    fetch(address+'/disable_totp', {
      method: 'POST',
      headers: headers_post()
    }).then((response=>response.json())).then((json)=>{
      setTotp(null)
    })
  }

  useEffect(()=>{
    setInfos(undefined)
    const dataFetch = async () => {
      const data = await (
        await fetch(address + '/user')
        ).json();
        setInfos(data);
      };
      dataFetch()
  },[totp])


  if(infos == undefined)
    return <><HeaderHome/><div className="h-screen"></div></>
  else
    return (
      <>
        <HeaderHome username={infos.username} credit={infos.credit} />
        <p {...cookies.get('sport_mode')} className=" w-full border border-zinc-300"></p>
        <div className="h-screen text-xl text-zinc-300 bg-zinc-900 font-bold text-center h-full flex flex-col items-center justify-start pt-10">
          <p className="w-full"> PAUL IS WAITING</p>
          {(infos.totp_enabled == true)?
            <>
              <button className="mt-4 bg-zinc-600 hover:bg-zinc-700 px-4 py-2 uppercase rounded text-xs tracking-wider" onClick={disableTOTP}>Disable TOTP</button>
              <p className="text-md py-5">Get totp:</p>
              {(totp != null)?<p>{totp}</p>:<p>TOTP already enabled</p>}
            </>
            :
            <><button className="mt-4 bg-zinc-600 hover:bg-zinc-700 px-4 py-2 uppercase rounded text-xs tracking-wider" onClick={enableTOTP}>Enable TOTP</button></>
          }

        </div>
      </>
    )
}