# 1. User Records
1. ```Get Game History```
2. ```Get Showcase History```
3. ```Submit Game```

### 1.1 Get Game History ```/user/games/{user_id}```(POST)
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


### 1.2 Get Showcase History ```/user/showcases/{user_id}``` (POST)
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

### 1.3 Submit Game ```/user/games/{user_id}/submit```
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
    "success": "boolean"
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

### 3.1 Post Showcase ```/showcases/post```(POST)
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

### 3.2 Add Comment ```/showcases/comment/```(POST)
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

### 3.3 Edit Showcase ```/showcases/edit/{showcase_id}``` (PUT)
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


### 3.4 Search Showcase ```/showcases/search```(GET)
**Query Parameters:**
- r

**Request:**
- r

# 4. Report Records
1. ```Make Report```

### 4.1 Make Report
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
