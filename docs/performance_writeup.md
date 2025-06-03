# Fake Data Modeling

### Instructions

File Link: [mock_data.py](../src/test/fake_data/mock_data.py)

The file should be ran at least twice. The file is designed to attempt to insert exactly 1 million rows of data. However, some data will be duplicates, resulting in unique constraint violations. These attempts are handled by skipping them, which means that it is rare the file will ever insert the whole 1 million.

NOTE: This file make take a while to complete. The file will print "hello world" to the terminal before attempting to load data into the tables. The successful insertion into each table is accompanied by success messages in the terminal. The `users` table is filled first and takes the longest. The rest of the tables should fill significantly quicker after mocking data for `users` has concluded.

### Data Distribution
```
> users: 10% (195181)
> games: 15% (300000)
> showcases: 15% (300000)
> showcase_comments: 25% (500000)
> showcase_views: 30% (599993)
> reports: 5% (100000)
```

### Justification
As primarily a social platform and due to how we store views, we expected showcase_views to have the most amount of rows relative to everything else. While realistically, it's very likely that views take up much more than 30% of the rows, we still wanted adequate availability for the tables. By the same logic, comments also takes up a great share of row space, and these tables collectively take up more than half the expected row space. There are less comments than rows because obviously, not everyone who scrolls past a Showcase would have left a comment.

Together, games and showcases are the "meat-and-potatoes" of our data, but only take up a collective 30% of the row space. We believe this is a good middle ground of data, taking up a good chunk of our database while leaving a lot of room for the aforementioned social metrics.

Users, despite being the root prerequisite for every other row of data, only takes up 10%. Since logically, it is expected that the average user records more than 1 game and posts more than 1 showcase, it makes sense that this collection is relatively smaller than the others.

The smallest table holds reports against users. Based off assumptions of real-life data, there should be on average less than 1 report per user, while allowing room for some users to face multiple reports against them as well. Thus, we felt that around half the allocted users space is a good ball park estimate.


# Performance Results of Hitting Endpoints
```
> GET /games/{game_id} - [86 ms]
> GET /games/search - [7620 ms]
> POST /showcases/ - [32 ms]
> PUT /showcases/{showcase_id} - [60 ms]
> DELETE /showcases/{showcase_id} - [65 ms]
> GET /showcases/{showcase_id} - [68 ms]
> POST /showcases/{showcase_id}/comment - []
> GET /showcases/{showcase_id}/comments - []
> DELETE /showcases/comments/{comment_id} - []
> POST /showcases/view/{showcase_id} - []
> PUT /showcases/like/{showcase_id} - []
> GET /showcases/search - [4830 ms]
> POST /user/games/{user_id} - [23 ms]
> GET /user/games/{user_id}
> GET /user/showcases/{user_id}
> POST /user/register - [20 ms]
> GET /user/trending - 
> POST /reports/ - 
> GET /reports/ - 
> POST /admin/autowarn - 
> DELETE /admin/reset - 



```

# Performance Tuning