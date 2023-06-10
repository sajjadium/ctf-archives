import { HeaderHome,ItemCard } from "../components"
import { address } from "../lib/utils"
import { useState } from "react"
import { useEffect } from "react"

export default function Shop() {
  const [items, setItems] = useState()
  useEffect(()=>{
    const dataFetch = async () => {
      const data = await (
        await fetch(address + '/item')
        ).json();
        setItems(data.items);
      };
      dataFetch()
  },[])

  if(items == undefined)
    return <><HeaderHome/><div className="h-screen"></div></>
  else
    return (
      <>
        <HeaderHome/>      
        <div className=" h-screen">
        <h1 className="text-xl font-bold text-slate-200 text-center">PRICING</h1>
        <div className="flex items-center justify-center">
        {items.map((item, id) => (
          <ItemCard key={item.id} id={item.id} name={item.name} price={item.cost} buy={true}></ItemCard>
        ))}
        </div>
        </div>
      </>
    )
}