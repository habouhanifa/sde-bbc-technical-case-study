-- How many trip offers have been published last month?

SELECT count(*) FROM mydb.Trip T
WHERE T.is_published = 1
AND T.date_published BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE();

-- What country had the highest number of publications last month?
WITH tmp as(
	SELECT t.trip_id, t.origin FROM mydb.Trip t
	WHERE t.is_published = 1
	AND t.date_published BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
	)
SELECT c.country, count(tmp.trip_id) as number_of_publications FROM mydb.City c
INNER JOIN mydb.Stops s ON s.city_id = c.city_id
INNER JOIN tmp ON tmp.origin = s.stop_id
GROUP BY c.country
ORDER BY number_of_publications DESC LIMIT 1;