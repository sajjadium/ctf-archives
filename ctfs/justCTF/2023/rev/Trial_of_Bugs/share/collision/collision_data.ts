export type CollisionBox = {
    type: 'box',
    x: number,
    y: number,
    w: number,
    h: number,
    rot?: number
}
export type CollisionCircle = {
    type: 'circle',
    x: number,
    y: number,
    radius: number
}
export type CollisionPolygon = {
    type: 'polygon',
    x: number,
    y: number,
    points: {x: number, y: number}[],
    rot?: number
}


export type CollisionItem = CollisionBox | CollisionCircle | CollisionPolygon;
