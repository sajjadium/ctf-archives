import * as React from 'react';
import {useObservableField} from "../util/useObservableField";
import "./QuestListUi.css";
import {QuestManager} from "../../share/quest/quest_manager";
import {CheckOn} from "./icons/CheckOn";
import {CheckOff} from "./icons/CheckOff";

export function QuestListUi(props: {quest: QuestManager}) {
    const questList = useObservableField(props.quest.activeQuests);

    return questList && questList.length > 0 ? (
        <div className="quest-list">
            {questList.map(x => (<div className="quest-info" key={x.meta.id}>
                <div className="quest-title">
                    <h4>{x.meta.name}</h4>
                    <div className="quest-title-underline">
                        <div className="u-1"></div>
                        <div className="u-2"></div>
                        <div className="d-1"></div>
                        <div className="d-2"></div>
                        <div className="c-1"></div>
                        <div className="c-2"></div>
                    </div>
                </div>
                {x.taskInfo.map((t,i) => (<div className="quest-info-task" key={x.meta.id + "-" + i + "-" + t.toString()}>
                    <div className="quest-appear-anim"/>
                    {t[1] ? <CheckOn/> : <CheckOff/>}<span>{t[0]}</span>
                </div>))}
            </div>))}
        </div>
    ) : null;
}
