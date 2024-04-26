'use client'
import { useContext, useState, useEffect } from 'react'
import { useAppContext } from '../appContext.js';
import { redirect } from 'next/navigation'
import styles from './page.module.css'

export default function Profile() {
  const [profile, setProfiledata] = useState(null);
  const [isLoading, setLoading] = useState(true);
  const {jwt, userid, setUserid, API_ROOT} = useAppContext();

  useEffect(() => {
    fetch(API_ROOT + '/profile', {headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}})
      .then((res) => res.json())
      .then((data) => {
        setProfiledata(data)
        setLoading(false)
      })
  }, [])


  function updateValue(e) {
    let newdata = {... profile};
    newdata[e.target.name] = e.target.value;
    setProfiledata(newdata);
  }

  function updateProfile(e) {
    fetch(API_ROOT + '/profile', {method:'PUT', headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}, body: JSON.stringify(profile), })
      .then((res) => res.json())
      .then((data) => {
        setProfiledata(data)
      })
  }
  if(!jwt) redirect("/auth/login")
  if (isLoading) return <p>Loading...</p>
  if (!profile) return <p>No profile</p>
  
  return (
    <table className={styles.profile}>
      <tbody>
        <tr>
          <td>Firstname</td><td><input type="text" value={profile.firstname} name="firstname" onChange={updateValue}/></td>
        </tr>
        <tr>
          <td>Lastname</td><td><input type="text" value={profile.lastname} name="lastname" onChange={updateValue}/></td>
        </tr>
        <tr>
          <td>Email</td><td><input type="text" value={profile.email} name="email" onChange={updateValue}/></td>
        </tr>
        <tr>
        <td colSpan="2">
          <input type="button" value="Save" onClick={updateProfile}/>
        </td>
        </tr>
      </tbody>
    </table>
  )
}