/**
 * Author and copyright: Stefan Haack (https://shaack.com)
 * Repository: https://github.com/shaack/cm-chessboard
 * License: MIT, see file 'LICENSE'
 */
import {Position} from "./Position.js"

export function createTask() {
    let resolve, reject
    const promise = new Promise(function (_resolve, _reject) {
        resolve = _resolve
        reject = _reject
    })
    promise.resolve = resolve
    promise.reject = reject
    return promise
}

export class ChessboardState {

    constructor() {
        this.position = new Position()
        this.orientation = undefined
        this.markers = []
        this.inputWhiteEnabled = false
        this.inputBlackEnabled = false
        this.inputEnabled = false
        this.squareSelectEnabled = false
        this.extensionPoints = {}
        this.moveInputProcess = createTask().resolve()
    }

    setPosition(fen, animated = false) {
        this.position = new Position(fen, animated)
    }

    movePiece(fromSquare, toSquare, animated = false) {
        const position = this._position.clone()
        position.animated = animated
        const piece = position.getPiece(fromSquare)
        if(!piece) {
            console.error("no piece on", fromSquare)
        }
        position.setPiece(fromSquare, undefined)
        position.setPiece(toSquare, piece)
        this._position = position
    }

    setPiece(square, piece, animated = false) {
        const position = this._position.clone()
        position.animated = animated
        position.setPiece(square, piece)
        this._position = position
    }

    addMarker(square, type) {
        this.markers.push({square: square, type: type})
    }

    removeMarkers(square = undefined, type = undefined) {
        if (!square && !type) {
            this.markers = []
        } else {
            this.markers = this.markers.filter((marker) => {
                if (!type) {
                    if (square === marker.square) {
                        return false
                    }
                } else if (!square) {
                    if (marker.type === type) {
                        return false
                    }
                } else if (marker.type === type && square === marker.square) {
                    return false
                }
                return true
            })
        }
    }

    invokeExtensionPoints(name, data = {}) {
        const extensionPoints = this.extensionPoints[name]
        const dataCloned = Object.assign({}, data);
        dataCloned.extensionPoint = name
        if(extensionPoints) {
            for (const extensionPoint of extensionPoints) {
                setTimeout(() => {
                    extensionPoint(dataCloned)
                })
            }
        }
    }

}
