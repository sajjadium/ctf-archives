Note: this challenge is the start of a series of challenges. The purpose of this CTF challenge is to bring real world phishing attachments to the challengers and attempt to find flags (previously executables or malicious domains) within the macros. This is often a process used in IR teams and becomes an extremely valuable skill. In this challenge we’ve brought to the table a malicious html file, GandCrab/Ursnif sample, and a IceID/Bokbot sample. We’ve rewritten the code to not contain malicious execution however system changes may still occur when executing, also some of the functionalities have been snipped and will likely not expose itself via dynamic analysis.

• Outlook helps, with proper licensing to access necessary features
    ◦ Otherwise oledump or similar would also help but isn’t necessary
• CyberChef is the ideal tool to use for decoding

Part 1: Start with the HTML file and let’s move our way up, open and or inspect the HTML file provide in the message file. There is only one flag in this document.

This challenge is brought to you by SRA

