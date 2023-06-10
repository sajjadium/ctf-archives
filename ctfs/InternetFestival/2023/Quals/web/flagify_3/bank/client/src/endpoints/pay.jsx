import { HeaderHome, PayComponent } from "../components";
import { useLocation } from "react-router"; 
import { parse } from "qs";
import { useState, useEffect } from "react";
import { address, headers } from "../lib/utils";
import Cookies from "universal-cookie";

export function useQs(){
    const location = useLocation();
    return parse(location.search, {
        ignoreQueryPrefix: true,
        decoder: (str) => {
            str = decodeURIComponent(str);
            return str
        }
    });
}
export default function Pay() {
    const cookies = new Cookies()
    const [infos, setInfos] = useState(undefined)
    const [sport_mode, setsport_mode]= useState({})
    const qs= useQs()
    useEffect(()=>{
        const dataFetch = async () => {
            const data = await (
            await fetch(address + '/user')
            ).json();
            setInfos(data); 
        };
        dataFetch()
        setsport_mode(cookies.get('sport_mode'))
    },[])
    if (infos === undefined)
        return (<></>)
    else
        return (
            <>
            <HeaderHome username={infos.username} credit={infos.credit} />
            <div className="flex flex-col items-center justify-start h-screen w-full">
                <PayComponent sport_mode={sport_mode} {...qs} />
            </div>
            </>
        );
}