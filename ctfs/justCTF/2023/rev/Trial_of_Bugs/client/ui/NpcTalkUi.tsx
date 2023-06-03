import * as React from 'react';
import {DialogueModel} from "../../share/game/dialogue_model";
import {useObservableField} from "../util/useObservableField";
import "./NpcTalkUi.css";

export function NpcTalkUi(props: {model: DialogueModel}) {
    const dialogueInfo = useObservableField(props.model.dialogueInfo);
    const choiceInfo = useObservableField(props.model.choiceInfo);

    const displayDialogue = choiceInfo || dialogueInfo;

    return (
        <>
            {displayDialogue && <div className="npc-dialogue-complete-area" onClick={() => props.model.completeDialogue()} />}
            {displayDialogue && <div className="npc-dialogue">
                <h2>{displayDialogue.npcName}</h2>
                <p>{displayDialogue.msg}</p>
            </div>}
            {choiceInfo && <div className="npc-choice">
                {choiceInfo.choices.map((x, i) => <button key={i} onClick={() => props.model.completeChoice(i)}>{x}</button>)}
            </div>}
        </>
    );
}
