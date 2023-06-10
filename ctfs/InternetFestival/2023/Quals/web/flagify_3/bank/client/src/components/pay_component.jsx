import { useState } from "react";
import { address, headers_post } from "../lib/utils";
import Cookies from 'universal-cookie';

export default function PayComponent({sport_mode, token, user, amount}) {
  const [totp, setTotp] = useState('')
  const cookies = new Cookies()
  const handleSubmit = (e)=>  {
    e.preventDefault()
    var formBody = 'totp='+totp+'&token='+token;
    fetch(address+'/checkout', {
        method: 'POST',
        headers: headers_post(),
      body: formBody
    }).then((response=>response.json())).then((json)=>{
      if(json.error !== undefined){
        alert(json.error)
      }else{
        document.location = json.url;
    }
    })
  }
    return (
        <>
        <p {...sport_mode} className=" mb-20 w-full border border-zinc-300"></p>
        <div className="flex w-3/4 items-start justify-center">
            <div className="bg-zinc-800 rounded-xl py-10 px-5 w-1/2 flex-col items-center justify-center text-center">
                <p className="text-zinc-200 w-full text-lg">User {user} requires some spicciolis. Do you want to pay {amount}?</p>
                <form onSubmit={handleSubmit}className="flex flex-col items-center justify-start pt-5">
                    <p className="text-zinc-200 w-full text-lg">OTP:</p>
                    <input type="number" name="OTP" className="bg-zinc-600 text-zinc-200 px-1 rounded-lg" onChange={
                        (e) => setTotp(e.target.value)}/>
                    <div className="flex">
                        <button className="mt-4 bg-green-600 hover:bg-green-700 px-4 py-2 text-zinc-200 uppercase rounded text-xs tracking-wider mx-2" type="submit">Yes</button>
                        <button className="mt-4 bg-red-600 hover:bg-red-700 px-4 py-2 text-zinc-200 uppercase rounded text-xs tracking-wider mx-2" type="submit">No</button>
                    </div>
                </form>
            </div>
        </div>
        </>
    );
}
