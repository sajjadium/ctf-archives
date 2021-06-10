import * as React from "react";

import { UserContext } from "../contexts/user";
import { SiteContext, useSiteOption, SiteKind } from "../contexts/site";

import { rest } from "../actions/rest";

import { useHistory, unreachable } from "../utils/utils";

import "./home.scss";

export default () => {
    const { data: user, refresh } = React.useContext(UserContext);
    const { kind: siteKind } = React.useContext(SiteContext);
    const [message, setMessage] = React.useState("");
    const [messageTitle, setMessageTitle] = React.useState("");
    let history = useHistory();

    let placeholder = useSiteOption(
        "Save a new note for posterity!",
        "Submit a new post to the forum (multi-users coming soon!)",
        "Describe the bug and how to reproduce it",
    );

    let submission = useSiteOption(
        "Save Note",
        "Upload Post",
        "Post Bug",
    );

    const BugTargets = [
        "MaryRoad",
        "Naught Week Program",
        "Ültimate",
        "Grammm",
        "ConfrontFinances",
        "Blip",
        "Programml",
        "Artemisian",
    ]

    if (user === null) {
        return <></>;
    }

    if (user.kind === "none") {
        history.push("/login");
        return <div/>;
    }

    const uploadPost = async () => {
        let effectiveMessage = messageTitle !== "" ? `${messageTitle}: ${message}` : message;
        await rest("/post", [], { message: effectiveMessage });
        setMessage("");
        refresh();
    }

    return (
        <div className="home">
            <div className="pure-form form">
                {
                    siteKind === SiteKind.BUG_PORTAL
                        ? <input type="text" placeholder="Where did you find the bug?" className="post-title" value={messageTitle} onChange={(e) => setMessageTitle(e.target.value)} />
                        : undefined
                }
                <textarea className="post materialize-textarea" onChange={(e) => setMessage(e.target.value)} placeholder={placeholder}>{message}</textarea>
            </div>

            <input type="button" className="submit-button pure-button btn waves-effect" onClick={uploadPost} value={submission}/>
            {
                siteKind === SiteKind.BUG_PORTAL
                    ? <div className="sub-header">Recent Submissions</div>
                    : undefined
            }
            <div className="messages">
                {
                    user.messages.map(({ message, messageTime }, i) =>
                        siteKind === SiteKind.FORUM
                            ? (
                                <div className={"forum-message"} key={i}>
                                    <div className="forum-header">New post by {user.name} at {(new Date(messageTime)).toLocaleDateString()}</div>
                                    <div className="forum-body">{ message }</div>
                                </div>
                            ) :
                        siteKind === SiteKind.BUG_PORTAL
                            ? (
                                <div className={"bug-message card"} key={i}>
                                    <div className="bug-header">{ message.includes(":") ? message.split(":")[0] : BugTargets[i % BugTargets.length] }</div>
                                    <div className="bug-body">{ message.includes(":") ? message.split(":")[1].trimLeft() : message }</div>
                                </div>
                            ) :
                        <div className={"message card"} key={i}>{ message }</div>
                    )
                }
            </div>
        </div>
    );
}