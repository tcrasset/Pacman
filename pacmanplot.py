from matplotlib import pyplot as plt
import numpy as np
def buildPlot(title, data, ylabel, filename):
    nb_maps = 3
    maps = ["small", "medium", "large"]
    algorithms = ["dfs", "bfs", "ucs", "astar"]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    nb_algo = 4
    bar_width = .15
    
    for j in range(nb_maps):
        plt.figure()
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel("Map: {}".format(maps[j]))
        plt.xticks([])
        ax = plt.subplot(111)

        for i in range(nb_algo):
            plt.bar((0.05+ bar_width)*i, data[j][i], width=bar_width,color=colors[i])
            ax.legend(["Algo {}".format(i) for i in algorithms],
                        loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
        plt.savefig("{}_{}.svg".format(filename,maps[j]), format="svg")
        plt.show()


#[DFS BFS UCS A*]
small_layout_score = [500, 502, 502, 502]
small_layout_time = [0.00146, 0.00172, 0.00315, 0.00190]
small_layout_expanded = [15, 16, 16, 16]


#[DFS BFS UCS A*]
medium_layout_score = [414, 570, 570, 570]
medium_layout_time = [0.0512, 7.695, 8.245, 4.725]
medium_layout_expanded = [362, 17432, 13241, 8808]


#[DFS BFS UCS A*]
large_layout_score = [319, 434, 434, 434]
large_layout_time = [0.111, 0.619, 0.786, 0.470]
large_layout_expanded = [378, 2134, 2065, 1014]

total_score = [
    small_layout_score,
    medium_layout_score,
    large_layout_score
]

run_times = [
    small_layout_time,
    medium_layout_time,
    large_layout_time
]

total_expanded = [
    small_layout_expanded,
    medium_layout_expanded,
    large_layout_expanded
]

buildPlot("Running times of different search algorithms", run_times, "Running time (s)", "run_times")
buildPlot("Total number of expanded nodes for different search algorithms", total_expanded, "Number of expanded nodes", "total_expanded")
buildPlot("Total score for different search algorithms", total_score, "Total score", "total_score")
