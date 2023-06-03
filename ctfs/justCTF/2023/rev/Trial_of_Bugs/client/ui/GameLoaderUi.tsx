import * as React from 'react';
import {GameLoader} from "../game_loader";
import {useObservableField} from "../util/useObservableField";

export function GameLoaderUi(props: {loader: GameLoader}) {
    const state = useObservableField(props.loader.loadDownload!.state);

    return (
        <>
            <h1 className="load-status">Loading game...&nbsp;&nbsp;&nbsp;{state?.completeRequests || 0}/{state?.allRequests || 0}</h1>
        </>
    );
}
