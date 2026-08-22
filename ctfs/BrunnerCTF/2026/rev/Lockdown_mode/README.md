LEGO
Author: Anakin

Brunnerne Inc.™ has recently completed a major modernization initiative by replacing several aging industrial control systems with the new Brunnerne Modular Automation Platform™. Due to budget optimization, the platform appears to be built from LEGO MINDSTORMS EV3 hardware.

One of the units has entered lockdown-mode after an employee failed the mandatory quarterly access-code rotation procedure. Unfortunately, the employee responsible has since been "strategically offboarded" and nobody documented the new code.

The IT-department says they have a log of all access codes added to devices, but only its MD5-hash is stored here:

 UNITID | DATE       | CODE                            
  (...)
 788    | 2026-08-21 | c92e0ceceda7927384359ccacbe5a94c
More importantly, IT has dumped and recovered the program currently running on the controller. Management expects you to find the code and restore access before the end of the business day.

Flag format: brunner{<guid-access-code>}.
Example: brunner{deadb33f-b4b3-f33d-deaf-c0ffee5e11e2}.

You can verify the access code offline like this (without brunner{}):

echo -n "<INSERT CODE HERE>" | md5sum
The real access code should match the MD5-hash from the log: c92e0ceceda7927384359ccacbe5a94c.
