SELECT title
FROM
    (
        SELECT title, id
        FROM movies
        WHERE id IN
        (
            SELECT movie_id
            FROM stars
            WHERE person_id =
            (
                SELECT id
                FROM people
                WHERE name = "Johnny Depp"
            )
        )
    )
    WHERE id IN
        (
            SELECT movie_id
            FROM stars
            WHERE person_id =
            (
                SELECT id
                FROM people
                WHERE name = "Helena Bonham Carter"
            )
        );