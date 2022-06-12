const express = require('express')
const app = express()
const port = 10000

app.get('/', (req, res) => {
    return res.send(`<pre>
flagchecker(1)                                     flagchecker(1)

<b>NAME</b>
       flagchecker - Check your flag

<b>SYNOPSIS</b>
       curl [ <b>-v</b> ] https://flagchecker/check_flag?flag=[1]&otp=[2]
       
       curl [ <b>-v</b> ] https://flagchecker/

<b>DESCRIPTION</b>
       <b>flagchecker</b> is a tool for checking whether a flag is correct.

<b>SEE</b> <b>ALSO</b>
       <b>curl(1)</b>

                            Jun 2022                          1

</pre>`)
})


app.listen(port, () => {
    console.log(`App listening on port ${port}`)
})
process.setMaxListeners(0);