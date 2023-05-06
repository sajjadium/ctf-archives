/**
 * Author and copyright: Barak Michener (@barakmich)
 * Repository: https://github.com/shaack/cm-chessboard
 * License: MIT, see file 'LICENSE'
 */

import {Extension, EXTENSION_POINT} from "../../model/Extension.js"
import {Svg} from "../../view/ChessboardView.js"

export const ARROW_TYPE = {
    default: {class: "arrow-default", slice: "arrowDefault", headSize: 7},
    danger: {class: "arrow-danger", slice: "arrowDefault", headSize: 7},
    pointy: {class: "arrow-pointy", slice: "arrowPointy", headSize: 7},
}

export class Arrows extends Extension {
    constructor(chessboard, props) {
        super(chessboard, props)
        this.registerExtensionPoint(EXTENSION_POINT.redrawBoard, () => {
            this.onRedrawBoard()
        })
        let defaultProps = {
            sprite: {
                url: "./assets/images/chessboard-arrows.svg",
                size: 40,
                cache: true
            },
        }
        this.props = {}
        Object.assign(this.props, defaultProps)
        Object.assign(this.props, props)
        this.props.sprite = defaultProps.sprite
        if (props.sprite) {
            Object.assign(this.props.sprite, props.sprite)
        }
        if (this.props.sprite.cache) {
            this.chessboard.view.cacheSpriteToDiv("chessboardArrowSpriteCache", this.props.sprite.url)
        }
        this.registerMethod("addArrow", this.addArrow)
        this.registerMethod("getArrows", this.getArrows)
        this.registerMethod("removeArrows", this.removeArrows)
        this.arrowGroup = Svg.addElement(chessboard.view.piecesLayer, "g", {class: "arrows"})
        this.arrows = []
    }

    onRedrawBoard() {
        while (this.arrowGroup.firstChild) {
            this.arrowGroup.removeChild(this.arrowGroup.firstChild)
        }
        this.arrows.forEach((arrow) => {
            this.drawArrow(arrow)
        })
    }

    drawArrow(arrow) {
        const arrowsGroup = Svg.addElement(this.arrowGroup, "g")
        arrowsGroup.setAttribute("data-arrow", arrow.from + arrow.to)
        arrowsGroup.setAttribute("class", "arrow " + arrow.type.class)

        const view = this.chessboard.view
        const sqfrom = document.querySelectorAll('[data-square="' + arrow.from + '"]')[0]
        const sqto = document.querySelectorAll('[data-square="' + arrow.to + '"]')[0]
        const spriteUrl = this.chessboard.props.sprite.cache ? "" : this.chessboard.props.sprite.url
        const defs = Svg.addElement(arrowsGroup, "defs")
        const id = "arrow-" + arrow.from + arrow.to
        const marker = Svg.addElement(defs, "marker", {
            id: id,
            markerWidth: arrow.type.headSize,
            markerHeight: arrow.type.headSize,
            //markerUnits: "userSpaceOnUse",
            refX: 20,
            refY: 20,
            viewBox: "0 0 40 40",
            orient: "auto",
            class: "arrow-head",
        })

        const ignored = Svg.addElement(marker, "use", {
            href: `${spriteUrl}#${arrow.type.slice}`,
        })


        const x1 = sqfrom.x.baseVal.value + (sqfrom.width.baseVal.value / 2)
        const x2 = sqto.x.baseVal.value + (sqto.width.baseVal.value / 2)
        const y1 = sqfrom.y.baseVal.value + (sqfrom.height.baseVal.value / 2)
        const y2 = sqto.y.baseVal.value + (sqto.height.baseVal.value / 2)

        const width = ((view.scalingX + view.scalingY) / 2) * 4
        let lineFill = Svg.addElement(arrowsGroup, "line")
        lineFill.setAttribute('x1', x1)
        lineFill.setAttribute('x2', x2)
        lineFill.setAttribute('y1', y1)
        lineFill.setAttribute('y2', y2)
        lineFill.setAttribute('class', 'arrow-line')
        lineFill.setAttribute("marker-end", "url(#" + id + ")")
        lineFill.setAttribute('stroke-width', width + "px")

    }

    addArrow(type, from, to) {
        if (typeof type === "string" || typeof from === "object" || typeof to === "object") { // todo remove 2022-12-01
            console.error("changed the signature of `addArrow` to `(type, from, to)` with v5.1.x")
            return
        }
        this.arrows.push(new Arrow(from, to, type))
        this.chessboard.view.redrawBoard()
    }

    getArrows(type = undefined, from = undefined, to = undefined) {
        if (typeof type === "string" || typeof from === "object" || typeof to === "object") { // todo remove 2022-12-01
            console.error("changed the signature of `getArrows` to `(type, from, to)` with v5.1.x")
            return
        }
        let arrows = []
        this.arrows.forEach((arrow) => {
            if (arrow.matches(from, to, type)) {
                arrows.push(arrow)
            }
        })
        return arrows
    }

    removeArrows(type = undefined, from = undefined, to = undefined) {
        if (typeof type === "string" || typeof from === "object" || typeof to === "object") { // todo remove 2022-12-01
            console.error("changed the signature of `removeArrows` to `(type, from, to)` with v5.1.x")
            return
        }
        this.arrows = this.arrows.filter((arrow) => !arrow.matches(from, to, type))
        this.chessboard.view.redrawBoard()
    }
}

class Arrow {
    constructor(from, to, type) {
        this.from = from
        this.to = to
        this.type = type
    }

    matches(from = undefined, to = undefined, type = undefined) {
        if (from && from !== this.from) {
            return false
        }
        if (to && to !== this.to) {
            return false
        }
        return !(type && type !== this.type)
    }
}
