# Community Member Search and Sharing Showcase Flow
Eager chess student Charlie Brown was talking to his friend Beth Harmon about the London System chess opening. Charlie Brown recounts finding a really funny but impractical response to the opening earlier while scrolling through his feed. 

Wanting to share this showcase to Beth, he searches for the showcase with GET```/showcases/search``` hoping that the title had the phrase 'london system'. Fortunately, a result is returned, and Charlie sends a link to Beth. Together, they both examine the game further through GET```/games/{game_id}```, and share a laugh as they bond over the failed creative attempt to triumph over the London System. Charlie Brown returns to the original post, and leaves a positive comment with POST```/showcases/comment``` humoring the snippet, before they both resume scrolling.

## Testing Results

### ```/games/{game_id}```
1. The curl statement:
    ~~~
    curl -X 'GET' \
        'http://127.0.0.1:3000/games/1' \
        -H 'accept: application/json' \
        -H 'access_token: brat'
    ~~~
2. Response:
    ~~~
    {
        "black_player_id": 1,
        "white_player_id": 2
    }
    ~~~

### ```/showcases/comment```
1. The curl statement:
    ~~~
    curl -X 'POST' \
        'http://127.0.0.1:3000/showcases/1/comment' \
        -H 'accept: */*' \
        -H 'access_token: brat' \
        -H 'Content-Type: application/json' \
        -d '{
        "post_id": 1,
        "auther_uid": 1,
        "date_posted": "2025-05-13T10:58:20.317Z",
        "comment_string": "hello darkness my old friend..."
        }'
    ~~~
2. Response:
    ~~~
    {
        "success": true
    }
    ~~~

# Reporting Obviously Fake Account Flow
Upstanding community member Sherlock Holmes was scrolling through his feed one day and found a very interesting showcase posted by Cat Branchman. It was a very impressive sequence that was featured, but Holmes noticed something strange. 

Holmes uses the showcase to find the original game using GET```/games/{game_id}``` and examines the moves played by both players, which are rated only around 1200 Elo. Holmes being a professional player himself, noticed that the original showcase poster played suspiciously well for someone with his rating, and investigates further finding his games history with GET```/user/games/{user_id}```. After checking out Cat Branchman's recent win rate, Holmes also checks out Branchman's showcase history to confirm a suspicion using GET```user/showcases/{user_id}```, and, as expected all of these suspicious games were also used for showcases. 

So, Holmes files a report against the account and a few of the showcases by calling POST```/reports/post```. Moreover, Holmes posts comments via POST```/showcases/comment```on a few of Branchman's latest posts urging other people to follow in his footsteps. After a few days, the account and its showcases were all removed from the platform.

## Testing Results

### ```/games/{game_id}```
1. The curl statement:
    ~~~
    curl -X 'GET' \
        'http://127.0.0.1:3000/games/1' \
        -H 'accept: application/json' \
        -H 'access_token: brat'
    ~~~
2. Response:
    ~~~
    {
        "black_player_id": 1,
        "white_player_id": 2
    }
    ~~~

### ```/user/games/{user_id}```
1. The curl statement:
    ~~~
    curl -X 'GET' \
        'http://127.0.0.1:3000/user/games/1' \
        -H 'accept: application/json' \
        -H 'access_token: brat'
    ~~~
2. Response:
    ~~~
    [
        {
            "black": 2,
            "white": 1,
            "winner": "white",
            "time_control": "classical",
            "duration_in_ms": 1100
        },
        {
            "black": 2,
            "white": 1,
            "winner": "white",
            "time_control": "classical",
            "duration_in_ms": 12
        },
        {
            "black": 2,
            "white": 1,
            "winner": "white",
            "time_control": "classical",
            "duration_in_ms": 0
        },
        {
            "black": 1,
            "white": 2,
            "winner": "white",
            "time_control": "classical",
            "duration_in_ms": 10
        }
    ]
    ~~~

### ```/user/showcases/{user_id}```
1. The curl statement:
    ~~~
    curl -X 'GET' \
        'http://127.0.0.1:3000/user/showcases/1' \
        -H 'accept: application/json' \
        -H 'access_token: brat'
    ~~~
2. Response:
    ~~~
    [
        {
            "created_by": 1,
            "title": "boowerqe",
            "views": 0,
            "caption": "rwerewr",
            "date_created": "2025-05-06",
            "game_id": 1
        }
    ]
    ~~~

### ```/reports/post```
1. The curl statement:
    ~~~
    curl -X 'POST' \
        'http://127.0.0.1:3000/reports/post' \
        -H 'accept: */*' \
        -H 'access_token: brat' \
        -H 'Content-Type: application/json' \
        -d '{
        "user_id": 1,
        "showcase_id": 1,
        "report_brief": "inappropriate content",
        "report_details": "did not need to see hans ziemaan speculative xray sketch"
        }'
    ~~~
2. Response:
    ~~~
    {
        "success": true,
    }
    ~~~


### ```/showcases/comment```
1. The curl statement:
    ~~~
    curl -X 'POST' \
        'http://127.0.0.1:3000/showcases/1/comment' \
        -H 'accept: */*' \
        -H 'access_token: brat' \
        -H 'Content-Type: application/json' \
        -d '{
        "post_id": 1,
        "auther_uid": 1,
        "date_posted": "2025-05-13T10:58:20.317Z",
        "comment_string": "hello darkness my old friend..."
        }'
    ~~~
2. Response:
    ~~~
    {
        "success": true
    }
    ~~~

