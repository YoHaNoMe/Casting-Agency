# Capstone Full Stack API

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
3. Create Database called `capstone_test`. By `createdb capstone_test`
**Note:** You don't need The last step if you are not going to test the application.
If you have any trouble creating the database, please refer to this [Article](https://www.enterprisedb.com/postgres-tutorials/how-create-postgresql-database-and-users-using-psql-and-pgadmin)

## Running the server
First **ensure** you are working using your created virtual environment.
Also If you want to **Disable** Authentication change the `AUTH_STATUS` in `.env` file from 1 to 0.

To run the server, execute:

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
      "name": "User 1"
    },
    {
      "age": 50,
      "gender": "male",
      "id": 5,
      "name": "User 2"
    },
    {
      "age": 50,
      "gender": "male",
      "id": 6,
      "name": "User 3"
    },
    {
      "age": 40,
      "gender": "female",
      "id": 7,
      "name": "User 4"
    },
    {
      "age": 40,
      "gender": "female",
      "id": 8,
      "name": "User 5"
    },
    {
      "age": 40,
      "gender": "female",
      "id": 9,
      "name": "User 6"
    }
  ],
  "status_code": 200,
  "success": true,
  "total_actors": 6
}
```
## POST /actors
- Create new Actor
- In the request *Body* You have to specify:
```
{
    "name": "The name of the user",
    "age": 40,
    "gender": "the gender of the user (male / female)"
}
```

- If you miss any of the (name, age, gender) you will get **Bad Request**
- If you miss any type of the (name, age, gender) you will get **Bad Request**
- Example: ``` curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "age": 50, "gender": "male"}' http://127.0.0.1:5000/actors ```

## UPDATE /actors/id
- Update an existing actor
- In the request *Body* You have to specify at **least** on of the following:
```
{
    "name": "The updated name of the user",
    "age": 40,
    "gender": "the updated gender of the user (male / female)"
}
```
- If you didn't specify any of the fields you will get **Bad Request**
- Example: ``` curl -X PATCH -H "Content-Type: application/json" -d '{"name": "John Doe", "age": 50, "gender": "male"}' http://127.0.0.1:5000/actors/1 ```

## DELETE /actors/id
- Delete an existing actor
- If the actor doesn't exist you will get **Not Found Request**
- Example: `curl -X DELETE http://127.0.0.1:5000/actors/1`

## GET /movies
- Get all movies

```
{
  "movies": [
    {
      "id": 1,
      "release_date": "04/07/2015",
      "title": "Test 1"
    },
    {
      "id": 4,
      "release_date": "12/02/2017",
      "title": "Test 2"
    },
    {
      "id": 7,
      "release_date": "30/08/2018",
      "title": "Test 3"
    },
    {
      "id": 8,
      "release_date": "12/07/2019",
      "title": "Test 4"
    },
    {
      "id": 9,
      "release_date": "12/07/2019",
      "title": "Test 5"
    },
    {
      "id": 11,
      "release_date": "12/07/2019",
      "title": "Test 6"
    }
  ],
  "status_code": 200,
  "success": true,
  "total_movies": 6
}
```

## POST /movies
- Create new Movie
- In the request *Body* You have to specify:
```
{
    "title": "The name of the movie",
    "release_date": "12/2/2019"
}
```

- If you miss any of the (title, release_date) you will get **Bad Request**
- If you miss any type of the (title, release_date) you will get **Bad Request**
- If you write wrong date you will get **Bad Request**
- Example: ``` curl -X POST -H "Content-Type: application/json" -d '{"title": "Fast & Furious", "release_date": "12/2/2019"}' http://127.0.0.1:5000/movies ```

## UPDATE /movies/id
- Update an existing movie
- In the request *Body* You have to specify at **least** on of the following:
```
{
    "title": "The updated name of the title",
    "release_date": "12/2/2019"
}
```
- If you didn't specify any of the fields you will get **Bad Request**
- Example: ``` curl -X PATCH -H "Content-Type: application/json" -d '{"title": "Fast & Furious 7", "release_date": "12/2/2019"}' http://127.0.0.1:5000/movies/1 ```

## DELETE /actors/id
- Delete an existing movie
- If the movie doesn't exist you will get **Not Found Request**
- Example: `curl -X DELETE http://127.0.0.1:5000/movies/1`


## Error Handling
```
{
  "message": "The error message",
  "status_code": status_code,
  "success": false
}
```
- 400: Bad Request
- 404: Not Found
- 422: Not Processable
- 401: Not Authorized


## Testing
To run the tests, run
```
python3 test_flaskr.py
```
