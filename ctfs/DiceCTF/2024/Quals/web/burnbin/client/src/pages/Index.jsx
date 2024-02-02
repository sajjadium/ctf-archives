import React from "react";
import { Link } from "react-router-dom";

export default function Index() {
  return (
    <>
      <Link to="/login">
        <button className="btn btn-primary me-2">Login</button>
      </Link>
      <Link to="/register">
        <button className="btn btn-danger">Register</button>
      </Link>
    </>
  );
}