import { Header } from "../components";
import { address } from "../lib/utils";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
 
  export default function RegisterForm(){
    const [user, setUser] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate();

    const handleSubmit = (e)=>  {
      e.preventDefault()
      var formBody = 'username='+user+'&password='+password;
      console.log(formBody)
      fetch(address+'/register', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: formBody
      }).then((response=>response.status)).then((stat)=>{
          if(stat == 201){
            navigate('/login')
        }else{
            alert('User already registered')
          }
        })
      }

    return (
      <>
        <Header></Header>
        <section className="h-screen flex flex-col justify-start space-y-10 items-center my-2 mx-5 ">
          <div className="w-full">
          </div>
          <div className="w-full flex flex-col items-center">
            <h1 className="text-lg text-slate-200 font-bold p-5">REGISTER</h1>
            <form onSubmit={handleSubmit} className="w-full flex flex-col items-center">
              <input id="username" name="username" className="text-sm w-1/2 px-4 py-2 text-slate-200 bg-slate-800 rounded" type="text" placeholder="Username" value={user} 
              onChange={(e)=> {
                setUser(e.target.value)
              }} />
              <input id="password" name="password" className="text-sm w-1/2 px-4 py-2 text-slate-200 bg-slate-800 rounded mt-4" type="password" placeholder="Password" value={password} 
              onChange={(e)=> {
                setPassword(e.target.value)
              }} />
              <input type="submit" className="mt-4 bg-slate-600 hover:bg-slate-700 px-4 py-2 text-white uppercase rounded text-xs tracking-wider" value="Register"></input>
            </form>
          </div>
        </section>
      </>
    );
}
