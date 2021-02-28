from util import *

d = 10
n = 10
num_trials = 100
sum_scores = 0.0
for _ in range(num_trials):
    ba = BasicAgent(d, n)
    ba.run()
    sum_scores += ba.score
print('Average score: ' + str(round(sum_scores / num_trials, 2)))
