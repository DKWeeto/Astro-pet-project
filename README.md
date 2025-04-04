NEO (asteroids) https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY
https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY

could do previous and next close approach dates, with a dropdown menu to list all dates from up to a certain amount of years ago


PIC OF DAY (COULD BE BACKGROUND OF DASH) https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY


NOTIFICTIONS (OR MAYBE A NEWS PAGE) https://api.nasa.gov/DONKI/notifications?startDate=2014-05-01&endDate=2014-05-08&type=all&api_key=DEMO_KEY


astronomy - positions and events and star charts and moon phase

a "get tonights sky forecast" kind of deal

if it is night (can find out with weather api), then do hourly?

what bodies are in the sky? what phase is the moon in? whats the weather and visibility (not same as weather visibility bc dark == good) like?

https://docs.astronomyapi.com/endpoints/bodies/positions
maybe user can pick a location on map which translates to nearest lat/lon in database, OR a new api request is made per click - OR highlight large areas on a UK map (north eng, south eng, scot, Wales, cornwall + nth ireland, etc)

HAVE A RED MODE AND A DARK MODE
ALSO HAVE WEATHER


sky = hourly

THRESHOLD green 0
THRESHOLD yellow 50
THRESHOLD amber 100
THRESHOLD red 200

TODO:
FIND API OR ENDPOINT THAT GIVES BRIGHT STARS IN NIGHT SKY?

![ERD draft](./Screenshot%202024-05-29%20at%2023.19.05.png)

![Example star chart (red mode)](https://widgets.astronomyapi.com/star-chart/generated/5ed13e0447cb88ef6d0a4784ae1202638cf0c8bf33e9292fd519393edeb50191.png)

test
