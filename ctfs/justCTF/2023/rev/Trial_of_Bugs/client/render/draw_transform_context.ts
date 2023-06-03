import {mat4, quat, vec3} from "gl-matrix";
import {Transform} from "../../share/entity/transform";

export class DrawTransformContext {

    private readonly matrixStack: mat4[];
    matrix: mat4;
    private tmpTranslation: vec3;
    private tmpScaling: vec3;
    private tmpQuat: quat;
    private tmpMatrix: mat4;

    constructor() {
        this.matrixStack = [];
        this.matrix = mat4.create();
        this.tmpTranslation = vec3.create();
        this.tmpScaling = vec3.create();
        this.tmpScaling[0] = 1;
        this.tmpScaling[1] = 1;
        this.tmpScaling[2] = 1;
        this.tmpQuat = quat.create();
        this.tmpMatrix = mat4.create();
    }

    push(matrix?: mat4) {
        this.matrixStack.push(matrix || mat4.clone(this.matrix));
    }

    pop() {
        this.matrix = this.matrixStack.pop()!;
    }

    translate(x: number, y: number) {
        this.tmpTranslation[0] = x;
        this.tmpTranslation[1] = y;
        mat4.translate(this.matrix, this.matrix, this.tmpTranslation);
    }

    scale(x: number, y: number) {
        this.tmpScaling[0] = x;
        this.tmpScaling[1] = y;
        mat4.scale(this.matrix, this.matrix, this.tmpScaling);
    }

    applyFromComponent(transform: Transform) {
        this.tmpTranslation[0] = transform.x;
        this.tmpTranslation[1] = transform.y;
        this.tmpScaling[0] = 1;
        this.tmpScaling[1] = 1;
        mat4.fromRotationTranslationScale(this.tmpMatrix, this.tmpQuat, this.tmpTranslation, this.tmpScaling);
        mat4.mul(this.matrix, this.matrix, this.tmpMatrix);
    }

}
