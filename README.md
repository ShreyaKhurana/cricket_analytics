----------


# cricket_analytics

## tl;dr

Modelling the batting order of the Indian ODI Team using Markov chain 

## Introduction

In cricket, there are finite number of possible outcomes once a ball is bowled. Each ball represents a transition from one state to the other. So in total, if we consider our beginning as a separate state, there are 301 possible states, one for after each ball, assuming no extras are bowled during the innings.

This feature makes it possible to use Markov chain to model the probability of a match’s innings going from one state to the other. To make this clearer, we first explain which all possible outcomes exist.

## Model

For the sake of simplicity and accuracy, we only consider the following options once a ball is bowled:

 1. No run taken by the batsman at strike
 2. 1 run taken by the batsman and the strike is changed
 3. 2 runs taken by the batsman but strike remains unchanged
 4. 3 runs taken by the batsman and the strike is exchanged
 5. 4 runs hit by the batsman (boundary). Strike remains with him.
 6. 6 runs hit by the batsman (boundary). Strike remains with him.
 7. No run is taken by the batsman but he is dismissed. He’s either bowled out, stumped, caught or caught LBW (but not run out)

To capture the essence of an innings we only need three measures - runs scored till now, batsman on strike, batsman on the other end. With these two batsmen and the batting order given, we can calculate the total number of wickets that have fallen.

Hence, to see how these vary along as the innings progresses, we need to evaluate all possible combinations of them. Since our assumption of no extras holds, we have a maximum of 300 balls bowled in the innings. The maximum runs that can be scored in one ball is 6. Hence at the end of 300 balls, the maximum score can be 1800 only. However generally, scores do not go over 400 and the maximum ODI score till now has been 443/9 made by Sri Lanka against Netherlands (Amstelveen, July 2006). To reduce the complexity of the model, the maximum runs that can be stored have been taken as 600.

The number of batsman that can be on strike range from the first to the last i.e. 11. This is true for the batsman at the other end too.

Therefore, if we utilize a three-dimensional matrix to represent all the possible permutations of the three variables, its dimensions will be 601 × 11 × 11 . After each ball is bowled, this matrix is updated to contain the probability of reaching that state. The matrix entries represent the probability after the end of the innings of being in that state. To make this clearer, we first define certain probabilities.

 - A batsman is dismissed and no runs score with probability `Pd`
 - Zero runs score (no dismissal) with probability `P0`
 - One run is scored (no dismissal) with probability `P1`
 - Two runs are scored (no dismissal) with probability `P2`
 - Three runs are scored (no dismissal) with probability `P3`
 - Four runs are scored (no dismissal) with probability `P4`
 - Six runs are scored (no dismissal) with probability `P6`

These probabilities are defined for each of the 11 batsmen. We use the notation:  `[runs, Batsman number on strike, batsman at the other end]` to denote each state.

overChange.py calculates the total number of runs made by a batting order. For simplicity, we check only three orders.

If you have time and the resources, you can check out all the 11! possibilities.

The final_scores file gives the final scores of the 'one-man teams' and this is used to rank the players.
(Pls dunt)
