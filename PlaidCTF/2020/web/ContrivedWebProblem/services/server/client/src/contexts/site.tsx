import * as React from "react";

export enum SiteKind {
    NOTE_APP = 1,
    FORUM = 2,
    BUG_PORTAL = 3,
};

export const SiteContext = React.createContext({
    kind: SiteKind.NOTE_APP,
});

export let useSiteOption = <T extends any>(noteMsg: T, forumMsg: T, bugMsg: T): T => {
    let { kind } = React.useContext(SiteContext);
    switch (kind) {
        case SiteKind.NOTE_APP:
            return noteMsg
        case SiteKind.FORUM:
            return forumMsg;
        case SiteKind.BUG_PORTAL:
            return bugMsg;
    }
}