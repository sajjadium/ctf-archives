'use client'
import { useContext, useState, useEffect } from 'react'
import { useAppContext } from '../appContext.js';
import styles from './page.module.css'
import { redirect } from 'next/navigation'


function Transactions({batchid,accountdata,pshow,verified,senderid,displayError}) {
  const [isLoading, setLoading] = useState(true);
  const [transactions,setTransactions] = useState([])
  const {jwt, userid, setUserid, API_ROOT} = useAppContext();
  const [txForm, setTxForm] = useState(false);
  const [sender, setSender] = useState(0);
  const [recipient, setRecipient] = useState(0);
  const [amount, setAmount] = useState(0);

  useEffect(() => {
    fetch(API_ROOT + '/transactions?batchid='+batchid,{headers: {'Authorization': 'Bearer ' + jwt}})
      .then((res) => res.json())
      .then((data) => {
        setTransactions(data)
        setSender(Object.keys(accountdata)[0])
        setRecipient(Object.keys(accountdata)[0])
        setLoading(false)
      })
  }, []);


  function newTx() {
    fetch(API_ROOT + '/transfer', {method:'POST', headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}, body: JSON.stringify({'batchid':batchid,'recipient':recipient,'amount':amount})})
      .then((res) => res.json())
      .then((data) => {
        if(!("error" in data)) {
          setTransactions(data);
        }
        else {
          displayError(data.error);
        }
     });
  }

  function removeTx(e) {
    fetch(API_ROOT + '/transactions?batchid='+batchid, {method:'DELETE', headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}, body: JSON.stringify({'txid':e.target.name})})
      .then((res) => res.json())
      .then((data) => {
        setTransactions(data);
     });
  }

  function showTxForm() {
    setTxForm(true);
  }

  if (!jwt) redirect("/auth/login")

  let display = []
  transactions.map((transaction) => {
    display.push(
      <div key={transaction.txid} className={styles.transaction}>
        <div>Recipient : {transaction.recipientname}</div>
        <div>Amount : {transaction.amount}</div>
        {!verified && <button className={styles.delete} name={transaction.txid} onClick={removeTx}>x</button>}
      </div>
      )
  });
  let displayaccounts = []
  for (const [id, data] of Object.entries(accountdata)) {
    displayaccounts.push(
      <option key={"option_"+id} value={id}>{accountdata[id]["name"]} (Balance : {accountdata[id]["balance"]})</option>
      )
  };

  let selectedAccount = accountdata[senderid]

  return(
      <div>
      {display}
      {!verified &&
        <div className={styles.createtx}>
            <div className={styles.recipient}>Recipient: &nbsp;
            <select className={styles.account} value={recipient} onChange={e => setRecipient(e.target.value)}>
              {displayaccounts}
            </select>
            </div>
            <div>Amount: <input type="text" value={amount} onChange={e => setAmount(e.target.value)} className={accountdata[senderid].balance < amount  ? styles.unacceptable : styles.good}/></div>
            <button className={styles.add} onClick={newTx} disabled={accountdata[senderid].balance < amount}>+</button> 
        </div>
      }
      </div>
    )
}

export default function MainTransactions() {
  const [isLoading, setLoading] = useState(true);
  const [batches, setBatches] = useState([]);
  const {jwt, userid, setUserid, API_ROOT} = useAppContext();
  const [accountdata, setAccountdata] = useState({});
  const [bdisplay,setBdisplay] = useState([]);
  const [selectedAccount,setSelectedAccount] = useState(0);

  useEffect(() => {
    fetch(API_ROOT + '/accounts',{headers: {'Authorization': 'Bearer ' + jwt}})
      .then((res) => res.json())
      .then((data) => {
        setAccountdata(data)
        setSelectedAccount(Object.keys(data)[0]);
        setLoading(false)
      })
  }, [])
 

  useEffect(() => {
    fetch(API_ROOT + '/batches',{headers: {'Authorization': 'Bearer ' + jwt}})
      .then((res) => res.json())
      .then((data) => {
        setBatches(data)
        setLoading(false)
      })
  }, [])

  function displayError(msg) {
    window.alert(msg);
  }


  function newBatch() {
    fetch(API_ROOT + '/batch/new', {method:'POST', headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}, body: JSON.stringify({'senderid':selectedAccount})})
      .then((res) => res.json())
      .then((data) => {
        if("error" in data) {
          displayError(data.error);
        }
        else {
          setBatches(data);
        }
     });
  }

  function validateBatch(e) {
    if(confirm("Are you sure? This action is irreversible")) {
      fetch(API_ROOT + '/validate', {method:'POST', headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}, body: JSON.stringify({'batchid':e.target.name})})
        .then((res) => res.json())
        .then((data) => {
          if("error" in data) {
            displayError(data.error);
          }
          else {
            fetch(API_ROOT + '/accounts',{headers: {'Authorization': 'Bearer ' + jwt}})
            .then((res) => res.json())
            .then((data) => {
              setAccountdata(data)
              setSelectedAccount(Object.keys(data)[0]);
              setLoading(false)
            })
            setBatches(data);
          }
       });
      }
  }

function removeBatch(e) {
  fetch(API_ROOT + '/batches', {method:'DELETE', headers: {'Content-Type': 'application/json','Authorization': 'Bearer ' + jwt}, body: JSON.stringify({'batchid':e.target.name})})
      .then((res) => res.json())
      .then((data) => {
        //asdf
        setBatches(data);
     });
  }

  function toggleBatch(e) {
    let mydisplay = [... bdisplay];
    if(mydisplay.includes(e.target.id)) {
      mydisplay.splice(mydisplay.indexOf(e.target.id));
    } 
    else {
      mydisplay.push(e.target.id);
    }
    setBdisplay(mydisplay);
  }
  if (!jwt) redirect("/auth/login")
  if (isLoading) return <p>Loading...</p>

  let display = [];

  let displayaccounts = []
  for (const [id, data] of Object.entries(accountdata)) {
    displayaccounts.push(
      <option key={"option_"+id} value={id}>{accountdata[id]["name"]} (Balance : {accountdata[id]["balance"]})</option>
      )
  };

  batches.map((batch) => {
    display.push(
      <div key={batch.batchid} className={styles.batch}>
        <div className={styles.batchhead}>
        {!batch.verified && !batch.executed && 
        <span>
          <button name={batch.batchid} title="Validate batch" className={styles.validate} onClick={validateBatch}>&#x2705;</button>
          <button name={batch.batchid} title="Cancel batch" className={styles.delete} onClick={removeBatch}>X</button>
        </span>
      }
          <div  className={styles.sourcename}>Source account: {batch.sendername} </div>
          <input className={styles.batchcheckbox} title="Validated" type="checkbox" checked={batch.verified} readOnly/>
          <input className={styles.batchcheckbox} title="Executed" type="checkbox" checked={batch.executed} readOnly/>
          <span id={batch.batchid} onClick={toggleBatch} className={styles.toggle}>{bdisplay.includes(batch.batchid) ? '▲' : '▼'}</span>

      
        </div>
        {bdisplay.includes(batch.batchid)  && 
          <Transactions batchid={batch.batchid} accountdata={accountdata} verified={batch.verified} senderid={batch.senderid} displayError={displayError}/>
        }
       
      </div>
    );
  })
  return (
    <div>
      <div className={styles.new} style={{textAlign: 'center'}}>Create new transaction batch from account <select className={styles.account} value={selectedAccount} onChange={e => setSelectedAccount(e.target.value)}>
              {displayaccounts}
            </select>
            &nbsp;<button className={styles.add} onClick={newBatch}>+</button>
          </div>
        {display}
    </div>
  )
}