import { Link } from "react-router-dom";
import { FaFire } from "react-icons/fa";
import Cookies from 'universal-cookie';
import { useNavigate } from "react-router-dom";
import sound from '../static/sportmode.mp3' 
export default function HeaderHome({username, credit}) {
  const cookies = new Cookies();
  const navigate = useNavigate();
  const logout = (e) => {
    navigate('/')
  }
  return (
    <div>
      <div className='z-50'>
        <div className="flex items-center justify-between bg-zinc-800 p-5">
            <div className="flex w-1/2 justify-start items-center flex-shrink-0 text-zinc-200 mr-6">
              <Link className="text-zinc-200 hover:underline p-1 text-xl font-bold" to='../home'>PAY PAUL</Link>
              <Link className="text-zinc-200 hover:underline p-1" to='../report '>Report</Link>
              <button className="text-zinc-200 hover:underline p-1" to='../logout' onClick={logout}>Logout</button>
            </div>
            <div className="flex w-1/2 justify-end items-center flex-shrink-0 text-zinc-200 pr-6 ">
              <p className="px-2">{username}</p>
              <p className="px-2">Current credit: {credit}</p>
              <audio id="audio" src={sound}></audio>
              <button className="flex items-center rounded-lg bg-zinc-600 p-2 hover:bg-zinc-500" onClick={async (e)=>{
                if(cookies.get('sport_mode').style.borderWidth == "0px" ){
                  cookies.set('sport_mode',JSON.stringify({style:{borderColor:"red",borderWidth:"1px"}}))
                }else{
                  cookies.set('sport_mode',JSON.stringify({style:{borderWidth:"0px"}}))
                }
                document.querySelector('audio').onended = ()=>{window.location.reload(false)}
                await document.querySelector('audio').play()
              }}>
              Sport Mode <FaFire></FaFire>
              </button>
            </div>
        </div>
      </div>
    </div>
  );
}