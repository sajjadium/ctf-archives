import { HeaderHome,ItemCard } from "../components"
import { address,headers } from "../lib/utils"
import { useState } from "react"
import { useEffect } from "react"
import Cookies from 'universal-cookie';
import { useNavigate } from "react-router-dom";

export default function Items() {
  const cookies = new Cookies();
  const navigate = useNavigate()
  const [items, setItems] = useState()
  useEffect(()=>{
    if(cookies.get('auth') == undefined){
      navigate('/')
    }
    const dataFetch = async () => {
      const data = await (
        await fetch(address + '/user/item',{
          headers:headers(cookies.get('auth'))
        })
        ).json();
        setItems(data.items);
      };
      dataFetch()
    },[])
  if(items == undefined || cookies.get('auth') == undefined)
    return <><HeaderHome/><div className="h-screen"></div></>
  else
    return (
        <>
        <HeaderHome/>      
        <div className=" h-screen flex flex-col items-center">
          <h1 className="text-xl font-bold text-slate-200 text-center">YOUR ITEMS</h1>
          <div className="flex items-center justify-center w-1/2">
            {
            items.map((x) => (
              <>
                <div className="w-full bg-slate-800 border-slate-600 rounded-xl m-5 p-3 flex flex-col items-center justify-center">
                  <h2 className="text-slate-200 font-bold text-lg ">{x.name}</h2>
                  {x.content.startsWith("https:") ? <><a href={x.content}>Go</a></> : <><h2 className="text-slate-200 font-bold text-lg ">{x.content}</h2></>}
                </div>
              </>
            ))
            }
          </div>
        </div>
      </>
    )}