-- How many trip offers have been published last month?

SELECT count(*) FROM Trip_Offer T
WHERE T.date_published BETWEEN DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 DAY) AND CURRENT_DATE();

-- What country had the highest number of publications last month?
SELECT c.country, count(ts.trip_offer_id) as number_of_publications FROM City c
LEFT OUTER JOIN Point_of_interest p ON p.city = c.city_id
LEFT OUTER JOIN Stops s ON (s.city_id = c.city_id OR s.point_of_interst_id = p.point_if_interst_id)
LEFT OUTER JOIN Trip_Offer_has_Stops ts ON ts.stop_id = s.stop_id
GROUP BY c.country
ORDER BY number_of_publications DESC LIMIT 1