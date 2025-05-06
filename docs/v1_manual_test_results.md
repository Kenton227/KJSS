# Chess Site Edutainer Showcase Posting Flow
Levy Rozman from GothamChess just had an incredibly close game on his climb to GM and he wants to share his game with the world and use his game as an example of crucial endgame theory. 

First, Levy will log his game into his history using POST ```/user/games/{user_id}/submit```. He will then be able to find this most recent game in his history when he calls GET```/user/games/{user_id}```. From here, he can create a showcase based on this great game, and post it using POST```/showcases/post```. 

But whoops, Levy accidentally posted the showcase without any captions. Luckily, instead of deleting the showcase and posting a new one about the same game, Levy opts to just edit the newly posted one, hoping no one's feed has already received it, with PUT```/showcases/edit/{showcase_id}```. Now, Levy has finished sharing his game with the world!


# Testing Results

1. 