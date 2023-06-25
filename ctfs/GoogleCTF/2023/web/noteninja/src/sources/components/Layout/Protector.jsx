import { NotesContext } from "@/sources/context/NotesContext";
import Router from "next/router";
import { useContext } from "react";
import { toast } from "react-toastify";
import Loading from "../UI/Loading";

const Protector = ({ children }) => {
  const { login } = useContext(NotesContext);

  if (login.isLoggedIn === undefined) {
    return <Loading />;
  } else if (login.isLoggedIn === false) {
    Router.push("/login");
    return;
  }

  return <>{children}</>;
};

export default Protector;
