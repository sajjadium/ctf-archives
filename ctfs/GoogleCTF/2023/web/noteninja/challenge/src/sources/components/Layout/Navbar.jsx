import { NotesContext } from "@/sources/context/NotesContext";
import Link from "next/link";
import React, { useContext } from "react";

const Navbar = () => {
  const { login, logout } = useContext(NotesContext);

  return (
    <div className="bg-[#1e1e1e] text-white p-4 flex items-center justify-between">
      <Link href="/" className="text-xl font-bold">
        Note Ninja 
      </Link>

      <div className="flex items-center gap-4">
        {!login.isLoggedIn ? (
          <>
            <Link
              href="/login"
              className="bg-[#21a56c] w-[70px] h-[35px] rounded flex justify-center items-center pb-0.5 hover:bg-[#1e8e5d] cursor-pointer"
            >
              Login
            </Link>
            <Link
              href="/signup"
              className="bg-[#21a56c] w-[70px] h-[35px] rounded flex justify-center items-center pb-0.5 hover:bg-[#1e8e5d] cursor-pointer"
            >
              Signup
            </Link>
          </>
        ) : (
          <span
            onClick={() => logout()}
            className="bg-[#ca3838] w-[70px] h-[35px] rounded flex justify-center items-center pb-0.5 hover:bg-[#992929] cursor-pointer"
          >
            Logout
          </span>
        )}
      </div>
    </div>
  );
};

export default Navbar;
