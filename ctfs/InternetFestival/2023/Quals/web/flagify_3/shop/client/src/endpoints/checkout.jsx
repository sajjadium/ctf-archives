import { useState } from "react";
import { address, headersPost } from "../lib/utils";
import { useNavigate, useSearchParams } from "react-router-dom";
import Cookies from 'universal-cookie';
import { useEffect } from "react";

export default function Checkout() {
  const cookies = new Cookies()
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams();
  useEffect(()=>{
    if(cookies.get('auth') == undefined){
      navigate('/')
    }
    const dataFetch = async () => {
      var formBody = 'token='+  searchParams.get("token")
      await fetch(address+'/checkout_transaction', {
            method: 'POST',
            headers: headersPost(cookies.get('auth')),
            body: formBody
        }).then(navigate('/items'))
    };
    dataFetch()
    },[])
    return (
        <>
        </>
    );
}
