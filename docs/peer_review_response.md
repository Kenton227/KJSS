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

*Response*: 
TODO

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
