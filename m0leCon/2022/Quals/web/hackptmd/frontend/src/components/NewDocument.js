import { useNavigate } from "react-router-dom";
import { useState } from "react";

import { Message } from './Message';

function NewDocument({ CSRFToken }) {

    const [error, setError] = useState(undefined);

    const navigate = useNavigate()
    const goToDocument = (id) => navigate('/document/' + id);

    const createNewDocument = async (e) => {
        e.preventDefault()
        const title = document.getElementById('title').value

        const r = await fetch('/api/document', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title, _csrf: CSRFToken })
        })

        if (r.status !== 200) {
            const j = await r.json()
            console.log(j)
            setError(j.error || "Creation failed")
        } else {
            const { id } = await r.json()
            goToDocument(id)
        }
    }

    return <>
        <Message msg={error} type='error' />

        <p className="h2 text-center my-4 pb-3">Create a new document</p>

        <form className="mx-auto col-xl-3 col-lg-5 col-md-6 col-sm-8" onSubmit={createNewDocument}>
            <div class="input-group mb-3">
                <input className="form-control" type="text" id="title" placeholder="title" />
                <button className="btn btn-primary" type="submit">Create</button>
            </div>
        </form>

    </>
}

export { NewDocument }