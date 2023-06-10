import { HeaderHome, PayComponent } from "../components";
import { useState, useRef, useEffect } from "react";
import { address, headers_post } from "../lib/utils";
import ReCAPTCHA from "react-google-recaptcha";

export default function Report() {
    const [url, setUrl] = useState('')
    const captchaRef = useRef(null)

    const recaptcha_site_key = "6LeySzkmAAAAAL1olc6bun-JnRprdfZIPPP8HP-K";
    
    useEffect(() => {
      const script = document.createElement('script');

      script.src = "https://www.google.com/recaptcha/api.js";
      script.async = true;
      script.defer = true;

      document.body.appendChild(script);
    
      return () => {
        document.body.removeChild(script);
      }
    }, []);


    const handleSubmit = (e)=>  {
      e.preventDefault()
      const captcha_token = captchaRef.current.getValue();
      captchaRef.current.reset();

      var formBody = 'url='+encodeURIComponent(url) + '&captcha=' + encodeURIComponent(captcha_token);
      console.log(formBody)
      fetch(address+'/report', {
          method: 'POST',
          headers: headers_post(),
        body: formBody
      }).then((r=>{
        if (r.status !== 200){
          alert("Error, logout and retry");
          return;
        } 
        r.json().then((r)=>{
          alert(r['response']);
        })
      }))
    }
  
    return (
      <>
        <HeaderHome></HeaderHome>
        <section className="h-screen flex flex-col justify-start space-y-10 items-center my-5 mx-5 ">
          <div className="w-3/4 flex flex-col items-center">
            <h1 className="text-lg text-zinc-200 font-bold p-5">Report a URL to the Admin</h1>
            <form onSubmit={handleSubmit} className="w-full flex flex-col items-center">
              <input className="text-sm w-1/2 px-4 py-2 text-zinc-200 bg-zinc-800 rounded" type="text" placeholder="URL" 
              onChange={(e)=> {
                    setUrl(e.target.value)
              }} />
              <ReCAPTCHA sitekey={recaptcha_site_key} ref={captchaRef}/>
              <input type="submit" className="mt-4 bg-zinc-600 hover:bg-zinc-700 px-4 py-2 text-white uppercase rounded text-xs tracking-wider" value="Report" />
            </form>
          </div>
        </section>
      </>
  );
  }