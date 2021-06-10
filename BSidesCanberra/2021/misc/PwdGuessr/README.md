    To guess at things randomly is not to guess at all. Only through being methodical can enlightenment be achieved

Note: This challenge has a second part which is a trophy challenge. You must be the first verified team to submit PwdGuessr2 to win the trophy.

We have learned that the Demon-tron server has very particular requirements for their users' passwords.

We have also managed to learn how those passwords are checked:

def check_pwd(sample, pwd):
    for s, p in zip_longest(sample, pwd):
        if s is None or p is None:
            return False
        if p != s:
            time.sleep(0.5)  # Add a delay to stop password-guessing attacks
            return False
    return True
