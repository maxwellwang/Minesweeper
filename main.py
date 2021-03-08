from util import *
import time
d = 16
n = 40
num_trials = 100
sum_scores = 0.0
t = time.time()
for _ in range(num_trials):
    ba = ImprovedAgent(d, n)
    ba.run()
    sum_scores += ba.score
print('Average score: ' + str(round(sum_scores / num_trials, 3)))
print(time.time() - t)
