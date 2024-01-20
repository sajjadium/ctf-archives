'use client'
import { useContext, useState, useEffect } from 'react'
import { useAppContext } from '../appContext.js';
import { redirect } from 'next/navigation'
import styles from './page.module.css'

export default function Account() {
  const [accountdata, setAccountdata] = useState({});
  const [isLoading, setLoading] = useState(true);
  const {jwt, userid, setUserid, API_ROOT} = useAppContext();

  useEffect(() => {
    fetch(API_ROOT + '/accounts', {headers: {'Authorization': 'Bearer ' + jwt}})
      .then((res) => res.json())
      .then((data) => {
        setAccountdata(data)
        setLoading(false)
      })
  }, [])

  function updateValue(e: React.ChangeEvent<object>) {
  	let newdata = {... (accountdata as object)};
  	newdata[e.target.name]["name"] = e.target.value;
  	setAccountdata(newdata);

  }
 
  function updateAccounts(e) {
  	
  	fetch(API_ROOT + '/accounts', {method:'PUT', headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}, body: JSON.stringify(accountdata), })
      .then((res) => res.json())
      .then((data) => {
        setAccountdata(data)
      })
  }
  if (!jwt) redirect("/auth/login")
  if (isLoading) return <p>Loading...</p>
  if (!accountdata) return <p>No accounts</p>
  let accounts = [];
  let totalbalance = 0;
  for (const [id, data] of Object.entries(accountdata)) {
  	totalbalance = totalbalance + parseFloat(data.balance);
   	accounts.push(
		  	<tr key={id}>
		  		<td><input type="text" name={id} value={data.name} onChange={updateValue}/></td>
		  		<td>{data.balance} CHF</td>
		  	</tr>
  		);
  }

  return (
  	<div>
  	<table className={styles.account}>
  			<thead>
  				<tr>
	  				<th>Account name</th>
	  				<th>Account balance</th>
  				</tr>
  			</thead>
  			<tbody>
		  		{accounts}
		  		<tr>
		  		<td>TOTAL</td>
		  		<td>{totalbalance.toFixed(2)} CHF</td>
		  		</tr>
		  		<tr>
		  		<td colSpan="2">
		  		<input type="button" value="Save" onClick={updateAccounts}/>
		  		</td>
		  		</tr>
	  		</tbody>
  		</table>
    	
    </div>
  )
}