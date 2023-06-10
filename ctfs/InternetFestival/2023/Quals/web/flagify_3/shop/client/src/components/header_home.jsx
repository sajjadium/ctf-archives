import { Link } from "react-router-dom";
import Cookies from 'universal-cookie';
import { useNavigate } from "react-router-dom";

export default function HeaderHome() {
  const cookies = new Cookies();
  const navigate = useNavigate();
  const logout = (e) => {
    cookies.remove('auth', { path: '/' });
    navigate('/')
  }
  return (
    <div>
      <div className='z-50'>
        <div className="flex items-center justify-between flex-wrap bg-slate-800 p-5">
            <div className="flex items-center justify-between flex-shrink-0 text-slate-200 mr-6">
              <Link className="text-slate-200 hover:underline p-1 text-xl font-bold" to='../home'>FR4NC0'S SHOP</Link>
              <Link className="text-slate-200 hover:underline p-1" to='../shop'>Shop</Link>
              <Link className="text-slate-200 hover:underline p-1" to='../items'>Your Items</Link>
              <button className="text-slate-200 hover:underline p-1" to='../logout' onClick={logout}>Logout</button>
            </div>
        </div>
        <svg className='w-full bg-slate-900 h-full' viewBox='0 0 1442 100' preserveAspectRatio="xMidYMid">
          <path className='w-full fill-slate-800' d="M 0 90 C 480 0 600 0 720 10.7 C 840 21 960 43 1080 48 C 1200 53 1320 43 1380 37.3 L 1440 32 L 1440 0 L 1380 0 C 1320 0 1200 0 1080 0 C 960 0 840 0 720 0 C 600 0 480 0 360 0 C 240 0 120 0 60 0 L 0 0 Z"></path>
        </svg>
      </div>
    </div>
  );
}