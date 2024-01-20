'use client'
import { useContext, useState } from 'react';
import { useAppContext } from '../../appContext.js';
import { useRouter, redirect } from 'next/navigation'
import styles from './page.module.css'




export default function Auth({ params }: { params: { slug: string } }) {
	const router = useRouter();
	const {jwt, setJwt, API_ROOT, userid, setUserid} = useAppContext();
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");


	function register() {
		fetch(API_ROOT + '/register', {method:'POST', headers: {'Content-Type': 'application/json',}, body: JSON.stringify({"username":username,"password":password}), })
		  .then((res) => res.json())
		  .then((data) => {
		    //asdf
		    setUserid(data.userid);
		    setJwt(data.jwt);
		    router.push("/account");
		 });
	}

	function login() {
		fetch(API_ROOT + '/login', {method:'POST', headers: {'Content-Type': 'application/json',}, body: JSON.stringify({"username":username,"password":password}), })
		  .then((res) => res.json())
		  .then((data) => {
		    //asdf
		    setUserid(data.userid);
		    setJwt(data.jwt);
		    router.push("/account");
		 });
	}

	if(params.slug == "logout") {
		setJwt(null);
		setUserid(null);
		redirect("/auth/login");
	}

	return(<table className={styles.login}>
			<tbody>
				<tr>
				<td>Username</td>
				<td><input type="text" id="username" value={username} onChange={e => setUsername(e.target.value)}/> </td>
				</tr>
				<tr>
				<td>Password</td>
				<td><input type="password" id="password" value={password} onChange={e => setPassword(e.target.value)}/></td>
				</tr>
				<tr>
				<td colSpan="2"><input type="submit" value={params.slug=="register" ? "Register" : "Login"} onClick={params.slug == "register" ? register : login}/></td>
				</tr>
				</tbody>
			</table>)
}