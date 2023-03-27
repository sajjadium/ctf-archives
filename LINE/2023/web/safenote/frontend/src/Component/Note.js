import Table from 'react-bootstrap/Table';
import { Link, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

const NOTE_API_URL = "/api/note";


function Note(props) {
  
  props.authRequired();
  const [notes, setNotes] = useState([]);

  useEffect( () => {
    fetch(NOTE_API_URL, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${localStorage.token}`,
            "Content-Type": "application/json",
        }
    }).then(
        res => {
            if(res.status === 200){
                return res.json();
            }
    }).then(
        res => {
            setNotes(res.result);
          }
    )
  }, []);
  
  if(props.auth){
    return (
      
      <div style={{width: "50%", margin:"10px auto"}}>
      <Table >
        <thead>
          <tr>
            <th>Id</th>
            <th>Notes</th>
            <th>Username</th>
            <th>CreateAt</th>
          </tr>
        </thead>
        <tbody>  
          { 
            notes.map((note, index) => (
            (<tr key={index}>
                <td>{note.id}</td>
                <td>{note.note}</td>
                <td>{note.username}</td>
                <td>{note.createdAt}</td>
              </tr>)
            )
          )}
        </tbody>
      </Table>
        <div>  
          <Link to="/create" className='btn btn-primary'> write </Link>
        </div>
      </div>
    )   
  }else{
    return (
      <Navigate to="/login" />
    )
  }
}

export default Note;