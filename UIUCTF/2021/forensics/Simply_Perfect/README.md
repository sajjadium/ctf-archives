You snuck into the building. You logged into the mainframe and checked a few things out. Time ran out, but you gave yourself remote access before you got out. After connecting again, you're able to survey the box more and add a collection script before you're disconnected. Later on, you realize your typical remote access is no longer available. Suspecting you've been detected, you connect with a different access and remove your collection script.

Remove any entries in the log that you are responsible for creating. The flag is the MD5 hash of the clean log file with your entries removed. Remember, you simply need to be perfect. In other words, it is the entries you created directly or very closely related entries the system created because of your activity at the time of your interaction. Do not clean entries that clearly would have existed without your activity. The clean log file is what you would use to replace the dirty log file with if you connected again and only wanted to remove your entries from your past activity. You are only removing entries, not creating or modifying any entries.

The number of bytes of the clean log is 4,618,880 bytes, which should tell you exactly how many entries need to be cleaned. If your clean log file is smaller, you cleaned too much; if it's is bigger, you have not cleaned enough; if it's the same size, you have not cleaned the right entries.

If you believe you have removed all of the right entries (your log file size is the same or very close) and your flag is not working, contact mod mail, but be prepared with a list of entries you have removed and an explanation of why you removed the entries you did or didn't remove certain entries you weren't sure about.

The flag format is: uiuctf{md5_hash_of_clean_log_here}
