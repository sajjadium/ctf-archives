package ru.mctf.azkaban

import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/magic")
class SpellController(
    private val executor: MagicSpellExecutor
) {

    @PostMapping
    fun testSpell(@RequestBody spell: String): Any? {
        return executor.executeSpell(spell)
    }

}