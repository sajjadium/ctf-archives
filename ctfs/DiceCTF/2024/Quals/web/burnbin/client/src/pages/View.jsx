import React from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import axios from 'axios';

export default function View() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [paste, setPaste] = React.useState(null);

  React.useEffect(() => {
    (async () => {
      try {
        const r = await axios.get(`/api/paste/${id}`);
        if (r.data) {
          setPaste(r.data);
          if (!r.data.image) {
            await deletePaste(r.data.id);
          }
        }
      }
      catch (e) {
        alert(e?.response?.data?.message || e.message);
        navigate("/home");
      }
    })();
  }, []);

  const deletePaste = async (id) => {
    try {
      await axios.get(`/api/destroy/${id}`);
    }
    catch (e) {
      alert(e?.response?.data?.message || e.message);
      navigate("/home");
    }
  };

  if (!paste) {
    return <></>
  }

  return (
    <>
      <h3>{paste.title}</h3>
      { paste.image && (
        <img src={`/uploads/${paste.image}`} onLoad={() => deletePaste(paste.id)} onError={() => deletePaste(paste.id)} className="mw-100" />
      )}
      <div style={{ whiteSpace: "pre-line" }} className="mb-2">{paste.text}</div>
      <Link to="/home">← Back</Link>
    </>
  );
}