## Django server for Engineering Thesis

### Steps to run app in developer mode

First you need to configure .env file. Example .env-example is included. <br>
<br>
In folder with docker-compose.yml run the following commands: <br>
`docker-compose build` to install all requirements <br>
`docker-compose up` to run local server ("localhost:8000/") <br>
optional: `docker-compose run web python manage.py createsuperuser` for admin user creation <br>

### Available endpoints

**User accounts management:** <br>
`/api/auth/users/` user list and create view <br>
`/api/auth/users/me/` currently logged-in user's detail <br>
`/api/auth/users/<id>/` chosen user detail <br>
`/api/auth/jwt/create/` create jwt token for user login <br>
`api/auth/jwt/refresh/` refresh jwt token <br>
`api/auth/jwt/verify/` verify jwt token <br>

**Devices management:** <br>
User can see only his building and it's parts (rooms, scenes, devices etc) <br>
`/api/buildings/` all user's buildings list view {GET} <br>
`/api/buildings/<id>/` selected building detail view (with building's rooms and scenes) {GET} <br>
`/api/rooms/` all user's building's rooms list view {GET} <br>
`/api/rooms/<id>/` selected room detail view (with room's devices and measuring devices) {GET} <br>
`/api/scenes/` all user's building's scenes list view {GET, POST, DELETE} <br>
`/api/scenes/<id>/` selected scene detail view (with scene's devices) {GET, PATCH} <br>
`/api/devices/` all user's building's devices list view {GET, POST} <br>
`/api/devices/<id>/` selected device detail view {GET, PATCH} <br>
`/api/measuring-devices/` all user's building's measuring devices list view {GET} <br>
`/api/daily-measurements/<id>` selected daily measurement's detail {GET} <br>
`/api/measurements/` all user's building's measureements {GET} <br>
`/api/measurements/<id>` selected measurement's detail {GET} <br>
`/api/daily-measurements/` all user's building's daily measurements {GET, POST} <br>
`/api/measuring-devices/<id>/`selected measuring device detail view {GET} <br>
`/api/measuring-devices/<id>/measurements/`selected measuring device measurements {GET} <br>
`/api/measuring-devices/<id>/daily-measurements/`selected measuring device daily measurements {GET} <br>
<br>

**Graphql endpoint:**<br>
The graphql endpoint is also available.<br>
`/graphql/` accessible queries are analogous to devices endpoints <br>

### How can you add to database

**Using django-admin:**<br>
`docker-compose run web python manage.py createsuperuser` for admin-user creating <br>
`/admin/` - endpoint for nice django interface for easy creating new buildings and stuff <br>
