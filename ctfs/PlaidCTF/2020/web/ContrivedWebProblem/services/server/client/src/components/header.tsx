import * as React from "react";

import { SiteContext, SiteKind } from "../contexts/site";
import { unreachable } from "../utils/utils";

import "./header.scss";

export default () => {
    const titles = [
        "Generic",
        "Nothing But a",
        "A Pretty Simple",
        "A Pretty Pathetic",
        "Basically Just a",
        "Boilerplate",
        "I Didn't Work Hard on This",
        "I Can't Believe It's Not a",
        "Really? It's a Bloody",
        "A Gluten Free",
        "zwad3's World Famous",
    ]

    const site = React.useContext(SiteContext);
    const [title, _setTitle] = React.useState(titles[Math.floor(Math.random() * titles.length)]);


    return (
        <div className="header">
            <div className="header-content">
                {title} {" "}
                {
                    site.kind === SiteKind.NOTE_APP ? "Note App" :
                    site.kind === SiteKind.FORUM ? "Forum" :
                    site.kind === SiteKind.BUG_PORTAL ? "Bug Submission Portal" :
                    unreachable(site.kind)
                }
                &trade;
            </div>
        </div>
    )
}