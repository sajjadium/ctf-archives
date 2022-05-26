import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import { Message } from './Message';


function DocumentList({ documents, error }) {

    if (error) {
        return <Message msg={error} type='error' />

    }

    if (documents === undefined) {
        return <>
            Loading...
        </>
    }

    if (documents.length === 0) {
        return <p className="text-center mt-3">Create your first document <Link to="/new">here</Link></p>
    }

    return <div className="mt-3 mx-4">
        <p>Your documents:</p>
        <ul>
            {documents.map(doc => <li key={doc.id}><Link to={'/document/' + doc.id}>{doc.title}</Link></li>)}
        </ul>
    </div>
}

export { DocumentList }