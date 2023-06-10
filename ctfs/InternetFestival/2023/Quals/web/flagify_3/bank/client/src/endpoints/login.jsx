import { Header } from "../components";
import { address } from "../lib/utils";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Link } from "react-router-dom";
import React from "react";
import Cookies from 'universal-cookie';

export default function LoginForm() {
  const cookies = new Cookies();
  const [user, setUser] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate();

  const handleSubmit = (e)=>  {
    e.preventDefault()
    var formBody = 'username='+user+'&password='+password;
    fetch(address+'/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    }).then((response=>response.json())).then((json)=>{
      if(json.error !== undefined){
        alert(json.error)
      }else{
        cookies.set('sport_mode',JSON.stringify({style:{borderWidth:"0px"}}))
        navigate('/home')
      }
    })
  }
  return (
    <>
      <Header/>
      <section className="h-screen flex flex-col justify-start space-y-10 items-center my-2 mx-5 ">
        <div className="w-full">
        </div>
        <div className="w-full flex flex-col items-center">
          <h1 className="text-lg text-zinc-200 font-bold p-5">LOGIN</h1>
          <form onSubmit={handleSubmit} className="w-full flex flex-col items-center">
            <input id="username" name="username" className="text-sm w-1/2 px-4 py-2 text-zinc-200 bg-zinc-800 rounded" type="text" placeholder="Username" value={user} 
            onChange={(e)=> {
              setUser(e.target.value)
            }} />
            <input id="password" name="password" className="text-sm w-1/2 px-4 py-2 text-zinc-200 bg-zinc-800 rounded mt-4" type="password" placeholder="Password" value={password} 
            onChange={(e)=> {
              setPassword(e.target.value)
            }} />
            <input id="submit" type="submit" className="mt-4 bg-zinc-600 hover:bg-zinc-700 px-4 py-2 text-white uppercase rounded text-xs tracking-wider" value="Login"></input>
          </form>
          <div className="mt-4 font-semibold text-sm text-center text-zinc-200">
            Don't have an account? <Link className="text-rose-600 hover:underline hover:underline-offset-4" to="../register">Register</Link>
          </div>
        </div>
      </section>
    </>
);
}