package ooo.localo.hacklu

import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.http.content.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeDriverService
import org.openqa.selenium.chrome.ChromeOptions


fun Application.module() {
    install(ContentNegotiation) {
        json()
    }

    val hints = listOf(System.getenv("HINT") ?: "REDACTED")

    val binary = System.getenv("CHROME_BINARY")
    // set chrome options
    val options = ChromeOptions()
    if (binary != null) {
        // set binary if env var is set
        options.setBinary(binary)
    }
    // don't use /dev/shm otherwise our infra would have to launch this with custom args: --shm-size=..
    options.addArguments("--disable-dev-shm-usage")
    // we don't have a display server inside Docker
    options.addArguments("--headless=true")
    // this is needed for Docker, works without on podman
    options.addArguments("--no-sandbox=true")

    // create the selenium service
    val service = ChromeDriverService.createDefaultService()

    routing {
        // serve static content
        staticResources("/", "static") {
            default("index.html")
        }

        // handler for the /report POST endpoint
        post("/report") {
            val urls = call.receive<List<String>>()
                    .map { url -> Url(url.replace("https://", "http://")) }
            
            // Starts a new chrome instance for the admin bot
            val session = ChromeDriver(service, options)
            val ret = withContext(Dispatchers.IO) {
                urls.map { url ->
                    runCatching {
                        // only allow http links
                        require(url.protocol == URLProtocol.HTTP)
                        val adminURL = URLBuilder(url)
                        // force to visit using localhost (container has no internet connection)
                        adminURL.host = "localhost"
                        // visit website
                        session.get(adminURL.buildString())
                        // wait until js is executed
                        delay(1000L)
                        // return content
                        session.executeScript("return document.documentElement.outerHTML").toString()
                    }.getOrDefault("invalid url")
                }
            }

            // close the chrome instance again
            session.close()

            // send all responses to the client
            call.respond(mapOf(
                    // if there is a ghost, also send a hint
                    "hints" to (hints.takeIf { ret.any { x -> x.indexOf("class=\"ghost\"") > 0 } } ?: listOf()),
                    "ret" to ret
            ))
        }
    }
}