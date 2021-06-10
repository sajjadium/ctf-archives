import * as React from "react";
import { ToastContainer } from "react-toastify";
import { PaletteProvider, Palettes } from "react-pwn";

import { UserProvider } from "../../providers/user-provider";
import { ConsoleRouter } from "../router";
import { Header } from "../header";

import "./index.scss";
import 'react-toastify/dist/ReactToastify.css';

export interface Props {

}

export const App = (props: Props) => {
    return (
        <PaletteProvider palette={Palettes.GreenOrange}>
            <ToastContainer position={"bottom-right"}/>
            <UserProvider>
                <div className="main">
                    <Header/>
                    <div className="page">
                        <ConsoleRouter/>
                    </div>
                </div>
            </UserProvider>
        </PaletteProvider>
    )
};