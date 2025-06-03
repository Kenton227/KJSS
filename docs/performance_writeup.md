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
Slowest Endpoint: `GET /games/search`

Top 3 Slowest:

1. `GET /games/search`
2. `GET /showcases/search`
3. `GET /reports/`

All Results: (Measured using Postman)

```
> GET /games/{game_id} - [86 ms]
> GET /games/search - [5060 ms]
> POST /showcases/ - [32 ms]
> PUT /showcases/{showcase_id} - [60 ms]
> DELETE /showcases/{showcase_id} - [65 ms]
> GET /showcases/{showcase_id} - [68 ms]
> POST /showcases/{showcase_id}/comment - [35 ms]
> GET /showcases/{showcase_id}/comments - [54 ms]
> DELETE /showcases/comments/{comment_id} - [23 ms]
> POST /showcases/view/{showcase_id} - [19 ms]
> PUT /showcases/like/{showcase_id} - [17 ms]
> GET /showcases/search - [2350 ms]
> POST /user/games/{user_id} - [23 ms]
> GET /user/games/{user_id} - [114 ms]
> GET /user/showcases/{user_id} - [107 ms]
> POST /user/register - [20 ms]
> GET /user/trending - [793 ms]
> POST /reports/ - [21 ms]
> GET /reports/ - [1940 ms]
> POST /admin/autowarn - [882 ms]
> DELETE /admin/reset - [81 ms]
```

# Performance Tuning

### Initial `EXPLAIN ANALYZE` Results
Slowest Endpoint: `GET /games/search`
```
Gather Merge  (cost=18338.84..23443.69 rows=44390 width=32) (actual time=191.604..208.401 rows=74830 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  ->  Sort  (cost=17338.83..17449.81 rows=44390 width=32) (actual time=185.883..189.618 rows=37415 loops=2)
        Sort Key: g.date_played DESC
        Sort Method: quicksort  Memory: 3100kB
        Worker 0:  Sort Method: quicksort  Memory: 3139kB
        ->  Parallel Hash Join  (cost=9798.77..13912.38 rows=44390 width=32) (actual time=126.744..174.164 rows=37415 loops=2)
              Hash Cond: (wp.id = g.white)
              Join Filter: ((bp.username ~~* '%'::text) OR (wp.username ~~* '%Tri%'::text))
              ->  Parallel Seq Scan on users wp  (cost=0.00..3147.60 rows=114860 width=17) (actual time=0.010..8.581 rows=97631 loops=2)
              ->  Parallel Hash  (cost=9243.85..9243.85 rows=44394 width=45) (actual time=124.953..124.958 rows=37415 loops=2)
                    Buckets: 131072  Batches: 1  Memory Usage: 7008kB
                    ->  Parallel Hash Join  (cost=5260.81..9243.85 rows=44394 width=45) (actual time=83.708..113.141 rows=37415 loops=2)
                          Hash Cond: (bp.id = g.black)
                          ->  Parallel Seq Scan on users bp  (cost=0.00..3147.60 rows=114860 width=17) (actual time=0.012..8.909 rows=97631 loops=2)
                          ->  Parallel Hash  (cost=4705.88..4705.88 rows=44394 width=32) (actual time=83.000..83.001 rows=37415 loops=2)
                                Buckets: 131072  Batches: 1  Memory Usage: 5760kB
                                ->  Parallel Seq Scan on games g  (cost=0.00..4705.88 rows=44394 width=32) (actual time=0.106..71.923 rows=37415 loops=2)
                                      Filter: (time_control ~~* '%rapid%'::text)
                                      Rows Removed by Filter: 112585
Planning Time: 0.972 ms
Execution Time: 211.283 ms
```

### Interpretation
The database spins up an extra process to help tackle the query. Together, these processes split up the work in join large number of rows between multiple tables through some sort of hashing. Multiple sequential (full-table) scans are also ran in parallel to filter row from the final, sorted query.

### Index
A GIN index is used instead of a traditional b-tree index. These indexes work better for our purposes since we are finding results through variable strings coming from user input, which does not lend well to traditional indices.

SQL Commands used:
``` sql
CREATE EXTENSION pg_trgm; -- Required for GIN indices
CREATE INDEX idx_users_username_trgm ON users USING gin (username gin_trgm_ops);
CREATE INDEX idx_games_time_control_trgm ON games USING gin (time_control gin_trgm_ops);
```

### Post-Index Result

The performance was a little more than we had expected. It is found that the GIN indices do not really come into use if the given queries are not complex enough, so seeing this fairly decent improvement for a relatively minimal query was better than originally anticipated.

Average Improvement: ~40 ms or 20% increase

```
Gather Merge  (cost=17245.81..22350.66 rows=44390 width=32) (actual time=119.585..133.422 rows=74830 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  ->  Sort  (cost=16245.80..16356.78 rows=44390 width=32) (actual time=116.454..119.449 rows=37415 loops=2)
        Sort Key: g.date_played DESC
        Sort Method: quicksort  Memory: 3110kB
        Worker 0:  Sort Method: quicksort  Memory: 3130kB
        ->  Parallel Hash Join  (cost=8705.74..12819.35 rows=44390 width=32) (actual time=71.919..107.375 rows=37415 loops=2)
              Hash Cond: (wp.id = g.white)
              Join Filter: ((bp.username ~~* '%'::text) OR (wp.username ~~* '%Tri%'::text))
              ->  Parallel Seq Scan on users wp  (cost=0.00..3147.60 rows=114860 width=17) (actual time=0.010..6.805 rows=97631 loops=2)
              ->  Parallel Hash  (cost=8150.82..8150.82 rows=44394 width=45) (actual time=70.772..70.776 rows=37415 loops=2)
                    Buckets: 131072  Batches: 1  Memory Usage: 7008kB
                    ->  Parallel Hash Join  (cost=4167.78..8150.82 rows=44394 width=45) (actual time=37.436..60.841 rows=37415 loops=2)
                          Hash Cond: (bp.id = g.black)
                          ->  Parallel Seq Scan on users bp  (cost=0.00..3147.60 rows=114860 width=17) (actual time=0.013..7.069 rows=97631 loops=2)
                          ->  Parallel Hash  (cost=3612.85..3612.85 rows=44394 width=32) (actual time=36.766..36.768 rows=37415 loops=2)
                                Buckets: 131072  Batches: 1  Memory Usage: 5728kB
                                ->  Parallel Bitmap Heap Scan on games g  (cost=557.93..3612.85 rows=44394 width=32) (actual time=8.437..28.222 rows=37415 loops=2)
                                      Recheck Cond: (time_control ~~* '%rapid%'::text)
                                      Heap Blocks: exact=1310
                                      ->  Bitmap Index Scan on idx_games_time_control_trgm  (cost=0.00..539.06 rows=75470 width=0) (actual time=8.941..8.941 rows=74830 loops=1)
                                            Index Cond: (time_control ~~* '%rapid%'::text)
Planning Time: 0.751 ms
Execution Time: 135.800 ms
```
