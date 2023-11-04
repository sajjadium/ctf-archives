const codeSource = document.getElementById('code')
const codeOutput = document.getElementById('code-minified')

document.getElementById('button-minify').addEventListener('click', async () => {
    const params = new URLSearchParams({
        code: codeSource.value
    })
    const response = await fetch(`/minify?${params}`)
    codeOutput.value = await response.text()
})
