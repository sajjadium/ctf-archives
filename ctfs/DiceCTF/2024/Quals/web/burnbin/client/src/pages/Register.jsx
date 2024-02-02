import React from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

export default function Register() {
  const [user, setUser] = React.useState("");
  const [pass, setPass] = React.useState("");
  const navigate = useNavigate();

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const r = await axios.post("/api/register", { user, pass });
      if (r.data.success) {
        navigate("/home");
      }
    }
    catch (e) {
      alert(e?.response?.data?.message || e.message);
    }
  };

  return (
    <>
      <h3 className="mb-3">Register</h3>
      <form className="d-flex" onSubmit={onSubmit}>
        <fieldset>
        <p>
          <input className="form-control me-sm-2" placeholder="Username" value={user} onChange={e => setUser(e.target.value)} />
        </p>
        <p>
          <input className="form-control me-sm-2" placeholder="Password" value={pass} type="password" onChange={e => setPass(e.target.value)} />
        </p>
        <p>
          <button className="btn btn-primary my-2 my-sm-0" type="submit">Register</button>
        </p>
        </fieldset>
      </form>
      <Link to="/">← Back</Link>
    </>
  );
}