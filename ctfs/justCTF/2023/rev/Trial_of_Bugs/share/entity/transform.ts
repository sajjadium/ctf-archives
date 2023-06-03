import {Component, registerNamedComponent} from "./component";
import {ref} from "./ref";

export class Transform extends Component {
    static typeName = 'transform';

    name: string = '(unnamed)';
    @ref parent?: Transform;
    x: number = 0;
    y: number = 0;
    w: number = 0;
    h: number = 0;

    get centerX() {
        return this.x + this.w / 2;
    }
    get centerY() {
        return this.y + this.h / 2;
    }

    containsPoints(x: number, y: number) {
        return x >= this.x && y >= this.y && x < this.x + this.w && y < this.y + this.h;
    }

    intersects(other: Transform) {
        return other.x < this.x + this.w && other.x + other.w > this.x &&
               other.y < this.y + this.w && other.y + other.w > this.y;
    }
}
registerNamedComponent(Transform);
