USE `remixd`;

INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (1, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", 10, True, 'still only like the third best kendrick lamar album lol');
INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (2, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", 1, False, 'i hate this album and also all good music');
INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (3, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", 5, False, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nisi risus, facilisis vel purus id, feugiat consequat metus. Integer eu lorem eu metus congue placerat sed eget tortor.');
INSERT INTO Review (AccountID, AlbumID, Score, Liked, Content) VALUES (4, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", 8, True, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nisi risus, facilisis vel purus id, feugiat consequat metus. Integer eu lorem eu metus congue placerat sed eget tortor.');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (1, 1, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", b'10000000');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (4, 1, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", b'10000000');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (1, 2, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", b'01000000');
INSERT INTO Tags (AccountID, ReviewAccountID, ReviewAlbumID, info) VALUES (1, 3, "11755c21-2546-4cb3-9b87-392f4f3c2fa2", b'10000000');