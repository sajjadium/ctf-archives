package ru.mctf

import io.micronaut.http.HttpRequest
import io.micronaut.http.MediaType
import io.micronaut.http.annotation.Controller
import io.micronaut.http.annotation.Get
import io.micronaut.http.annotation.Produces
import io.micronaut.http.annotation.QueryValue
import io.micronaut.http.client.RxHttpClient
import io.micronaut.http.client.annotation.Client
import javax.inject.Inject

@Controller("/")
class TaskController {

    @Inject
    @field:Client("/")
    lateinit var client: RxHttpClient

    @Get("/backend/{target:.*}")
    @Produces(MediaType.APPLICATION_JSON)
    fun proxy(@QueryValue("userId") userId: String?, target: String): String {
        return client.toBlocking().retrieve(
            HttpRequest.GET<String>("http://quals-notifications-backend:8081/$target")
                .apply {
                    if (userId != null) {
                        header("X-User-Id", userId)
                    }
                }
        )
    }

    @Get("/healthcheck")
    fun healthcheck(): String {
        return "it works"
    }

}