DROP TABLE IF EXISTS ctfers;
CREATE TABLE IF NOT EXISTS ctfers (
    id TEXT PRIMARY KEY,
    name TEXT,
    image TEXT,
    team TEXT,
    specialty TEXT,
    website TEXT,
    description TEXT,
    searchable BOOLEAN
);
INSERT INTO ctfers (id, name, image, team, specialty, website, description, searchable) VALUES ('4a24b0971bf4d7537a53d6d5ae2a463f', 'Vie', 'https://avatars.githubusercontent.com/u/23710699?v=4', 'Maple Bacon', 'web', 'https://jamvie.net/', 'Vie is the former leader of Maple Bacon & an Information Security Engineer at Google! She does a lot of cool web hacking and makes really cool anime art!', TRUE);
INSERT INTO ctfers (id, name, image, team, specialty, website, description, searchable) VALUES ('a290ce7aae07973593f767249037339e', 'Strellic', 'https://avatars.githubusercontent.com/u/16631579?v=4', 'DiceGang', 'web', 'https://brycec.me/', 'Strellic is a really cool web hacker who works for ElectronVolt & Cure53!', TRUE);
INSERT INTO ctfers (id, name, image, team, specialty, website, description, searchable) VALUES ('c8f020d57b9ff2f7275884bf6fa0d2d6', 'Masato', 'https://avatars.githubusercontent.com/u/1499192?v=4', 'Cure53', 'web', 'https://mksben.l0.cm/', 'Masato is an prolific web security researcher who is notable for some amazing accomplishments such as find an [XSS in Google Search](https://youtu.be/lG7U3fuNw3A?si=_vvYPZwyR3nJ9p-Z) and working on [DOMPurify](https://github.com/cure53/DOMPurify).', TRUE);
INSERT INTO ctfers (id, name, image, team, specialty, website, description, searchable) VALUES ('fd07882a12b7605e64bdd561304ec983', 'Aplet123', 'https://avatars.githubusercontent.com/u/16807306?v=4', 'PBR | UCLA, DiceGang', 'moral support', 'https://aplet.me', 'Aplet123 is an experienced CTFer who has helped put together many CTFs ranging from AngstromCTF, DiceCTF, and most notably, LA CTF! **Cool CTFs:** [https://lac.tf](https://lac.tf)', TRUE);
INSERT INTO ctfers (id, name, image, team, specialty, website, description, searchable) VALUES ('4da793e35353bb844e073fc7bade512f', 'kaiphait', 'https://pbr.acmcyber.com/assets/images/members/kaiphait.webp', 'PBR | UCLA', './aplet123', 'https://www.alexyzhang.dev/', 'kaiphait is a pwner for PBR | UCLA. He specializes in making fun of Aplet123 and enjoys playing [SuperTuxKart](https://supertuxkart.net/Main_Page) in his spare time. **Cool Writeups:** [CSAW CTF 2023 Finals – brainflop](https://www.alexyzhang.dev/write-ups/csaw-finals-2023/brainflop/), [ångstromCTF 2023 – noleek](https://www.alexyzhang.dev/write-ups/angstromctf-2023/noleek/), [LA CTF 2023 – pwn/stuff](https://www.alexyzhang.dev/write-ups/lactf-2023/stuff/)', TRUE);
INSERT INTO ctfers (id, name, image, team, specialty, website, description, searchable) VALUES ('8d6a9c655a13d9e540796e4a526a2a46', 'defund', 'https://avatars.githubusercontent.com/u/14859625?v=4', 'DiceGang', 'crypto', 'https://priv.pub/', 'defund is a really cool crypto CTFer who is currently working on his PhD at NYU in Cryptography! He is also an alumni of ACM Cyber at UCLA.', TRUE);