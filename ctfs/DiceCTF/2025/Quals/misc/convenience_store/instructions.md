This is an Android challenge. You must develop and build a signed APK and upload it to the provided site.

For each submission, the server will evaluate the submission as follows:

- A fresh Android emulator with a stock Google API 35 image is started.
  - The emulator has no Internet access. It only has access to the internal network where the webapp is hosted.
- A fresh instance of the web app is deployed at `http://10.2.2.2:8000/`, with a single account "admin" and a random password.
  - For local testing, you may run the web app using the provided docker-compose, and then access the webapp from the emulator using the IP of your host machine.
- We run an automated script to launch Google Chrome, pointing to `http://10.2.2.2:8000/` and login to admin with the random password.
- The APK you submitted is installed into the emulator.
- We launch your APK with the command `am start -n com.dicectf2025quals.attackerapp/com.dicectf2025quals.attackerapp.MainActivity`. **Make sure your package name and activity name match those**.
- We wait for 60 seconds to allow your app to run.
- We run `logcat -d dicectf:V *:S` and provide you with the result. You may download the output in the "status" tab of the submission site.

Note: As provided in the web app's source code, the content of the flag is in the admin's note. The real flag is different, but static across submissions.

Note: The evaluation process is similar to a heavy-weight integration test. Although we've tried very hard to make the test reliable, it's possible it can still report an error occasionally. If you encounter "Infra failure", please try submitting it again. If it still fails, please let us know :)

- orion / hpmv