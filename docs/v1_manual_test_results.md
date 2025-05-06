# Chess Site Edutainer Showcase Posting Flow
Levy Rozman from GothamChess just had an incredibly close game on his climb to GM and he wants to share his game with the world and use his game as an example of crucial endgame theory. 

First, Levy will log his game into his history using POST ```/user/games/{user_id}/submit```. He will then be able to find this most recent game in his history when he calls GET```/user/games/{user_id}```. From here, he can create a showcase based on this great game, and post it using POST```/showcases/post```. 

But whoops, Levy accidentally posted the showcase without any captions. Luckily, instead of deleting the showcase and posting a new one about the same game, Levy opts to just edit the newly posted one, hoping no one's feed has already received it, with PUT```/showcases/edit/{showcase_id}```. Now, Levy has finished sharing his game with the world!


# Testing Results

### ```/user/games/{user_id}/submit```
1. The curl statement:
    ~~~
    curl -X 'POST' \
        'https://three65-group-project.onrender.com/user/games/1/submit' \
        -H 'accept: */*' \
        -H 'access_token: cbf5378e064ebeeacea64ee666f64d7d' \
        -H 'Content-Type: application/json' \
        -d '{
        "color": "white",
        "game_status": "win",
        "time_control": "classical",
        "opponent_id": 2,
        "time_in_ms": 10000
        }'
    ~~~
2. Response:
    ~~~
    {
        "success": True
    }
    ~~~

### ```/user/games/{user_id}```
1. The curl statement:
    ~~~
    curl -X 'GET' \
        'https://three65-group-project.onrender.com/user/games/1' \
        -H 'accept: application/json' \
        -H 'access_token: cbf5378e064ebeeacea64ee666f64d7d'
    ~~~
2. Response:
    ~~~
    [
        {
            "black": 2,
            "white": 1,
            "winner": "white",
            "time_control": "classical",
            "duration_in_ms": 10000
        }
    ]
    ~~~

### ```/showcases/post```
1. The curl statement:
    ~~~
    curl -X 'POST' \
        'https://three65-group-project.onrender.com/showcases/post' \
        -H 'accept: */*' \
        -H 'access_token: cbf5378e064ebeeacea64ee666f64d7d' \
        -H 'Content-Type: application/json' \
        -d '{
        "user_id": "1",
        "title": "My First Post",
        "game_id": 1,
        "caption": "Get pwned lol"
        }'
    ~~~
2. Response:
    ~~~
    {
        "success": True
    }
    ~~~

### ```/showcases/edit/{showcase_id}```
1. The curl statement:
    ~~~
    curl -X 'POST' \
        'https://three65-group-project.onrender.com/showcases/edit/1' \
        -H 'accept: */*' \
        -H 'access_token: cbf5378e064ebeeacea64ee666f64d7d' \
        -H 'Content-Type: application/json' \
        -d '{
        "title": "",
        "caption": "mb lol"
        }'
    ~~~
2. Response:
    ~~~
    {
        "success": True
    }
    ~~~