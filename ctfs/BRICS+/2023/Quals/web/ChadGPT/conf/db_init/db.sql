CREATE OR REPLACE TABLE replies
(
    id     INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    prompt VARCHAR(1000),
    reply  VARCHAR(10000)
);
CREATE OR REPLACE TABLE flags
(
    flag VARCHAR(100) PRIMARY KEY
);

INSERT INTO replies (prompt, reply)
VALUES ('What is your name?', 'My name is Chad GPT. Im a chatbot that was trained on the internet data.'),
       ('How to find a girlfriend ?',
        'To find a girlfriend, you need to be confident, respectful, and kind. You need to learn how to socialize, know what to say and be yourself. You need to approach girls that you like, make your intentions clear and start talking to them. Don''t be afraid of rejection, it happens to the best of us! You can always try again. Good luck, King!'),
       ('How to become like you ?',
        'To become like me, you need to focus on your goals and make them your number one priority. You need to be disciplined and consistent. You also need to surround yourself with people who will motivate you and encourage you to push through. Finally, you need to believe in yourself and have a positive attitude, as anything is possible! Good luck, brother!'),
       ('How to become a hacker',
        'If you want to become a hacker you need to start by learning about technology and computer programming. You need to develop your coding skills, understand the fundamentals of network communication and become familiar with the latest security exploits and vulnerabilities.');

INSERT
INTO flags (flag)
VALUES ('brics+{fake}');

GRANT SELECT ON *.* TO 'app'@'%';
FLUSH PRIVILEGES;
-- GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'; FLUSH PRIVILEGES;