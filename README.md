## Django server for Engineering Thesis

### Steps to run app in developer mode

First you need to configure .env file. Example .env-example is included. <br>
<br>
In folder with docker-compose.yml run the following commands: <br>
`docker-compose build` to install all requirements <br>
`docker-compose up` to run local server ("localhost:8000/") <br>

### Available endpoints

**User accounts management:** 
`/api/auth/users/` user list and create view <br>
`/api/auth/users/me/` currently logged-in user's detail <br>
`/api/auth/users/<id>/` chosen user detail <br>
`/api/auth/jwt/create/` create jwt token for user login <br>
`api/auth/jwt/refresh/` refresh jwt token <br>
`api/auth/jwt/verify/` verify jwt token <br>



