## Django server for Engineering Thesis

### Steps to run app in developer mode

First you need to configure .env file. Example .env-example is included.

In folder with docker-compose.yml run the following commands: <br>
`docker-compose build` to install all requirements 
`docker-compose up` to run local server ("localhost:8000/") 

### Available endpoints

**User accounts management:** 
`/api/auth/users/` user list and create view 
`/api/auth/users/me/` currently logged-in user's detail
`/api/auth/users/<id>/` chosen user detail
`/api/auth/jwt/create/` create jwt token for user login
`api/auth/jwt/refresh/` refresh jwt token
`api/auth/jwt/verify/` verify jwt token 



