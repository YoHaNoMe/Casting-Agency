# Capstone Full Stack API
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
There are three main Users who can access the Endpoints:
1. Casting Assistant
   - **get:movies**
   - **get:actors**
2. Casting Director
   - **get:movies**
   - **get:actors**
   - **add:actors**
   - **delete:actors**
   - **patch:actors**
   - **patch:movies**
3. Executive Producer
   - **get:movies**
   - **get:actors**
   - **add:actors**
   - **add:movies**
   - **delete:actors**
   - **delete:movies**
   - **patch:actors**
   - **patch:movies**

***Important Note:*** Emails and passwords for those users are sent to the Reviewer. If you want to access them, email me.

## Getting Started
***Please Note that all the below steps are for running the Application locally***. You could completely ignore all the below steps and using `https://yussefcapstoneudacity.herokuapp.com/` domain with the specified Endpoint that you want.

### Installing Dependencies

#### Python
Follow instructions to install the latest version of python for your platform in the [Python Docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [Python Docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by making sure you are in the right folder for the project. then, running:
```
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.


## Database Setup
If you want to run the app localy, please follow the instructions:
1. Make sure you have `PostgreSQL` Installed. [Download PostgreSQL](https://www.postgresql.org/download/)
2. Create Database called `capstone`. By `createdb capstone`
3. Connect to `capstone` Database and add the genders you want. For example:
```
psql -d capstone
INSERT INTO gender (gender) VALUES ('male')
INSERT INTO gender (gender) VALUES ('female')
```
4. Create Database called `capstone_test`. By `createdb capstone_test`
5. Connect to `capstone_test` Database and add the genders you want. The same as Step *3*

**Note:** You don't need The *4* and *5* steps if you are not going to test the application.
If you have any trouble creating the database, please refer to this [Article](https://www.enterprisedb.com/postgres-tutorials/how-create-postgresql-database-and-users-using-psql-and-pgadmin)

## Authentication
You have to be authenticated if you are going to use the Endpoints. By going to this [Link](https://dev-0qli2zso.auth0.com/authorize?audience=capstone&response_type=token&client_id=0oLtaAA3ksqSRMSDHfBTy9Ph0UdDuHXg&redirect_uri=https://yussefcapstoneudacity.herokuapp.com/).
If you are going to use the application locally and don't want to have Authentication, refer to the [below](https://github.com/YoHaNoMe/capstone_udacity#running-the-server) section.

## Running the server
First **ensure** you are working using your created virtual environment.
Also If you want to **Disable** Authentication change the `AUTH_STATUS` in `.env` file from 1 to 0.

1. Change the `ENV` in `.env` file from 1 to 0

2. To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Reference

### Getting Started
- Base URL: The basic URL for the application is : `http://127.0.0.1:5000/`

### GET /actors
- Get all actors
- Example: `curl http://127.0.0.1:5000/actors`

```
{
  "actors": [
    {
      "age": 50,
      "gender": "male",
      "id": 4,
      "movies": ["Movie name"],
      "name": "Actor 1"
    },
    {
      "age": 50,
      "gender": "male",
      "id": 5,
      "movies": [],
      "name": "Actor 2"
    },
  ],
  "status_code": 200,
  "success": true,
  "total_actors": 2
}
```
## POST /actors
- Create new Actor
- In the request *Body* You have to specify:
```
{
    "name": "The name of the actor",
    "age": 40,
    "gender": "the gender of the actor (male / female)"
}
```

- If you miss any of the (name, age, gender) you will get **Bad Request**
- If you miss any type of the (name, age, gender) you will get **Bad Request**
- Example: ``` curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "age": 50, "gender": "male"}' http://127.0.0.1:5000/actors ```

```
{
  "actor_id": 1,
  "status_code": 201,
  "success": true
}
```

## UPDATE /actors/id
- Update an existing actor
- In the request *Body* You have to specify at **least** on of the following:
```
{
    "name": "The updated name of the actor",
    "age": 40,
    "gender": "the updated gender of the actor (male / female)"
}
```
- If you didn't specify any of the fields you will get **Bad Request**
- Example: ``` curl -X PATCH -H "Content-Type: application/json" -d '{"name": "John Doe", "age": 50, "gender": "male"}' http://127.0.0.1:5000/actors/1 ```

```
{
  "actor": {
    "age": 40,
    "gender": "female",
    "id": 3,
    "name": "Actor 7 Updated"
  },
  "status_code": 200,
  "success": true
}
```

## DELETE /actors/id
- Delete an existing actor
- If the actor doesn't exist you will get **Not Found Request**
- Example: `curl -X DELETE http://127.0.0.1:5000/actors/1`

```
{
  "actor_id": 3,
  "status_code": 200,
  "success": true
}
```

## GET /movies
- Get all movies

```
{
  "movies": [
    {
      "id": 1,
      "release_date": "04/07/2015",
      "actors": ["Actor name1", "Actor name2", "Actor name3"],
      "title": "Test 1"
    },
    {
      "id": 4,
      "release_date": "12/02/2017",
      "actors": [],
      "title": "Test 2"
    },
  ],
  "status_code": 200,
  "success": true,
  "total_movies": 2
}
```

## POST /movies
- Create new Movie
- In the request *Body* You have to specify:
```
{
    "title": "The name of the movie",
    "release_date": "12/2/2019",
    "actors": [int]
}
```

- If you miss any of the (title, release_date, actors) you will get **Bad Request**
- If you miss any type of the (title, release_date, actors) you will get **Bad Request**
- If you write wrong date you will get **Bad Request**
- Example: ``` curl -X POST -H "Content-Type: application/json" -d '{"title": "Fast & Furious", "release_date": "12/2/2019", "actors": [1,2,3]}' http://127.0.0.1:5000/movies ```

```
{
  "movie_id": 12,
  "status_code": 201,
  "success": true
}
```

## UPDATE /movies/id
- Update an existing movie
- In the request *Body* You have to specify at **least** on of the following:
```
{
    "title": "The updated name of the title",
    "release_date": "12/2/2019",
    "actors": [int]
}
```
- If you didn't specify any of the fields you will get **Bad Request**
- Example: ``` curl -X PATCH -H "Content-Type: application/json" -d '{"title": "Fast & Furious 7", "release_date": "12/2/2019"}' http://127.0.0.1:5000/movies/1 ```

```
{
  "movie": {
    "id": 12,
    "release_date": "12/02/2019",
    "actors": [1,2]
    "title": "Movie Updated"
  },
  "status_code": 200,
  "success": true
}
```

## DELETE /movies/id
- Delete an existing movie
- If the movie doesn't exist you will get **Not Found Request**
- Example: `curl -X DELETE http://127.0.0.1:5000/movies/1`

```
{
  "movie_id": 12,
  "status_code": 200,
  "success": true
}
```

## Error Handling
```
{
  "message": "The error message",
  "status_code": status_code,
  "success": false
}
```
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Unprocessable


## Testing
To run the tests, run
```
python3 test_flaskr.py
```
