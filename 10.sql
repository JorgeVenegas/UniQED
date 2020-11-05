SELECT name FROM people WHERE id IN
(SELECT DISTINCT people.id FROM people
JOIN directors ON people.id=directors.person_id
JOIN movies ON movies.id=directors.movie_id
JOIN ratings ON movies.id=ratings.movie_id
WHERE ratings.rating >= 9);