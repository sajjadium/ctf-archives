import React from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios';

export default function Home() {
  const navigate = useNavigate();

  const [title, setTitle] = React.useState("");
  const [text, setText] = React.useState("");
  const fileRef = React.useRef();

  const [pastes, setPastes] = React.useState(null);

  const [url, setURL] = React.useState("");

  const refresh = async () => {
    try {
      const r = await axios.get(`/api/pastes`);
      if (r.data) {
        setPastes(r.data);
      }
    }
    catch (e) {
      alert(e?.response?.data?.message || e.message);
      navigate("/");
    }
  };

  React.useEffect(() => {
    refresh()
  }, []);

  const onSubmit = (e) => {
    e.preventDefault();
    (async () => {
      try {
        const formData = new FormData();
        formData.append('title', title);
        formData.append('text', text);

        if (fileRef.current.files[0]) {
          formData.append('file', fileRef.current.files[0]);
        }

        const r = await axios.post("/api/create", formData, { headers: { "Content-Type": "multipart/form-data" } });
        if (r.data.success) {
          setTitle("");
          setText("");
          fileRef.current.value = "";
          refresh();
        }
      }
      catch (e) {
        alert(e?.response?.data?.message || e.message);
        navigate("/home");
      }
    })();
  };

  const onSubmitReport = async (e) => {
    e.preventDefault();
    (async () => {
      try {
        const r = await axios.post("/api/submit", { url });
        if (r.data.success) {
          alert(r.data.message);
        }
      }
      catch (e) {
        alert(e?.response?.data?.message || e.message);
        navigate("/home");
      }
    })();
  }

  const deleteAccount = async () => {
    try {
      await axios.post("/api/delete");
    }
    catch (e) {
      alert(e?.response?.data?.message || e.message);
    }
    navigate("/");
  };

  if (!pastes) {
    return <></>
  }

  return (
    <>
      <h5 className="mt-4">Create a paste:</h5>
      <form className="d-flex" onSubmit={onSubmit}>
        <fieldset>
          <p>
            <input className="form-control me-sm-2" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} />
          </p>
          <p>
            <textarea className="form-control me-sm-2" placeholder="Paste contents" value={text} onChange={e => setText(e.target.value)} />
          </p>
          <p>
            <label className="form-label">Image (optional):</label>
            <input className="form-control me-sm-2" type="file" accept="image/png, image/jpeg" ref={fileRef} />
          </p>
          <p>
            <button className="btn btn-primary my-2 my-sm-0" type="submit">Create</button>
          </p>
        </fieldset>
      </form>
      <h5>Your pastes:</h5>
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">Title</th>
            <th scope="col">View</th>
          </tr>
        </thead>
        <tbody>
          { pastes.map((paste, i) => (
            <tr key={i} className="mb-2">
              <th>{paste.title}</th>
              <td><Link to={`/view/${paste.id}`}><button className="btn btn-sm btn-primary">View (this will delete the paste!)</button></Link></td>
            </tr>
          )) }
        </tbody>
      </table>
      <h5>Submit a URL:</h5>
      <form className="d-flex" onSubmit={onSubmitReport}>
        <fieldset>
          <p>
            <input className="form-control me-sm-2" placeholder="http(s)://" value={url} onChange={e => setURL(e.target.value)} />
          </p>
          <p>
            <button className="btn btn-primary my-2 my-sm-0" type="submit">Submit</button>
          </p>
        </fieldset>
      </form>
      <button className="btn btn-danger my-2 my-sm-0" onClick={deleteAccount}>Delete account</button>
    </>
  );
}