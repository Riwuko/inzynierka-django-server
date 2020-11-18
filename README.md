## Django server for Engineering Thesis

### Steps to run app in developer mode

First you need to configure .env file. Example .env-example is included. <br>
<br>
In folder with docker-compose.yml run the following commands: <br>
`docker-compose build` to install all requirements <br>
`docker-compose up` to run local server ("localhost:8000/") <br>
`docker-compose run web python manage.py makemigrations` (in new terminal) <br>
`docker-compose run web python manage.py migrate` <br>
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
`/api/buildings/` all user's buildings list view <br>
`/api/buildings/<id>/` selected building detail view (with building's rooms and scenes) <br>
`/api/rooms/` all user's building's rooms list view <br>
`/api/rooms/<id>/` selected room detail view (with room's devices and measuring devices)<br>
`/api/scenes/` all user's building's scenes list view<br>
`/api/scenes/<id>/` selected scene detail view (with scene's devices) <br>
`/api/devices/` all user's building's devices list view <br>
`/api/devices/<id>/` selected device detail view <br>
`/api/measuring-devices/` all user's building's measuring devices list view <br>
`/api/measuring-devices/<id>/`selected measuring device detail view <br>
<br>

### How can you add to database

**Using django-admin:**<br>
`docker-compose run web python manage.py createsuperuser` for admin-user creating <br>
`/admin/` - endpoint for nice django interface for easy creating new buildings and stuff <br>
