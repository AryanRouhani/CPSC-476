/* who is following whom*/
INSERT INTO user (username, email, pw_hash)
VALUES ('shirley', 's@gmail.com', '12345');

INSERT INTO follower (who_id, whom_id)
VALUES (1, 2),
        (1, 3),
        (1, 4),
        (1, 5);

INSERT INTO message(author_id, text, pub_date)
VALUES (2, 'Hello my name walter white', 10231996),
       (2, 'Whats going on with you guys?', 11231998),
       (1, 'I have many followers', 10231996);
