import {Component, registerNamedComponent} from "../entity/component";

export class PersistFlag extends Component {
    static typeName = 'persist_flag';
}
registerNamedComponent(PersistFlag);
