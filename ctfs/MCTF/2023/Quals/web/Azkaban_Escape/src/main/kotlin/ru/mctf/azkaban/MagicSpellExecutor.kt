package ru.mctf.azkaban

import org.springframework.expression.EvaluationContext
import org.springframework.expression.ExpressionParser
import org.springframework.stereotype.Service

@Service
class MagicSpellExecutor(
    private val parser: ExpressionParser,
    private val context: EvaluationContext
) {

    private val bannedChars = setOf('\'', '"', '#', '$')

    fun executeSpell(spell: String): Any? {
        if (spell.any { it in bannedChars }) {
            throw IllegalArgumentException("Forbidden characters")
        }

        val exp = parser.parseExpression(spell)
        return exp.getValue(context)
    }

}