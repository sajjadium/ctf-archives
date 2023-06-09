export function html(body: string) {
    return new Response(body, {
        headers: {
            'content-type': 'text/html'
        }
    })
}

export function redirect(location: string) {
    return new Response(null, {
        status: 307,
        headers: { location }
    })
}

export function template(content: string) {
    return `<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Secure Login</title>
    <meta name="description" content="Just a pure semantic HTML markup, without .classes.  Built with Pico CSS.">

    <!-- Pico.css (Classless version) -->
    <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.classless.min.css">
</head>

<body>

<main>
    <section>
        ${content}
    </section>
</main>
`
}

export function templateResponse(content: string) {
    return html(template(content))
}
