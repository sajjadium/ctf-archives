icesfont

Even the admin bot forgets things sometimes, which is why they wrote a memo and forgot about it. Can you jog their memory?

NB: The admin bot on remote does not match the bot.js given in the old distribution exactly.

In particular, the remote admin bot is running on an old version: HeadlessChrome/107.0.5296.0, whereas the intended solution works on latest.

This means that there exist unintended solutions that abuse bugs in this older version of Chromium.

A revenge challenge will be released later with the admin bot as part of the challenge itself (rather than relying on the redpwn bot) and with Chromium up-to-date.

For now, the distribution has been updated to match remote in order to aid local testing; http://localhost:3000/srcdoc-memos provides the same (outdated) admin bot used on remote.
