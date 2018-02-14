/*Start at 1*/
INSERT INTO user (username, email, pw_hash)
VALUES ('bobjUmbo', 'bobjumbo@gmail.com', '1234');

/*2*/
INSERT INTO user (username, email, pw_hash)
VALUES ('jeffdillon', 'jeffdillon@gmail.com', '3421');

/*3*/
INSERT INTO user (username, email, pw_hash)
VALUES ('xgen', 'xgen@gmail.com', '2845');

INSERT INTO user (username, email, pw_hash)
VALUES ('obj123', 'obj123@gmail.com', '3957');

INSERT INTO user (username, email, pw_hash)
VALUES ('xj9', 'nani@gmail.com', '9845');

INSERT INTO user (username, email, pw_hash)
VALUES ('salion', 'salion@gmail.com', '1983');

INSERT INTO user (username, email, pw_hash)
VALUES ('jesse', 'walter@gmail.com', '2845');

INSERT INTO follower (who_id, whom_id)
VALUES (1, 2);

INSERT INTO follower (who_id, whom_id)
VALUES (1, 7);

INSERT INTO follower (who_id, whom_id)
VALUES (1, 4);

INSERT INTO message(author_id, text, pub_date)
VALUES (7, 'Hello my name walter white', 10231996);

INSERT INTO message(author_id, text, pub_date)
VALUES (1, 'I have many followers', 10231996);
