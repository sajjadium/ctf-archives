import { address, headersPost } from "../lib/utils"
import Cookies from 'universal-cookie';

export default function ItemCard({id,name,price,buy}) {
  const cookies = new Cookies();
  const handleSubmit = (e)=>  {
    e.preventDefault()
    var formBody = 'item_id='+id
    fetch(address+'/buy', {
        method: 'POST',
        headers: headersPost(cookies.get('auth')),
      body: formBody
    }).then((response=>response.json())).then((json)=>{
      document.location = json.url;
    })
  }

    return (
      <>
        <div className="w-full bg-slate-800 border-slate-600 rounded-xl m-5 p-3 flex flex-col items-center justify-center">
            <h2 className="text-slate-200 font-bold text-lg ">{name}</h2>
            {(buy)?<>
              <p className="text-slate-200">{price}</p>
            <form onSubmit={handleSubmit} className="text-center flex items-center justify-center border-t mt-4 border-slate-400">
                <input className="mx-1 mt-3 bg-slate-600 hover:bg-slate-700 px-4 py-2 text-white uppercase rounded text-xs tracking-wider" type="submit" value="Buy with paypaul"></input>
            </form></>:<></>}
        </div>
      </>
    )}