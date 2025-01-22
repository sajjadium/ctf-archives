package com.example.tictactoe

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.Button
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    private lateinit var buttons: Array<Array<Button>>
    private var playerTurn = true // true for X, false for O

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        buttons = Array(3) { r ->
            Array(3) { c ->
                val buttonID = resources.getIdentifier("button$r$c", "id", packageName)
                findViewById<Button>(buttonID)
            }
        }

        for (r in 0..2){
            for (c in 0..2){
                buttons[r][c].setOnClickListener {
                    if (buttons[r][c].text == ""){
                        buttons[r][c].text = if(playerTurn) "X" else "O"
                        if(checkWin()){
                            Toast.makeText(this, "${if(playerTurn) "X" else "O"} wins!", Toast.LENGTH_SHORT).show()
                            resetBoard()
                        } else if (isBoardFull()){
                            Toast.makeText(this, "Draw!", Toast.LENGTH_SHORT).show()
                            resetBoard()
                        }
                        playerTurn = !playerTurn
                    }
                }
            }
        }
    }

    private fun checkWin(): Boolean {
        // Check rows, columns, and diagonals
        for (i in 0..2){
            if(buttons[i][0].text == buttons[i][1].text && buttons[i][1].text == buttons[i][2].text && buttons[i][0].text != ""){
                return true
            }
            if(buttons[0][i].text == buttons[1][i].text && buttons[1][i].text == buttons[2][i].text && buttons[0][i].text != ""){
                return true
            }
        }
        if(buttons[0][0].text == buttons[1][1].text && buttons[1][1].text == buttons[2][2].text && buttons[0][0].text != ""){
            return true
        }
        if(buttons[0][2].text == buttons[1][1].text && buttons[1][1].text == buttons[2][0].text && buttons[0][2].text != ""){
            return true
        }
        return false
    }

    private fun isBoardFull(): Boolean {
        for(row in buttons){
            for(button in row){
                if(button.text == "") return false
            }
        }
        return true
    }

    private fun resetBoard(){
        for(row in buttons){
            for(button in row){
                button.text = ""
            }
        }
    }
}
