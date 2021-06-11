

Attached is a zip archive containing the source code of a Spring MVC Java web application. Download and extract the archive.

The goal is for you to analyze the code and construct HTTP requests to either (There are multiple sites due to high traffic volume):

    http://challenges.ctfd.io:30542/
    http://challenges.ctfd.io:30541/
    http://challenges.ctfd.io:30543/

This could be accomplished using a web proxy tool such as OWASP ZAP or Burp Suite or your favorite scripting language. It's up to you how you retrieve the flags. Please, no automated scanners or denial of service. Be nice to the application! This is an exercise in precision.

If you would like to run the application locally, inside you'll find a README which instructs you on how to run the application. A pre-built WAR has been provided. The app was created and tested in the following environment:

Ubuntu 20.04 LTS Release: 20.04 openjdk 14.0.2 2020-07-14 OpenJDK Runtime Environment (build 14.0.2+12-Ubuntu-120.04) OpenJDK 64-Bit Server VM (build 14.0.2+12-Ubuntu-120.04, mixed mode, sharing)

When in doubt, read the Spring framework docs!

Note: The flags in the provided source code have been changed in the live app.

