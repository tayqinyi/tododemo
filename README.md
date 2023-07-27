# ToDoDemo

## Start api server
docker-compose up --build

## Authentication with header
### Authentication with google
--header 'google-token:<google token>'
### Authentication with facebook
--header 'facebook-token:<facebook token>'
### Authentication with github
--header 'github-token:<github token>'

## Create ToDo
```commandline
curl --location 'http://127.0.0.1:8000/api/todo' --header 'facebook-token: <token>' --header 'Content-Type: application/json' --data '{
    "title": "test todo 2",
    "description": "This is a test todo"
}'
```

## Get ToDos
```commandline
curl --location 'http://127.0.0.1:8000/api/todo' --header 'facebook-token: <token>'
```

## Delete ToDos
```commandline
curl --location --request DELETE 'http://127.0.0.1:8000/api/todo/1' --header 'facebook-token: <token>'
```

## Mark complete ToDos
```commandline
curl --location --request POST 'http://127.0.0.1:8000/api/todo/mark_complete/1' --header 'facebook-token: <token>'
```

## Developer
### Run unittest
```commandline
python manage.py test
```

## Note
- No proper email capturing in authentication (that should be the unique identifier for user)
