#Runner Rank: Experimental ranking procedure for NCAA and High School Cross-Country/Track and Field

The goal of Runner Rank is to create, from some arbitrary collection of race results, a sorted list of all the runners ranked 
from strongest to weakest. This process is made less intuitive by the fact that race courses vary dramatically in difficulty. For example, 
say athlete A ran 15:30 in his most recent 5k race and athlete B ran 15:00 in a different race. These performances appear dramatically 
different by plain observation. However, say A’s race was run at 5000 ft. of altitude, or was in 90 degree heat, or was a hilly course, 
it might then be the case that A’s performance is a better indicator of fitness than B’s. This issue makes it difficult to rank individual 
athletes and teams in the sport, and often the outcome of national and state finals can be surprising. 

Runner Rank solves this problem by ‘partially’ isolating the notion of completion time in the comparison of athletes. Instead, 
Runner Rank determines the quality of an athlete by a weighted sum of the scores of the athletes he/she has defeated in competition. 
When athlete A beats athlete B in competition, athlete A receives a portion of B’s score. If Athlete A is the only athlete to defeat 
athlete B, then A’s score will be boosted by B’s score. If multiple athletes have defeated B (most likely that this will be the case), 
then the exact score boost will be divided among the athletes based on victory margin. Finally, older results will be scaled down relative 
to more recent results. 

This leaves us with a self-referential web of athlete nodes, and the problem reduces to finding an eigenvector solution to a large matrix.
My program uses the ‘power method’ to efficiently produce a rankings vector for the athletes in the system. The goal is to be able to use 
this rankings vector to predict future race outcomes more accurately than human intuition. 

I am currently working to tune the model and I will compare the effectiveness of different models by how accurately they reflect the 
outcomes of Nike Cross Nationals and Footlocker Nationals as well as the recent NCAA D1 championship race.  
