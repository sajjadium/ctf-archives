import {Body, System} from "detect-collisions";
import {CollisionItem} from "./collision_data";

export function createBody(system: System, item: CollisionItem, x: number, y: number, options: {
    isStatic?: boolean,
    isTrigger?: boolean,
    scaleX?: number,
    scaleY?: number
}): Body {
    const mx = options.scaleX || 1;
    const my = options.scaleY || 1;
    if (item.type === 'box') {
        return system.createBox({x: x + item.x * mx, y: y + item.y * my}, item.w * mx, item.h * my, {
            angle: item.rot,
            isStatic: options.isStatic && !options.isTrigger,
            isTrigger: options.isTrigger
        });
    } else if (item.type === 'circle') {
        return system.createCircle({x: x + item.x * mx, y: y + item.y * my}, item.radius * mx, {
            isStatic: options.isStatic && !options.isTrigger,
            isTrigger: options.isTrigger
        });
    } else if (item.type === 'polygon') {
        return system.createPolygon({x: x + item.x * mx, y: y + item.y * my}, item.points, {
            angle: item.rot,
            isStatic: options.isStatic && !options.isTrigger,
            isTrigger: options.isTrigger
        });
    }
    throw new Error('Unknown item type: ' + item);
}
