INSERT INTO follower (who_id, whom_id)
VALUES (1, 2),
       (2, 3),
       (1, 3),
       (3, 2),
       (2, 3),
       (1, 4),
       (4, 1);

INSERT INTO message(author_id, text, pub_date)
VALUES (2, 'Hello my name walter white', 10231996),
       (2, 'Whats going on with you guys?', 11231998),
       (1, 'I have many followers', 10231996);
