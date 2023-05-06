import './App.css';
import React, { useState, useEffect } from 'react';
import { Routes, Route, useLocation } from "react-router-dom";
import { Navigate } from "react-router";

import { Navbar } from './components/Navbar'
import { Document } from './components/Document'
import { DocumentList } from './components/DocumentList'
import { NewDocument } from './components/NewDocument'
import { Home } from './components/Home'
import { Login, Logout, Signup } from './components/Auth'

import 'bootstrap/dist/css/bootstrap.css';
//import 'bootstrap/dist/js/bootstrap.bundle';

function App() {

  const [documents, setDocuments] = useState(undefined);
  const [CSRFToken, setCSRFToken] = useState(undefined);
  const [errorFetchDoc, setErrorFetchDoc] = useState(undefined);

  let location = useLocation()
  React.useEffect(() => {
    (async () => {
      async function fetchCSRFToken() {
        const r = await fetch('/api/getCSRFToken')
        const j = await r.json()
        if (r.status === 200) {
          setCSRFToken(j.CSRFToken)
        }
      }
      async function fetchDocuments() {
        const r = await fetch('/api/document')
        const j = await r.json()
        if (r.status === 200) {
          setErrorFetchDoc(undefined)
          setDocuments(j)
        } else {
          setErrorFetchDoc(j.error || 'failed to fetch documents')
        }
      }

      if (!CSRFToken) {
        await fetchCSRFToken()
      }
      fetchDocuments()
    })()
  }, [location, CSRFToken])

  return <>
    <Navbar />

    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/new" element={<NewDocument CSRFToken={CSRFToken} />} />
      <Route path="/login" element={<Login CSRFToken={CSRFToken} />} />
      <Route path="/signup" element={<Signup CSRFToken={CSRFToken} />} />
      <Route path="/logout" element={<Logout />} />
      <Route path="/document" element={<DocumentList documents={documents} error={errorFetchDoc} />} />
      <Route path="/document/last" element={<Navigate to={documents?.length >= 1 ? '/document/' + documents[documents.length - 1].id : '/document'} />} />
      <Route path="/document/:id" element={<Document CSRFToken={CSRFToken} />} />
    </Routes>
  </>
}

export default App;
