import React from "react";
import Navbar from "./Navbar";
import Alert from "./Alert";
import NotesProvider from "@/sources/context/NotesContext";
import Script from "next/script";
import { Roboto } from "next/font/google";

const font = Roboto({
  subsets: ["latin"],
  weight: ["100", "300", "400", "700", "900"],
});

const Layout = ({ children }) => {
  return (
    <div className={font.className}>
      <Script
        src={`https://www.google.com/recaptcha/api.js?render=${process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY}`}
      ></Script>
      <NotesProvider>
        <Navbar />
        <Alert />
        {children}
      </NotesProvider>
    </div>
  );
};

export default Layout;
