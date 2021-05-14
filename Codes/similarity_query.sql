SELECT *, MATCH(bagowords) AGAINST ((SELECT bagowords FROM books WHERE title = "Autobiography of a Yogi") IN NATURAL LANGUAGE MODE) AS `Score` 
FROM books Where author <> (SELECT author FROM books WHERE title = "Autobiography of a Yogi") AND title <> "Autobiography of a Yogi"
ORDER BY `Score` DESC;