## Member

Every user that interacts with the carpooling platform needs to be an authenticated user, therefore the system has to
store his information on the database.
For This reason, we create the `Member` table which will store the name, email and phone number of the user.

## City/Point Of Interest/Stops

When a user wants to publish a trip, he needs to choose an origin and a destination, ideally from a drop-down,
which means that those locations must be stored in our database.
By creating a `city` table we have a list of cities to choose from, which will store the name of the city (`city_name`),
the `region` and `country`. 
Additionally the user could also choose his starting location/destination from a list of known places, which we will 
store in the `point_of_interest` table, which in turn would store the `name`, `address`, and references the city table.

A trip could also have multiple stops, those stops could be:
- An origin/destination.
- A chosen stop in a city.
- A point of interest.

A table `Stops` stores these details:
- `stop_id`: PK of the stop
- `city_id`: FK of the city
- `point_of_interest_id`: FK of the point of interest
- `address`: Address of the stop if it is not a point of interest
- `is_origin`: 1 if the stop is the starting point else 0
- `is_destination`: 1 if the stop is the destination else 0
- `is_point_of_interest`: 1 if the stop is a point of interest else 0

