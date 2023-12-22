# GameOfThrones

Summary of First 3 Submissions:

	For our implementation StudentBot for the GoTProblem we decided to use the Alpha-Beta pruning algorithm with a cutoff to determine the best action to take.
	For a heuristic we are focusing on a few distinct factors:
Proximity of White Walkers
Total Space taken by each player
Point in the game (whether we are winning or losing)
Proximity to other players tail

In order to find the proximity of white walkers, we take the coordinates of the closest white walker to the given player and find the minimum amount of moves it would take for the white walker to attack our player

In order to rank total space taken up per player, we are using the static count_space_players method in the GoTProblem class. This tells us the total space owned by both players. We then take the difference of those two and count that number towards our heuristic score.

We decided to take a more aggressive strategy if we were already losing the game and take a more safe strategy if we were winning. We determined whether we were winning or not by the total amount of space we owned vs our opponent.

We also chose to reward game states where we were closer to our opponents hit trail and penalized states where our opponent was close to our hit trail or we were close to our own

Our bot performed well against our opponents and we will briefly summarize how our bots worked against each opponent:

RandBot

This bot was the easiest opponent because its actions are random and even a basic heuristic was good enough to beat it. So our initial implementation of using proximity to white walkers and total space owned was enough to beat it

AttackBot

Similarly, attack bot did not present much of a challenge to our initial implementation and we found that taking a safer strategy of prioritizing total space taken by each player was an effective strategy in opposing the attack bot


SafeBot

SafeBot was the most challenging bot to beat because our safer strategy of counting total space taken up did not always work to beat SafeBot. This is what inspired us to include a section of our heuristic which calculated how our player was doing at mid game states and change how aggressive our bot played based on the outcome. We decided to choose more aggressive moves if we were losing and more safe moves if we were winning. We achieved this by writing different heuristics for our different levels of aggression. I think this strategy made a great impact on our performance against the Safe Bot. Finally, using hit trail proximity as a calculation added another layer to our strategy which allowed us to take a safer strategy and ensure our hit trail wasn’t taken by the opponent.


TABot1

For the first TABot we found that we were able to beat it more easily in the small room however, we encountered more challenges in the big room. In order to beat this bot in the larger room we found that our addition of using hit trail proximity was very helpful in our bot performance staying consistent as the board size scaled.

TABot 2

We found that our implementation that we used for TABot1 was sufficient to beat TABot2 in the smaller room which was the only provided evaluation for this checkpoint

Changes For Final Implementation

For our final implementation we knew that we would have to make some adjustments to our heuristics and bot model to ensure that the white walker interactions were not causing us to lose. In order to do so we made a few important changes:
We changed our white walker proximity calculation to include all white walkers on the board instead of just the closest one.
Found the minimum distance:
Of any white walker to the player’s TEMP
Of opponent to the player’s TEMP
Of the player to PERM
	a.-c. (lines 171, 326) were necessary for comparing a white walker or opponent’s distance to the player’s being less than the distance of the player to its PERM. We tried to minimize these cases, as this would imply that our player could be killed before reaching its safety of PERM territory. The earlier we could catch this smaller ratio (ww_to_temp/opp_to_temp < player_to_perm), the safer path we could create.
Of opponent to its own PERM
Useful in comparing ratio of player to opponent’s tail versus opponent to its own tail: kill shot criteria.
Of the player to the player’s TEMP
Disincentivize crashing into own’s tail
Kept track of whether one of the actions could lead to a killshot
This consisted depended on the following comparison of distances: 
player_to_oppon_perm < oppon_to_its_perm and oppon_to_temp < player_to_perm
We also kept track of whether our location was within a certain distance of white walkers or opponents. We tried to not be in locations where the distance to the player or distance to TEMP were within certain ranges (<1 or <2).
In lines 189-194, we compare the distances of the white walkers and opponents from the previous turn to now. We incentivize taking space or opponent territory (+5) if the white walkers and opponents stayed in same place or are moving away. 
However, we realized there were some vulnerabilities to having too long a tail. At times, the TEMP to PERM ratio (a.-c.) was not dissuasive enough and the player would not return to a PERM space in time. We thus implemented a prevention measure for space grabs to mitigate risk. If the TEMP tail of the player exceeded a length of 5, any free spaces would be taxed by 3*the current length of TEMP tail—carving a path back to PERM locations. 
During the middle of games, as territory began to be dominated and the player and opponent would be focusing on similar regions, we realized our bot was struggling to take new territory and be bold. Instead, it would make repetitive moves in its own territory, as other spaces were close to our opponent or white walker, which were disincentivized. In lines 279-281, we then highlighted free spaces for our bot by +25 if it had no TEMP tail. Our bot would focus now on contiunuing to take territory, and straddle the benefits and costs of nearing an opponent or white walker.

We found that these changes were effective in improving our performance on all bots and it was very effective in evading white walkers. The only section in which we didn't receive full credit was against TABOT1 in which we lost a small amount of points on each section. 
	We think that if we had included some more functionality in our bot implementation to anticipate our opponent bot approaching our hit trail, this could have improved our performance. We also think that if we had tuned the weight of some of our heuristic this could have improved. For example, if we had weighted distance from white walkers more than total space taken up we may have outperformed our current model.

HyperParameter Tuning

There were a couple of significant hyperparameters in our model that we wanted to consider in our final implementation. The most important being the cutoff depth for our alpha-beta pruning model. In the end we settled on a depth of 4 which we found produced the best outcome against all opponent bots.
	Another hyperparameter of interest was our penalization factor. In developing the best path for the player, we would look closely at the distance of an enemy to the player itself or it’s tail. We tried to compound the cost of the player moving closer to an enemy. While these growing deficits would prove helpful in avoiding obvious collisions with opponents, we realized that if the player was more aggressive, it would at times fail to anticipate an oncoming opponent moves down the road. The -60 for ww_to_temp/opp_to_temp < player_to_perm would be a useful calculation to see if any future locations would be too dangerous. Once locations of closer proximity to enemy attack were decided, we found that incentivizing even just slightly (+5) available spaces would make the player continue to annex territory while avoiding any opponent/white walker confrontation. The decision for +25 in lines 279-281 comes from the dilemma of the player repeating the same move in its own territory. A larger incentive was necessary to disrupt this equilibrium the player may fall into, where its TEMP tail was 0 and the risk of venturing out far outweighed the benefit. 

Future Bot Ideas:
Developing a function that incentivizes the trapping of white walkers
Then can switch to heuristic without white walker
Develop a function to trap opponent
Fine tuning when our TEMP tail can be longer to allow for more area to be enclosed
Minimize returning to PERM territory
Only landing on PERM spaces if absolutely necessary
This will allow for more opportunities for expansion
Potentially develop more aggressive strategy that pursues opponent and focuses on hitting opponent tail.
Conclusion

In conclusion we found that using alpha-beta cutoff to select the best action for our bot was a very effective method. We also found that heuristic components such as complete white walker distance and amount of space captured in the board was an effective way of evaluating game states. Finally, we found that being able to change our heuristic depending on points in the game was a really good way to react to mid game changes. Being able to take a more aggressive strategy when the game required it was very effective. 
