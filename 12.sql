SELECT m.title
FROM movies m JOIN (stars s1 JOIN stars s2 ON s1.movie_id=s2.movie_id)
ON s1.movie_id = m.id
where s1.person_id=(select id from people where name = "Johnny Depp")
and s2.Person_id=(select id from people where name = "Helena Bonham Carter");