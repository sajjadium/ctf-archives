import * as React from 'react';
import {Connection} from "../connection";
import {NpcTalkUi} from "./NpcTalkUi";
import {QuestListUi} from "./QuestListUi";

export function Game(props: {connection: Connection}) {
    const player = props.connection.player!;

    return (
        <>
            <QuestListUi quest={player.quest} />
            <NpcTalkUi model={player.dialogue} />
        </>
    );
}
