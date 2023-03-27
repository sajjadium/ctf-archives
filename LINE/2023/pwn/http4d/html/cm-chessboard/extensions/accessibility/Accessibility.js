/**
 * Author and copyright: Stefan Haack (https://shaack.com)
 * Repository: https://github.com/shaack/cm-chessboard
 * License: MIT, see file 'LICENSE'
 */
import {Extension, EXTENSION_POINT} from "../../model/Extension.js"
import {piecesTranslations, renderPieceTitle} from "../../view/ChessboardView.js"
import {COLOR, INPUT_EVENT_TYPE} from "../../Chessboard.js"

const hlTranslations = {
    de: {
        pieces_lists: "Figurenlisten",
        board_as_table: "Schachbrett als Tabelle",
        move_piece: "Figur bewegen",
        from: "von",
        to: "nach",
        move: "bewegen",
        input_white_enabled: "Eingabe Weiß aktiviert",
        input_black_enabled: "Eingabe Schwarz aktiviert",
        input_disabled: "Eingabe deaktiviert"
    },
    en: {
        pieces_lists: "Pieces lists",
        board_as_table: "Chessboard as table",
        move_piece: "Move piece",
        from: "from",
        to: "to",
        move: "move",
        input_white_enabled: "Input white enabled",
        input_black_enabled: "Input black enabled",
        input_disabled: "Input disabled"
    }
}

export class Accessibility extends Extension {

    constructor(chessboard, props) {
        super(chessboard, props)
        this.props = {
            brailleNotationInAlt: true, // show the braille notation of the position in the alt attribute of the SVG image
            boardAsTable: false, // display the board additionally as HTML table
            movePieceForm: false, // display a form to move a piece (from, to, move)
            piecesAsList: false, // display the pieces additionally as List
            visuallyHidden: true // hide all those extra outputs visually but keep them accessible for screen readers and braille displays
        }
        Object.assign(this.props, props)
        this.lang = chessboard.props.language
        this.translations = piecesTranslations
        this.t = this.translations[this.lang]
        this.th = hlTranslations[this.lang]
        if (this.props.movePieceForm) {
            this.movePieceFormContainer = this.createElement(`<div><h3>${this.th.move_piece}</h3><form>
            <label for="move_piece_input_from_${chessboard.id}">${this.th.from}</label><input class="input-from" type="text" size="2" id="move_piece_input_from_${chessboard.id}"/>
            <label for="move_piece_input_to_${chessboard.id}">${this.th.to}</label><input class="input-to" type="text" size="2" id="move_piece_input_to_${chessboard.id}"/>
            <button type="submit" class="button-move">${this.th.move}</button>
            </form><div class="input-status" aria-live="polite"></div></div>`)
            this.form = this.movePieceFormContainer.querySelector("form")
            this.inputFrom = this.form.querySelector(".input-from")
            this.inputTo = this.form.querySelector(".input-to")
            this.moveButton = this.form.querySelector(".button-move")
            if (this.props.visuallyHidden) {
                this.movePieceFormContainer.classList.add("cm-visually-hidden")
            }
            this.form.addEventListener("submit", (evt) => {
                evt.preventDefault()
                if (this.chessboard.view.moveInputCallback({
                    chessboard: this.chessboard,
                    type: INPUT_EVENT_TYPE.validateMoveInput,
                    squareFrom: this.inputFrom.value,
                    squareTo: this.inputTo.value
                })) {
                    this.chessboard.movePiece(this.inputFrom.value, this.inputTo.value,
                        true).then(() => {
                        this.inputFrom.value = ""
                        this.inputTo.value = ""
                    })
                }
            })
            this.chessboard.context.appendChild(this.movePieceFormContainer)
        }
        if (this.props.boardAsTable) {
            this.boardAsTableContainer = this.createElement(`<div><h3>${this.th.board_as_table}</h3><div class="table"></div></div>`)
            this.boardAsTable = this.boardAsTableContainer.querySelector(".table")
            this.chessboard.context.appendChild(this.boardAsTableContainer)
            if (this.props.visuallyHidden) {
                this.boardAsTableContainer.classList.add("cm-visually-hidden")
            }
        }
        if (this.props.piecesAsList) {
            this.piecesListContainer = this.createElement(`<div><h3>${this.th.pieces_lists}</h3><div class="list"></div></div>`)
            this.piecesList = this.piecesListContainer.querySelector(".list")
            this.chessboard.context.appendChild(this.piecesListContainer)
            if (this.props.visuallyHidden) {
                this.piecesListContainer.classList.add("cm-visually-hidden")
            }
        }
        this.registerExtensionPoint(EXTENSION_POINT.moveInput, () => {
            this.updateFormInputs()
        })
        this.registerExtensionPoint(EXTENSION_POINT.moveInputToggled, () => {
            this.updateFormInputs()
        })
        this.registerExtensionPoint(EXTENSION_POINT.positionChanged, () => {
            if(this.chessboard.state) { // not destroyed
                this.redrawPositionInAltAttribute()
                if (this.props.boardAsTable) {
                    this.redrawBoardAsTable()
                }
                if (this.props.piecesAsList) {
                    this.redrawPiecesLists()
                }
            }
        })
        this.registerExtensionPoint(EXTENSION_POINT.boardChanged, () => {
            console.log("EXTENSION_POINT.boardChanged")
            if (this.props.boardAsTable) {
                this.redrawBoardAsTable()
            }
        })
        this.redrawPositionInAltAttribute()
        if (this.props.boardAsTable) {
            this.redrawBoardAsTable()
        }
        if (this.props.piecesAsList) {
            this.redrawPiecesLists()
        }
    }

    updateFormInputs() {
        if (this.inputFrom) {
            if (this.chessboard.state.inputWhiteEnabled || this.chessboard.state.inputBlackEnabled) {
                this.inputFrom.disabled = false
                this.inputTo.disabled = false
                this.moveButton.disabled = false
            } else {
                this.inputFrom.disabled = true
                this.inputTo.disabled = true
                this.moveButton.disabled = true
            }
        }
    }

    redrawPositionInAltAttribute() {
        const pieces = this.chessboard.state.position.getPieces()
        let listW = piecesTranslations[this.lang].colors.w.toUpperCase() + ":"
        let listB = piecesTranslations[this.lang].colors.b.toUpperCase() + ":"
        for (const piece of pieces) {
            const pieceName = piece.name === "p" ? "" : piecesTranslations[this.lang].pieces[piece.name].toUpperCase()
            if (piece.color === "w") {
                listW += " " + pieceName + piece.position
            } else {
                listB += " " + pieceName + piece.position
            }
        }
        const altText = `${listW}
${listB}`
        this.chessboard.view.svg.setAttribute("alt", altText)
    }

    redrawPiecesLists() {
        const pieces = this.chessboard.state.position.getPieces()
        let listW = ""
        let listB = ""
        for (const piece of pieces) {
            if (piece.color === "w") {
                listW += `<li class="list-inline-item">${renderPieceTitle(this.lang, piece.name)} ${piece.position}</li>`
            } else {
                listB += `<li class="list-inline-item">${renderPieceTitle(this.lang, piece.name)} ${piece.position}</li>`
            }
        }
        this.piecesList.innerHTML = `
        <h4 id="white_${this.chessboard.id}">${this.t.colors_long.w}</h4>
        <ul aria-labelledby="white_${this.chessboard.id}" class="list-inline">${listW}</ul>
        <h4 id="black_${this.chessboard.id}">${this.t.colors_long.b}</h4>
        <ul aria-labelledby="black_${this.chessboard.id}" class="list-inline">${listB}</ul>`
    }

    redrawBoardAsTable() {
        const squares = this.chessboard.state.position.squares.slice()
        const ranks = ["a", "b", "c", "d", "e", "f", "g", "h"]
        const files = ["8", "7", "6", "5", "4", "3", "2", "1"]
        if (this.chessboard.state.orientation === COLOR.black) {
            ranks.reverse()
            files.reverse()
            squares.reverse()
        }
        let html = `<table><!--<caption>${this.th.board_as_table}</caption>--><tr><th></th>`
        for (const rank of ranks) {
            html += `<th scope='col'>${rank}</th>`
        }
        html += "</tr>"
        for (let x = 7; x >= 0; x--) {
            html += `<tr><th scope="row">${files[7 - x]}</th>`
            for (let y = 0; y < 8; y++) {
                const pieceCode = squares[y % 8 + x * 8]
                let color, name
                if (pieceCode) {
                    color = pieceCode.charAt(0)
                    name = pieceCode.charAt(1)
                    html += `<td>${renderPieceTitle(this.lang, name, color)}</td>`
                } else {
                    html += `<td></td>`
                }
            }
            html += "</tr>"
        }
        html += "</table>"
        this.boardAsTable.innerHTML = html
    }

    createElement(html) {
        const template = document.createElement('template')
        template.innerHTML = html.trim()
        return template.content.firstChild
    }

}
