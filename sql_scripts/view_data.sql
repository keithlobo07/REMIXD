USE `remixd`;

SELECT * FROM Account;
SELECT * FROM Review;
SELECT IF(info & 128 = 128, True, False) FROM Tags;
SELECT Account.ID, Account.Name, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE AlbumID=2130752 ORDER BY Review.timestamp DESC LIMIT 3;