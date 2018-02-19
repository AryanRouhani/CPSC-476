INSERT INTO user (username, email, pw_hash)
VALUES ('bobjUmbo', 'bobjumbo@gmail.com', '1234'),
       ('jeffdillon', 'jeffdillon@gmail.com', '3421'),
       ('xgen', 'xgen@gmail.com', '2845');


INSERT INTO follower (who_id, whom_id)
VALUES (1, 2),
       (1, 7),
       (1, 4);

INSERT INTO message(author_id, text, pub_date)
VALUES (7, 'Hello my name walter white', 10231996),
       (1, 'I have many followers', 10231996);
