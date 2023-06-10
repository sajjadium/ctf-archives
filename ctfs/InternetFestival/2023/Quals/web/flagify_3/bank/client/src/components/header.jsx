import { Link } from "react-router-dom";
  
export default function Header() {
  return (
    <div>
      <div className='z-50'>
        <div className="flex items-center justify-between flex-wrap bg-zinc-800 p-5">
            <div className="flex items-center justify-between flex-shrink-0 text-zinc-200 mr-6">
              <Link className="text-zinc-200 hover:underline p-1 text-xl font-bold" to='/'>PAY PAUL</Link>
              <Link className="text-zinc-200 hover:underline p-1" to='/login'>Login</Link>
              <Link className="text-zinc-200 hover:underline p-1" to='/register'>Register</Link>
            </div>
        </div>
      </div>
    </div>
  );
}