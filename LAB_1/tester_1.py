from dimacs import *
import os, time

def run_tests(directory, function, graph_converter = 'list', runall = True, without = []):
    def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
    def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

    pass_counter = test_counter = 0
    start_time = time.monotonic()
    for graph in os.listdir(directory):
        
        if (not runall and graph != 'g1') or graph in without: continue

        with open(os.path.join(directory, graph)) as f:
            print(f"TESTING GRAPH: {graph}")
            V,L = loadWeightedGraph(f"graphs-lab1/{graph}")

            match graph_converter:
                case 'set':
                    G = (V,L)
                    for u, v, c in L:
                        u -= 1
                        v -= 1
                case 'list' :
                    G = [[] for _ in range(V)]
                    for u, v, c in L:
                        u -= 1
                        v -= 1
                        G[u].append((v,c))
                        G[v].append((u,c))
                
            read_sol = readSolution(f"graphs-lab1/{graph}")

        my_sol = function(G)

        print(f"Expected result: {read_sol}")
        print(f"Given result: {my_sol}")
        
        if my_sol == float(read_sol):
            pass_counter += 1
            prGreen("PASSED\n")
        else: prRed("WRONG\n")

        test_counter += 1

    end_time = time.monotonic()
    print("TEST RESULTS".center(40,'-'))
    print(f"PASSED TESTS: {pass_counter}/{test_counter}".center(40, ' '))
    print(f"TIME: {round(end_time-start_time,4)}s".center(40, ' ') + '\n')