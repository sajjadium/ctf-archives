USE ctf;

CREATE TABLE User
(
  User_ID SERIAL NOT NULL,
  Email VARCHAR(128) NOT NULL,
  Username VARCHAR(128) NOT NULL,
  Password VARCHAR(128) NOT NULL,
  Blocked INT NOT NULL,
  Bitcoin_Wallet VARCHAR(256) NOT NULL,
  PRIMARY KEY (User_ID),
  UNIQUE (Email),
  UNIQUE (Username)
);

CREATE TABLE Interface
(
  Interface_ID SERIAL NOT NULL,
  User_ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Interface_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Support_Tickets
(
  Ticket_ID SERIAL NOT NULL,
  Description VARCHAR(2048) NOT NULL,
  Messages VARCHAR(2048) NOT NULL,
  Time_stamp VARCHAR(256) NOT NULL,
  User_ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Ticket_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Support_Staff
(
  Staff_ID SERIAL NOT NULL,
  Developer INT,
  User_ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Staff_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Affiliates
(
  Affiliate_ID SERIAL NOT NULL,
  Total_bots_added INT NOT NULL,
  Money_received FLOAT NOT NULL,
  User_ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Affiliate_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Botnet_Order
(
  Number_of_bots INT NOT NULL,
  Order_ID SERIAL NOT NULL,
  Time_of_use FLOAT NOT NULL,
  Price FLOAT NOT NULL,
  Approved INT,
  Time_stamp VARCHAR(256) NOT NULL,
  User_ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Order_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Manages
(
  Staff_ID BIGINT UNSIGNED NOT NULL,
  Ticket_ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Staff_ID, Ticket_ID),
  FOREIGN KEY (Staff_ID) REFERENCES Support_Staff(Staff_ID),
  FOREIGN KEY (Ticket_ID) REFERENCES Support_Tickets(Ticket_ID)
);

CREATE TABLE Bots
(
  Bot_ID SERIAL NOT NULL,
  OS VARCHAR(32) NOT NULL,
  IP_Address VARCHAR(15) NOT NULL,
  Interface_ID BIGINT UNSIGNED,
  PRIMARY KEY (Bot_ID),
  FOREIGN KEY (Interface_ID) REFERENCES Interface(Interface_ID),
  UNIQUE (IP_Address)
);

CREATE TABLE Adds
(
  Bot_ID BIGINT UNSIGNED NOT NULL,
  Affiliate_ID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (Bot_ID, Affiliate_ID),
  FOREIGN KEY (Bot_ID) REFERENCES Bots(Bot_ID),
  FOREIGN KEY (Affiliate_ID) REFERENCES Affiliates(Affiliate_ID)
);

CREATE VIEW User_Bots AS SELECT B.Bot_ID, B.OS, B.IP_Address, U.User_ID FROM Bots B JOIN Interface I ON B.Interface_ID = I.Interface_ID JOIN User U ON I.User_ID = U.User_ID;

CREATE VIEW Staff_Tickets AS SELECT ST.Ticket_ID, ST.Description, ST.Messages, ST.Time_stamp, ST.User_ID FROM Support_Tickets ST JOIN Manages M ON ST.Ticket_ID = M.Ticket_ID;