burturt with KQL help from bliutech

One of our professors thought it was a BRILLIANT idea to have their student project submission portal exposed to the internet, requiring only the student's ID to submit projects or retrieve them.

We suspect a malicious actor has stolen some of our student's submissions. We need to know which students' submissions were compromised (downloaded by a malicious actor) ASAP. Unfortunately, the only logs we have are proxy logs, and the professor refuses to give us the code or access to their web app (they claim they just immediately deleted the app's code once they realized they were hacked...).

The team at Microsoft has generously provided everyone with a free log analysis cluster, no credit card needed! Go to the link, create your cluster, then copy and open the "Cluster URI" in your browser. You will be brought to a page you can then use to query the data!

You can easily get started with analyzing the logs by running these commands:

.execute database script <
.drop table WebLogs ifexists
.create table WebLogs (
    IP: string,
    Timestamp: datetime,
    Method: string,
    Endpoint: string,
    HttpVersion: string,
    Status: long,
    UserAgent: string
)

To make sure it worked, sample 10 logs:

WebLogs
 limit 10

Notes:

    The network here at UCLA rotates IP addresses of students fairly often, and many people use shared computers, such as at the CPO Lab. Unfortunately, this means it's hard to know whether 2 requests from the same IP are the same person, or 2 different people, even if the user agent is the same.
    We've narrowed down the attack to a 3 hour window, which is (roughly) what the logs provided contains.
    Note that TAs also downloaded submissions - do not consider their downloads as "leaks"!
    Submission IDs are sequentially assigned to submissions as they submit, starting from the first submission in the log as ID 1, and are globally unique. You can assume there are no other submissions outside of the provided log.
    We suspect the number of compromised accounts is between 100 and 1000, counting the number of unique students IDs that had their submissions downloaded by the malicious actor, even if a student submitted multiple times.
    If you are 100% certain your answer is correct, and you've read all of the notes, but the submission is not taking your answer, feel free to open a support ticket, but make sure to provide the KQL query(s) you are using to get your answer.
