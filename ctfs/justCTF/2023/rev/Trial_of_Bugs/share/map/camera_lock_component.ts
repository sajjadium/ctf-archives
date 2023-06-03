import {Component, registerNamedComponent} from "../entity/component";

export class CameraLockComponent extends Component {
    static typeName = 'camera_lock';
}
registerNamedComponent(CameraLockComponent);
