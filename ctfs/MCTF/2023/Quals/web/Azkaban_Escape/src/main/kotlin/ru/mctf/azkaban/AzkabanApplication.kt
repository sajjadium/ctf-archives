package ru.mctf.azkaban

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class AzkabanApplication

fun main(args: Array<String>) {
    runApplication<AzkabanApplication>(*args)
}
