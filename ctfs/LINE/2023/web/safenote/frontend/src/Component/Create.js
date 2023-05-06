import Form from 'react-bootstrap/Form';
import { Navigate } from 'react-router-dom';

const CREATE_URL_API = "/api/note/create";

function Create(props) {
  props.authRequired();

  const handleCreate = (e) => {
    e.preventDefault();

    fetch(CREATE_URL_API, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({note: e.target[0].value})
    })
        .then(res => {
          if (res.status === 200) {
            window.location.replace("/note");
          }
        })
  }

  if (props.auth){
    return (
        <Form style={{width: "50%", margin: "10px auto"}} onSubmit={handleCreate}>
          <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
            <Form.Label>Note Content</Form.Label>
            <Form.Control as="textarea" controlId="content" rows={3}/>

          </Form.Group>
          <button className='btn btn-primary' type="submit">write</button>
        </Form>
    );
  }else{
    return (
        <Navigate to="/login" />
    );
  }

}

export default Create;