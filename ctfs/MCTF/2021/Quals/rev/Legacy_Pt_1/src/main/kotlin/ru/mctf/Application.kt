package ru.mctf

import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.core.io.Resource
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.server.ResponseStatusException

@SpringBootApplication
class Application

fun main(args: Array<String>) {
    runApplication<Application>(*args)
}

@RestController
class Controller(
    @Value("classpath:program.b")
    programResource: Resource
) {

    private val flag = checkNotNull(System.getenv("MCTF_FLAG"))
    private val log = LoggerFactory.getLogger(Controller::class.java)

    private val passwordRegex = Regex("[A-Za-z0-9]{14}")
    private val charRegex = Regex("[A-Za-z0-9]")
    private val programTemplate = programResource.inputStream.reader().readText()

    @PostMapping("/auth")
    fun auth(@RequestBody password: String): String {
        if (!validatePasswordFormat(password)) {
            throw ResponseStatusException(HttpStatus.FORBIDDEN)
        }

        val preparedPassword = preparePassword(password)
        val program = programTemplate.replace("[password]", preparedPassword)

        val result = runProgram(program)

        log.info("Password is $password, result is $result")

        if (result != '+') {
            throw ResponseStatusException(HttpStatus.FORBIDDEN)
        }

        return flag
    }

    @GetMapping("/healthcheck")
    fun healthcheck() = "ok"

    fun validatePasswordFormat(password: String) =
        password matches passwordRegex

    fun preparePassword(password: String): String {
        return password.replace(charRegex) {
            val letter = it.groupValues[0][0]
            buildString {
                append("+".repeat(letter.code))
                append('>')
            }
        }
    }

}