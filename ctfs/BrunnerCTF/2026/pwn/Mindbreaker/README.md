Clone2pwn LEGO
Difficulty: Very Hard
Author: Anakin

INTERNAL MEMO: Automation & Robotics Division

Back when Brunnerne Inc.™ was still a home bakery, someone automated the cake-decorating line with a LEGO MINDSTORMS EV3 brick. Several restructurings later, nobody remembers how the firmware works, but it is load-bearing, so we do not touch it.

To keep the interns billable, IT stood up a self-service EV3 Program Test Bench: upload a program and we will run it on the shared brick, and after a few seconds you receive a picture of its screen. Your program runs under a locked-down service account that cannot read anything it should not.

The rig's maintenance token is stored in /flag.txt on the brick. Access is limited to authorized maintenance personnel.

NOTE: Technical Documentation
The Test Bench runs unmodified third-party controller firmware (LEGO MINDSTORMS lms2012). In accordance with the vendor's license, its full source is published at https://github.com/mindboards/ev3sources. Employees are asked to review it before opening a support ticket.
