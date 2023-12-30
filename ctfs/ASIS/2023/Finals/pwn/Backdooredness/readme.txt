- The challenge is based on https://github.com/amhndu/SimpleNES
- I advice you to use the docker setup to debug you exploit. The following command is used to run the challenge ( important ): 
`mkdir nowhere; chmod 000 nowhere; docker run -v `pwd`/nowhere:/sys -p 1337:1337 backdooredness`
- You are not supposed to have the exact heap layout of remote
