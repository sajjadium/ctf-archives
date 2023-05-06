/**
 * Author and copyright: Stefan Haack (https://shaack.com)
 * Repository: https://github.com/shaack/cm-chessboard
 * License: MIT, see file 'LICENSE'
 */
import {FEN, Position} from "../model/Position.js"
import {Svg} from "./ChessboardView.js"

/*
* Thanks to markosyan for the idea of the PromiseQueue
* https://medium.com/@karenmarkosyan/how-to-manage-promises-into-dynamic-queue-with-vanilla-javascript-9d0d1f8d4df5
*/

export class PromiseQueue {

    constructor() {
        this.queue = []
        this.workingOnPromise = false
        this.stop = false
    }

    async enqueue(promise) {
        return new Promise((resolve, reject) => {
            this.queue.push({
                promise, resolve, reject,
            })
            this.dequeue()
        })
    }

    dequeue() {
        if (this.workingOnPromise) {
            return
        }
        if (this.stop) {
            this.queue = []
            this.stop = false
            return
        }
        const entry = this.queue.shift()
        if (!entry) {
            return
        }
        try {
            this.workingOnPromise = true
            entry.promise().then((value) => {
                this.workingOnPromise = false
                entry.resolve(value)
                this.dequeue()
            }).catch(err => {
                this.workingOnPromise = false
                entry.reject(err)
                this.dequeue()
            })
        } catch (err) {
            this.workingOnPromise = false
            entry.reject(err)
            this.dequeue()
        }
        return true
    }

    destroy() {
        this.stop = true
    }

}


const CHANGE_TYPE = {
    move: 0,
    appear: 1,
    disappear: 2
}

export class PositionsAnimation {

    constructor(view, fromPosition, toPosition, duration, callback) {
        this.view = view
        if (fromPosition && toPosition) {
            this.animatedElements = this.createAnimation(fromPosition.squares, toPosition.squares)
            this.duration = duration
            this.callback = callback
            this.frameHandle = requestAnimationFrame(this.animationStep.bind(this))
        } else {
            console.error("fromPosition", fromPosition, "toPosition", toPosition)
        }
    }

    static seekChanges(fromSquares, toSquares) {
        const appearedList = [], disappearedList = [], changes = []
        for (let i = 0; i < 64; i++) {
            const previousSquare = fromSquares[i]
            const newSquare = toSquares[i]
            if (newSquare !== previousSquare) {
                if (newSquare) {
                    appearedList.push({piece: newSquare, index: i})
                }
                if (previousSquare) {
                    disappearedList.push({piece: previousSquare, index: i})
                }
            }
        }
        appearedList.forEach((appeared) => {
            let shortestDistance = 8
            let foundMoved = undefined
            disappearedList.forEach((disappeared) => {
                if (appeared.piece === disappeared.piece) {
                    const moveDistance = PositionsAnimation.squareDistance(appeared.index, disappeared.index)
                    if (moveDistance < shortestDistance) {
                        foundMoved = disappeared
                        shortestDistance = moveDistance
                    }
                }
            })
            if (foundMoved) {
                disappearedList.splice(disappearedList.indexOf(foundMoved), 1) // remove from disappearedList, because it is moved now
                changes.push({
                    type: CHANGE_TYPE.move,
                    piece: appeared.piece,
                    atIndex: foundMoved.index,
                    toIndex: appeared.index
                })
            } else {
                changes.push({type: CHANGE_TYPE.appear, piece: appeared.piece, atIndex: appeared.index})
            }
        })
        disappearedList.forEach((disappeared) => {
            changes.push({type: CHANGE_TYPE.disappear, piece: disappeared.piece, atIndex: disappeared.index})
        })
        return changes
    }

    createAnimation(fromSquares, toSquares) {
        const changes = PositionsAnimation.seekChanges(fromSquares, toSquares)
        // console.log("changes", changes)
        const animatedElements = []
        changes.forEach((change) => {
            const animatedItem = {
                type: change.type
            }
            switch (change.type) {
                case CHANGE_TYPE.move:
                    animatedItem.element = this.view.getPieceElement(Position.indexToSquare(change.atIndex))
                    animatedItem.element.parentNode.appendChild(animatedItem.element) // move element to top layer
                    animatedItem.atPoint = this.view.indexToPoint(change.atIndex)
                    animatedItem.toPoint = this.view.indexToPoint(change.toIndex)
                    break
                case CHANGE_TYPE.appear:
                    animatedItem.element = this.view.drawPiece(Position.indexToSquare(change.atIndex), change.piece)
                    animatedItem.element.style.opacity = 0
                    break
                case CHANGE_TYPE.disappear:
                    animatedItem.element = this.view.getPieceElement(Position.indexToSquare(change.atIndex))
                    break
            }
            animatedElements.push(animatedItem)
        })
        return animatedElements
    }

    animationStep(time) {
        // console.log("animationStep", time)
        if (!this.startTime) {
            this.startTime = time
        }
        const timeDiff = time - this.startTime
        if (timeDiff <= this.duration) {
            this.frameHandle = requestAnimationFrame(this.animationStep.bind(this))
        } else {
            cancelAnimationFrame(this.frameHandle)
            // console.log("ANIMATION FINISHED")
            this.animatedElements.forEach((animatedItem) => {
                if (animatedItem.type === CHANGE_TYPE.disappear) {
                    Svg.removeElement(animatedItem.element)
                }
            })
            this.callback()
            return
        }
        const t = Math.min(1, timeDiff / this.duration)
        let progress = t < .5 ? 2 * t * t : -1 + (4 - 2 * t) * t // easeInOut
        if (isNaN(progress)) {
            progress = 1
        }
        this.animatedElements.forEach((animatedItem) => {
            // console.log("animatedItem", animatedItem)
            if (animatedItem.element) {
                switch (animatedItem.type) {
                    case CHANGE_TYPE.move:
                        animatedItem.element.transform.baseVal.removeItem(0)
                        const transform = (this.view.svg.createSVGTransform())
                        transform.setTranslate(
                            animatedItem.atPoint.x + (animatedItem.toPoint.x - animatedItem.atPoint.x) * progress,
                            animatedItem.atPoint.y + (animatedItem.toPoint.y - animatedItem.atPoint.y) * progress)
                        animatedItem.element.transform.baseVal.appendItem(transform)
                        break
                    case CHANGE_TYPE.appear:
                        animatedItem.element.style.opacity = Math.round(progress * 100) / 100
                        break
                    case CHANGE_TYPE.disappear:
                        animatedItem.element.style.opacity = Math.round((1 - progress) * 100) / 100
                        break
                }
            } else {
                console.warn("animatedItem has no element", animatedItem)
            }
        })
    }

    static squareDistance(index1, index2) {
        const file1 = index1 % 8
        const rank1 = Math.floor(index1 / 8)
        const file2 = index2 % 8
        const rank2 = Math.floor(index2 / 8)
        return Math.max(Math.abs(rank2 - rank1), Math.abs(file2 - file1))
    }

}

export class PositionAnimationsQueue extends PromiseQueue {

    constructor(chessboard) {
        super()
        this.chessboard = chessboard
    }

    async enqueuePositionChange(positionFrom, positionTo, animated) {
        if(positionFrom.getFen() === positionTo.getFen()) {
            return Promise.resolve()
        } else {
            return super.enqueue(() => new Promise((resolve) => {
                let duration = animated ? this.chessboard.props.animationDuration : 0
                if (this.queue.length > 0) {
                    duration = duration / (1 + Math.pow(this.queue.length / 5, 2))
                }
                // console.log("duration", duration, animated, "this.chessboard.props.animationDuration", this.chessboard.props.animationDuration)
                new PositionsAnimation(this.chessboard.view,
                    positionFrom, positionTo, animated ? duration : 0,
                    () => {
                        if (this.chessboard.view) { // if destroyed, no view anymore
                            this.chessboard.view.redrawPieces(positionTo.squares)
                        }
                        resolve()
                    }
                )
            }))
        }
    }

    async enqueueTurnBoard(position, color, animated) {
        return super.enqueue(() => new Promise((resolve) => {
            const emptyPosition = new Position(FEN.empty)
            let duration = animated ? this.chessboard.props.animationDuration : 0
            if(this.queue.length > 0) {
                duration = duration / (1 + Math.pow(this.queue.length / 5, 2))
            }
            new PositionsAnimation(this.chessboard.view,
                position, emptyPosition, animated ? duration : 0,
                () => {
                    this.chessboard.state.orientation = color
                    this.chessboard.view.redrawBoard()
                    this.chessboard.view.redrawPieces(emptyPosition.squares)
                    new PositionsAnimation(this.chessboard.view,
                        emptyPosition, position, animated ? duration : 0,
                        () => {
                            this.chessboard.view.redrawPieces(position.squares)
                            resolve()
                        }
                    )
                }
            )
        }))
    }

}
