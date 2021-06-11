<h1>Reinforcement Learning: An Introduction</h1>
<h2>Mountain Car</h2>
<p>
The mountain car problem involves a car starting somewhere near the center of the valley in the curve below. 
The car has the option of accelerating backwards, forwards, or not accelerating at each timestep.
When the car gets all the way to the top of the mountain on the right it will have reached its goal state. 
In this example we are using a greedy search algorithm, but combining it with an optimistic start
for every new state to encourage exploration to unknown state. 
As the state space is massive. Tiling is used as a value function estimation
</p>
<h3>The Mountain</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/mountain_car/mountain_curve.png">
</p>
<h3>The Pull of Gravity</h3>
<p>
This curve is the derivative of the mountain and is the hurdle our car must face.
Where the curve is positive, the car is being pulled to the center of the valley.
The inverse is true for the negative side of the curve. The curve moves back up on the right
as the slope of the mountain decreases near the top.
</p>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/mountain_car/gravity_curve.png">
</p>
<h3>Cost to Go</h3>
<p>
The cost to go curve visualizes roughly how far a given state is from the goal state.
As the episodes go on, more state have a chance to be explored and evaluated and refined.
Thus more states start to increase in value to their true "cost to go".
</p>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/mountain_car/cost_to_go.png">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/mountain_car/cost_to_go_rotation.gif">
</p>
<h3>Learning Curves</h3>
<p>
This graph shows how fast and how well four different alpha and n-step evaluation configurations converge to the optimal steps taken per episode.
The first three curves look forward a single step when creating their estimations and are used to compare step size alpha values.
The final red curve shows how these single step look ahead curves compare
to averaging a states estimation based on the next 8 steps to follow.
</p>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/mountain_car/learning_curves.png">
</p>
<h3>More Learning Curves</h3>
<p>
These curves are similar to the last set, but here we are looking at lines which represent a given n-step look ahead state evaluation at multiple step sizes. The lower the averaged number of steps per episode the better.
Note that some curves shoot up rapidly at higher step sizes. This is because past a certain point, these step sizes will not converge and need to be cut short.
</p>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/mountain_car/more_learning_curves.png">
</p>

<h2>Chapter 4:</h2>
<h3>Exercise 4-7:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-7/PolicyImprovement.png">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-7/PolicyEvaluation.png">
</p>

<h3>Exercise 4-9:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/128CapitalPh40PercentActions.png" width="350">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/128CapitalPh40PercentValues.png" width="350">
</p>

<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/127CapitalPh40PercentActions.png" width="350">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/127CapitalPh40PercentValues.png" width="350">
</p>

<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/100CapitalPh60PercentActions.png" width="350">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/100CapitalPh60PercentValues.png" width="350">
</p>

<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/127CapitalPh60PercentActionsWithGreatestAction.png" width="350">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise4-9/127CapitalPh60PercentValuesWithGreatestAction.png" width="350">
</p>
<h2>Chapter 5:</h2>
<h3>Example 5-1:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example5-1/BlackjackOnPolicyStateValues10000Episodes.png" >
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example5-1/BlackjackOnPolicyStateValues500000Episodes.png" >
</p>
<h3>Example 5-3:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example5-3\BlackjackExplorationStartPi5000000Episodes.png" >
</p>
<h2>Chapter 6:</h2>
<h3>Example 6-2:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example6-2/RandomWalkEstimatedValue.png">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example6-2/RandomWalkRMSE.png">
</p>
<h3>Example 6-5:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example6-5/WindyGridworldAccumulatedTime.png">
</p>
<h3>Example 6-6:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example6-6/CliffWalking.png">
</p>
<h3>Example 6-7:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example6-7/MaximizationBiasPercentLeft.png">
</p>
<h3>Exercise 6-5:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise6-5/RandomWalkRMSEInitials.png">
</p>
<h3>Exercise 6-9:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise6-9/WindyGridworldKingMovesAccumulatedTime.png">
</p>
<h3>Exercise 6-10:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise6-10/WindyGridworldKingMovesStochasticWindAccumulatedTime.png">
</p>



<h2>Chapter 7:</h2>
<h3>Example 7-1:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example7-1/nstepTDMethodsontheRandomWalk.png">
</p>
<h3>Exercise 7-2:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise7-2/sumTDvsnStepPrediciton.png">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/exercise7-2/sumTDvsnStepPredicitonDifference.png">
</p>

<h2>Chapter 8:</h2>
<h3>Example 8-1:</h3>
<p align="center">
    <img src="https://github.com/cvmaggio/ReinforcementLearningSutton-Barto/blob/main/figures/example8-1/DynaMaze.png">
</p>