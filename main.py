from util import *
import time
import concurrent.futures
import matplotlib.pyplot as plt


def density_plot():
    exec = concurrent.futures.ProcessPoolExecutor(max_workers=20)

    # Plot parameters (Dimension of minesweeper board, number of trials per data point, number of densities to test)
    dim = 30
    num_trials = 20
    p_steps = 20
    bonus = True  # Comment / un comment agents within futures as well

    # Submit all games to the executor
    futures = {}
    for _ in range(num_trials):
        for p in range(p_steps):
            for agent in [
                None,                                    # -> Basic Agent
                (-1, False),                             # -> Improved Agent
                (round(dim * dim * p / p_steps), False)  # -> Bonus: Global Mine Information
                # (-1, True)                             # -> Bonus: Optimized Selection Algorithm
            ]:
                futures[exec.submit(density_trial, dim, round(dim * dim * p / p_steps), agent)] = (p / p_steps, agent)

    t = time.time()

    # Data which will be plotted
    density = [[p / p_steps + i / 200 for p in range(p_steps)] for i in range(3)]
    results = [[0 for _ in range(p_steps)] for i in range(3)]

    # Processing the results and moving them to correct agent
    for f in concurrent.futures.as_completed(futures):
        if futures[f][1]:
            if futures[f][1] == (-1, False):
                results[1][round(futures[f][0] * p_steps)] += f.result() / num_trials
            else:
                results[2][round(futures[f][0] * p_steps)] += f.result() / num_trials
        else:
            results[0][round(futures[f][0] * p_steps)] += f.result() / num_trials

    print("Time: " + str(time.time() - t))

    # Plot the results, Basic, Improved, and Bonus are Red, Green and Blue repsectively
    for i in range(3 if bonus else 2):
        plt.scatter(density[i], results[i], s=5, c=["Red", "Green", "Blue"][i])
    plt.scatter([0, 1], [0, 1], s=0)
    plt.title('Figure 2')
    plt.xlabel('Mine Density (total mines / total cells)')
    plt.ylabel('Final score (identified mines / total mines)')
    plt.savefig('figure2.png')
    plt.show()


def density_trial(dimension, mines, improved):
    # A single minesweeper game
    if improved:
        agent = ImprovedAgent(dimension, mines, improved)
    else:
        agent = BasicAgent(dimension, mines)
    agent.run()
    return agent.score


def play_by_play():
    agent = ImprovedAgent(10, 10, (-1, False, 0))
    agent.run()


if __name__ == "__main__":
    density_plot()
    play_by_play()
