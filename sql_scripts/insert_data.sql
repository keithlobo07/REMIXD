USE `remixd`;

INSERT INTO Account (Name, Email, Password) VALUES ('Rose', 'rose@email.com', 'password');
INSERT INTO Account (Name, Email, Password) VALUES ('Imran', 'imran@email.com', 'password');
INSERT INTO Account (Name, Email, Password) VALUES ('Bethany', 'bethany@email.com', 'password');
INSERT INTO Account (Name, Email, Password) VALUES ('Keith', 'keith@email.com', 'password');
INSERT INTO Account (Name, Email, Password) VALUES ('Femi', 'femi@email.com', 'password');
INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (1, 2130752, 10, True, 'still only like the third best kendrick lamar album lol');
INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (2, 2130752, 1, False, 'i hate this album and also all good music');
INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (3, 2130752, 5, False, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nisi risus, facilisis vel purus id, feugiat consequat metus. Integer eu lorem eu metus congue placerat sed eget tortor.');
INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (4, 2130752, 8, True, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nisi risus, facilisis vel purus id, feugiat consequat metus. Integer eu lorem eu metus congue placerat sed eget tortor.');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (3, 1, 2130752, b'10000000');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (4, 1, 2130752, b'10000000');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (1, 2, 2130752, b'01000000');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (1, 3, 2130752, b'10000000');