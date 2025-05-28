# Code Review

## 1. Currently, when running alembic upgrade head you get a warning that there are two heads
*Suggestion*: Merge your heads with: uv run alembic merge -m "merge heads" 079499fe7aca d8cb70c89a56

*Response*: Done!

## 2. In showcases.py your ShowcaseRequest has user_id as a string, but everyone else in the codebase user_id is an int
*Suggestion*: Change your ShowcaseRequest to user_id: int

*Response*: Good catch!

## 3. In showcases.py your comment class has a field named auther_uid
*Suggestion*: Change it to author_id for correct spelling, consistency, and clarity.

*Response*: Done!

## 4. GameSubmitData and GameModel time control with repeated string literals
*Suggestion*: Put these in enums like so
```
class TimeControl(str, Enum):
    classical = "classical"
    rapid = "rapid"
    blitz = "blitz"
    bullet = "bullet"
```

*Response*: Done, and applied to replace other similar validators with enums, too!

## 5. Your class "comment" in showcases.py should be capitalized
*Suggestion*: Rename it to Comment to follow your capitalization scheme for all the other classes.

*Response*: Done!

## 6. In games.py, get_game() uses .one() without a fallback
*Suggestion*: If the game doesnt exist, the you get a 500 Error. It should return a 404 with HTTPException(status_code=404, detail="Game not found").

*Response*: Done!

## 7. In edit_showcase(), there’s no response or feedback when both fields are empty
*Suggestion*: If both title and caption are empty, nothing is updated but the client still gets a 204 No Content without knowing nothing happened. Probably return a 400 here instead.

*Response*: Edit request now has a model validator that ensures both cannot be empty! (Raises a 422)

## 8. Endpoint naming is not RESTful
*Suggestion*: Double check your endpoints and put them in REST format, for example
> - `/showcases/post` should be `POST /showcases`
> - `/showcases/edit/{id}` should be `PUT /showcases/{id}`

*Response*: Done!

## 9. No input validation on title, caption, or comment_string
*Suggestion*: ShowcaseRequest, EditRequest, and comment models allow empty strings. Add Field(..., min_length=1) to prevent users from submitting blank content. Maybe in your schema caption could be optionally blank, but I would assume title should be required.

*Response*: Added specified Field to classes! Also adjusted caption to be an optional str.

## 10. get_history() in user.py uses SELECT * instead of explicit columns
*Suggestion*: Using SELECT * can break if your schema changes and doesn’t guarantee the result shape will match GameModel. Listing the columns used in the response model also makes it clearer.

*Response*: Done! Plus, get_history() now provides error details on missing user or missing games.

## 11. There is no check for invalid opponent_id in game submission
*Suggestion*: In submit_game(), the code assumes that the opponent_id is valid and exists in the database, but theres no check for it. This will cause issues when submitting a game for a user_id that doesn't exist yet, so add a check there so you don't get a 500 Error.

*Response*: Bad player IDs (either user or opponent) now return a 422!


## 12. createGameModel() logic is really hard to read and confusing
*Suggestion*: Refactor to assign black and white directly using clear variable names based on game_data.color, and determine the winner explicitly.

*Response*: Refactored createGameModel():       
>1. Now called create_game_model() to follow python's snake case conventions
>2. Uses explicit variables (and python's tuple assignment) instead of lists and constant indexes
>3. Winner is now stored in an explicit variable and determined in a way that is (hopefully) more readable.

# Schema and API Design

## 1. showcase_comments table lacks timestamp and ordering field
*Suggestion*: The showcase_comments table has no created_at timestamp. This makes it impossible to consistently sort by comment date (for example newest), which is something also every comment section would have as a feature.

*Response*: Done!

## 2. Inconsistent data type usage for user_id
*Suggestion*: Your user_id is used something as a string and sometimes as an int, normalize it

*Response*: Done!

## 3. In showcases/{showcase_id}/comment POST endpoint, post_id is user-specified instead of server-incremented
*Suggestion*: Your post_id should just start at 1 and increment with every entry, theres no need for users to specify a specific id as its not a foreign key

*Response*: Done! Plus, comment now details bad user/showcase references on error.

## 4. No route for retrieving comments
*Suggestion*: You can post a comment with POST /showcases/{id}/comment, but there’s no corresponding GET /showcases/{id}/comments, so theres no point in posting comments if the data is effectively never used.

*Response*: Done! Endpoint also returns 404 on missing showcase ID.

## 5. No delete endpoints for user-generated content
*Suggestion*: In most systems, users can both post and delete their comments. Currently, users can post showcases and comments, but there’s no way to delete them so add those endpoints.

*Response*: Done! Endpoints return 404 on missing non-existent showcase/comment IDs.

## 6. Missing success responses
*Suggestion*: Most routes return 204 No Content and don't return any meaningful data after creation. This makes it hard for frontend clients to know what happened. For example, your post report endpoint should return a 201 created, and then probably the reports id.

*Response*: Done!

## 7. Limited entries in get games
*Suggestion*: /user/games/{user_id} returns a fixed number of items (20), but doesn’t allow clients to request more. So effectively, you're still storing more than 20 of their games in the database, but those older games are just completely inaccessible.

*Response*: For the purpose of the project (since there is no frontend), we are choosing to keep the LIMIT of 20 to keep the idea in code. However, added a new endpoint which allows searching through all existing games (by user or by time control), which makes these older games accessible as suggested.

## 8. No sorting support on list endpoints
*Suggestion*: Endpoints like /user/games/{user_id} and /user/showcases/{user_id} return results in a fixed sort order (most recent first), but there’s no way to sort by other fields like duration, views, or oldest first.

*Response*: There is no strong reason why these intentially simple endpoints would support sorting by other values, especially when they are already defined to return data in a specific order (most recent first, as you stated). However, games and showcases now have endpoints that allow searching, which fill this analytical function, and make more sense to be on those endpoints.

## 9. No way to retrieve reports
*Suggestion*: Users can submit reports via POST /reports/post, but there is no way for an admin or moderator to retrieve and view them (aside from manually looking through the tables). Add a GET /reports endpoint to have a better moderation workflow.

*Response*: New endpoint that fetches either all reports or a specific one given an id.

## 10. No GET route to retrieve a single showcase / sorting
*Suggestion*: There’s no GET /showcases/{id} to fetch an individual showcase’s details. Clients must either get all showcases for a user or none. If someone has many showcases and you only want to view a specific one, it makes it inconvenient to browse through all of them. It also doesn't have any sorting parameters.

*Response*: New endpoint to fetch a single showcase in showcases.py. Sorting will be handled by the searching endpoint.

## 11. Reports table doesn’t track resolution status
*Suggestion*: The reports table stores submitted reports, but there’s no way to mark them as reviewed, resolved, or dismissed, which are likely things that an admin would want to set after reviewing reports.

*Response*: Done! (New column 'status' in reports table)

## 12. Games are not linked to users via a clear creator or submitter field
*Suggestion*: While games track black and white player IDs, there’s no field identifying who submitted or created the game. This makes it difficult to distinguish between a player who participated in the game and the one who logged it, or published the game. For example, both users in a match can’t currently see “your games” vs. “games others uploaded about you.”

*Response*: Our vision for this project has changed, and among these changes include the notion that our service would allow users to play chess on-site and games would be automatically recorded. Thus, there exists no need to distinguish who logged the game. It becomes up to either player to "log" the game they have just completed, requiring only one of the players to do so for the game to be stored. For the purpose of showcases, any recorded game the user is involved in, is treated as if the user was the original logger for the game.

## 13. Add responses for all of your endpoints
*Suggestion*: Most of your post endpoints only return a 204 without a body, so its hard to tell what is actually going on, let the user know if a post was successful

*Response*: Done (this was already addressed in suggestion 6).