package ru.mctf

import org.springframework.http.HttpStatus
import org.springframework.web.server.ResponseStatusException
import java.util.*

// Taken and repurposed from https://github.com/joaodelgado/fuck-kotlin/blob/master/src/fuck.kt

fun runProgram(program: String): Char {
    val jumps = matchJumps(program)
    val memSize = 300
    val mem = MutableList(memSize, init = { 0 })
    var pc = 0
    var cursor = 0
    var steps = 0

    while (pc < program.length) {
        when (program[pc]) {
            '+' -> mem[cursor] = (mem[cursor] + 1).mod(256)
            '-' -> mem[cursor] = (mem[cursor] - 1).mod(256)
            '>' -> {
                cursor++
                if (cursor >= memSize) {
                    throw ResponseStatusException(HttpStatus.BAD_REQUEST)
                }
            }
            '<' -> {
                cursor--
                if (cursor < 0) {
                    throw ResponseStatusException(HttpStatus.BAD_REQUEST)
                }
            }
            '[' -> {
                if (mem[cursor] == 0) {
                    pc = jumps[pc] as Int
                }
            }
            ']' -> {
                pc = jumps[pc] as Int
                pc--
            }
            '.' -> throw ResponseStatusException(HttpStatus.NOT_IMPLEMENTED)
            ',' -> throw ResponseStatusException(HttpStatus.NOT_IMPLEMENTED)
        }

        pc++
        steps++

        if (steps > 1_000_000) {
            // Must be an infinite loop
            throw ResponseStatusException(HttpStatus.REQUEST_TIMEOUT)
        }
    }

    return mem[49].toChar()
}

private fun matchJumps(program: String): Map<Int, Int> {
    val stack = Stack<Int>()
    val jumpsMap = HashMap<Int, Int>()
    for ((i, c) in program.withIndex()) {
        when (c) {
            '[' -> stack.push(i)
            ']' -> {
                try {
                    val other = stack.pop()
                    jumpsMap[other] = i
                    jumpsMap[i] = other
                } catch (e: EmptyStackException) {
                    throw ResponseStatusException(HttpStatus.BAD_REQUEST)
                }
            }
        }
    }

    if (!stack.isEmpty()) {
        throw ResponseStatusException(HttpStatus.BAD_REQUEST)
    }

    return jumpsMap
}