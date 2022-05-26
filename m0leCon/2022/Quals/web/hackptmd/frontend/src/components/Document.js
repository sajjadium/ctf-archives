import { useParams } from "react-router-dom";
import { useState, useEffect, useCallback, useMemo } from "react";
import { SimpleMdeReact } from "react-simplemde-editor";
import SimpleMDE from "easymde";

import { Message } from './Message';

import "easymde/dist/easymde.min.css";


function Document({ CSRFToken }) {
    const [document, setDocument] = useState(undefined);
    const [documentData, setDocumentData] = useState(undefined);
    const [error, setError] = useState(undefined);
    const [reportSucceeded, setReportSucceeded] = useState(false);

    const { id } = useParams()

    useEffect(() => {
        async function fetchDocument(id) {
            setError(undefined)
            const r = await fetch('/api/document/' + id)
            const doc = await r.json()
            if (r.status !== 200) {
                setError(doc.error)
            }
            console.log(doc)
            setDocument(doc)

            setDocumentData(doc.data)
        }
        fetchDocument(id)
    }, [id]);

    const saveChanges = async () => {
        const r = await fetch('/api/document/' + id, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: documentData, _csrf: CSRFToken })
        })

        if (r.status !== 200) {
            const j = await r.json()
            console.log(j)
            setError(j.error || 'failed')
        }
    }

    const reportAbuse = async () => {
        const r = await fetch('/api/report/' + id, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ _csrf: CSRFToken })
        })

        if (r.status === 200) {
            setReportSucceeded(true)
        } else {
            const j = await r.json()
            console.log(j)
            setError(j.error || 'failed')
        }
    }

    const mdeoptions = useMemo(() => {
        return {
            sideBySideFullscreen: false
        }
    }, []);


    const onChange = useCallback((value) => {
        setDocumentData(value);
    }, []);

    const getMdeInstanceCallback = useCallback((simpleMde) => {
        console.log('side')
        SimpleMDE.toggleSideBySide(simpleMde)
    }, []);


    if (error) {
    }

    if (documentData === undefined) {
        if (error) {
            return <Message msg={error} type='error' />
        }
        return <>
            Loading...
        </>
    }

    return <>
        <Message msg={error} type='error' />
        {reportSucceeded ? <Message msg={'Post reported!'} type='success' /> : ''}
        <p class="display-4 text-center">{document?.title}</p>
        <a className="btn btn-outline-secondary" style={{ position: 'absolute', right: '1.5em', top: '5em' }} onClick={saveChanges}>save changes</a>
        <SimpleMdeReact value={documentData} onChange={onChange} options={mdeoptions} getMdeInstance={getMdeInstanceCallback} />
        <div style={{ position: "absolute", bottom: "0", width: "100%", textAlign: "center" }}>
            <a href="#" onClick={reportAbuse}>Report abuse</a>
        </div>
    </>
}

export { Document }