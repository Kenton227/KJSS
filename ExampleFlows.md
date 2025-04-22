# Chess Site Edutainer Showcase Posting Flow
Levy Rozman from GothamChess just had an incredibly close game on his climb to GM and he wants to share his game with the world and use his game as an example of crucial endgame theory. 

First, Levy will log his game into his history using POST ```/user/games/{user_id}/submit```. He will then be able to find this most recent game in his history when he calls GET```/user/games/{user_id}```. From here, he can create a showcase based on this great game, and post it using POST```/showcases/post```. 

But whoops, Levy accidentally posted the showcase without any captions. Luckily, instead of deleting the showcase and posting a new one about the same game, Levy opts to just edit the newly posted one, hoping no one's feed has already received it, with PUT```/showcases/edit/{showcase_id}```. Now, Levy has finished sharing his game with the world!

# Community Member Search and Sharing Showcase Flow
Eager chess student Charlie Brown was talking to his friend Beth Harmon about the London System chess opening. Charlie Brown recounts finding a really funny but impractical response to the opening earlier while scrolling through his feed. 

Wanting to share this showcase to Beth, he searches for the showcase with GET```/showcases/search``` hoping that the title had the phrase 'london system'. Fortunately, a result is returned, and Charlie sends a link to Beth. Together, they both examine the game further through GET```/games/{game_id}```, and share a laugh as they bond over the failed creative attempt to triumph over the London System. Charlie Brown returns to the original post, and leaves a positive comment with POST```/showcases/comment``` humoring the snippet, before they both resume scrolling.

# Reporting Obviously Fake Account Flow
Upstanding community member Sherlock Holmes was scrolling through his feed one day and found a very interesting showcase posted by Cat Branchman. It was a very impressive sequence that was featured, but Holmes noticed something strange. 

Holmes uses the showcase to find the original game using GET```/games/{game_id}``` and examines the moves played by both players, which are rated only around 1200 Elo. Holmes being a professional player himself, noticed that the original showcase poster played suspiciously well for someone with his rating, and investigates further finding his games history with GET```/user/games/{user_id}```. After checking out Cat Branchman's recent win rate, Holmes also checks out Branchman's showcase history to confirm a suspicion using GET```user/showcases/{user_id}```, and, as expected all of these suspicious games were also used for showcases. 

So, Holmes files a report against the account and a few of the showcases by calling POST```/reports/post```. Moreover, Holmes posts comments via POST```/showcases/comment```on a few of Branchman's latest posts urging other people to follow in his footsteps. After a few days, the account and its showcases were all removed from the platform.

