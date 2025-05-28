# 1. User Records
1. ```Get Game History```
2. ```Get Showcase History```
3. ```Submit Game```

### 1.1 Get Game History ```/user/games/{user_id}``` (GET)
Retrieves a User's previous games and basic information for each, not limited to but including: id, win/loss, time controls, and opponent.

Response:
```
[
    {
        "id": "integer",
        "game_status": "string",
        "time_control": "string"
        "opponent_username": "string",
        ...
    }
]
```


### 1.2 Get Showcase History ```/user/showcases/{user_id}``` (GET)
Retrives a User's posted showcases and basic information for each, not limited to but including: likes, dislikes, date_posted

Response:
```
[
    {
        "id":"integer",
        "likes": "integer",
        "dislikes": "integer",
        "date_posted": "date",
        ...
    }
]
```

### 1.3 Submit Game ```/user/games/{user_id}``` (POST)
Add a new game to a User's past games record.

Request:
```
{
    "game_status": "string",
    "time_control": "string",
    "opponent_username": "string",
    "date_played": "date",
    "moves_history_id": "integer",
    ...
}
```

Response:
```
{
    "new_game_id": "integer"
}
```



# 2. Game Records
1. ```Get Stats```

### 2.1 Get Stats ```/games/{game_id}``` (GET)
Retrieves stored data about a specific game

Response:
```
[
    {
    "game_status": "string",
    "time_control": "string",
    "opponent_username": "string",
    "date_played": "date",
    "moves_history_id": "integer",
    ...
    }
]
```


# 3. Showcase Records
1. ```Post Showcase```
2. ```Add Comment```
3. ```Edit Post```
4. ```Search Showcase```

### 3.1 Post Showcase ```/showcases``` (POST)
Posts a new showcase from a specific user, represented by their user id.

Request:
```
{
    "user_id": "integer",
    "title": "string",
    "date_created": "date",
    "game_id": integer,
    "caption": "string",
    ...
}
```

Response:
```
{
    "success":"boolean"
}
```

### 3.2 Add Comment ```/showcases/comment``` (POST)
Adds a new comment onto a specific post by a specific user

Request:
```
{
    "post_id": "integer",
    "author_uid": "integer",
    "date_posted": "date",
    "comment_content": "string",

}
```

Response:
```
{
    "success":"boolean"
}
```

### 3.3 Edit Showcase ```/showcases/{showcase_id}``` (PUT)
Modifies title and/or the caption of a showcase

Request:
```
{
    "title":"string",
    "caption": "string"
}
```

Response:
```
{
    "success":"boolean"
}
```


### 3.4 Search Showcase ```/showcases/search``` (GET)
Filters through showcases based on specific query parameters, and returns a list of the desired showcases.

Query Parameters:
- title
- author
- tags

Response:
```
[
    {
        "id": "integer",
        "user_id": "integer",
        "title": "string",
        "date_created": "date",
        "game_id": integer,
        "caption": "string",
        ...
    },
    ...
]
```

# 4. Report Records
1. ```Make Report```

### 4.1 Make Report ```/reports``` (POST)
Adds a report associated with a user, and optionally a showcase

Request:
```
{
    "user_id": "integer",
    "post_id": "integer",
    "report_brief": "string",
    "date_reported": "date",
    "report_details": "string",
    ...
}
```

Response:
```
{
    "success": "boolean"
}
```

# Complex Endpoints
1. `GET /user/trending`
2. `PUT /admin/autowarn`

### C.1 Top Users of the Week
Returns users with the highest total views and average views within a range of recent weeks.

Request:
```
(Query) "week_range": "integer"
```

Response:
```
[
    {
        "username": "string",
        "email": "string",
        "views": "integer",
        "likes": "integer"
    }
]
```


### C.2 Automatically Warn Users
Automatically set the status of user(s) with a certain number of reports or higher to 'Probation'

Request:
```
(Query) "tolerance": "integer"
(Query) "user_id: "integer"
```

Response:
```
{
    "affected_users": [
        "username": "string"
    ]
}
```


