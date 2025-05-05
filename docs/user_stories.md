## User Stories
1. As a chess student, I want to see a record of my past games, so I can review my games.
2. As a chess student, I want to find varying statistics about my past games so I can study trends in my own gameplay.
3. As a competitive player, I want to see my current and updates to my Elo score so I can get a sense of my own skill relative to everyone else.
4. As a competitive fan, I want to see a leaderboard of the top chess players and their Elo scores, so I can find the best players to follow.
5. As a chess "edutainer", I want to post snippets of my chess games, so I can educate and entertain other chess fans via my games.
6. As a chess fan, I want to respond to and share feedback with posts, so I can share my thoughts with and support the community.
7. As a community member, I want to report or flag problematic posts and comments, so we can keep our community clean and welcoming.
8. As a community member, I want to search for specific posts, so I can reference and share them with others.
9. As a community member, I want to find new and recommended posts on my feed, so I can explore new content creators and new genres of post.
10. As a community member, I want to filter my feed, so I can specifically find posts matching what I want to see in a given moment.
11. As an "edutainer", I want to see varying statistics about my own posts, so I can gauge what content works and what people want to see.
12. As a chess fan, I want to save posts, so I can quickly reference particularly funny or educational material I have already seen.

## Exceptions
1. There exist no past games
    > If a user has no previously recorded games, there will be placeholder text in their Match History that will invite them to add a new game.
2. Post is deleted mid-interaction (comment/report)
    > An error will be given to the user, letting them know that the post has been deleted and that they should refresh their page.
3. New account has no updates to their Elo score
    > Default Elo score will be assigned (probably 1000) and an update visual will indicate that there are yet to be updates.
4. Multiple accounts on leaderboard have tied Elo scores
    > If there are multiple accounts with tied Elo, we will attempt to tiebreak based on whose Elo was updated most recently (then probably alphabetically).
5. There is not enough storage for a user's new post
    > The user will be alerted that there is not enough space for their new post and will receive suggestion to either wait or delete a previous post.
6. Comments are too long
    > The comment will be truncated to fit within the character limit and the author will receive a notification about the character limit.
7. Incomplete report formatting
    > The reporter will receive an error notifying them about missing necessary fields.
8. No posts match the search
    > If there are no posts that match the search, the search space will be filled with placeholder text indicating that no results matched the user's search.
9. No sufficient new or recommended posts can be sent to users
    > Users will have the latest posts on their feed and there will be an indicator notifying the user that there are no currently new posts.
10. No posts match all my filters
    > Search space will feature placeholder text explaining that no results match all the filters. Below text will be posts deemed relevant which would have shown up if a word was missing from the search, similar to Google's "Does not include: keyword" feature.
11. The post is brand new and there is no data to analyze
    > Appropriate placeholder values (mostly zero) will occupy relevant fields and any analysis feature will instead notify user that the post has insufficient data.
12. Saved post is deleted
    > If a saved post is deleted by the original poster, the post will be removed from all users' saved posts archive and post link will lead to the home page and feature an error telling the user that the post could not be found. 
