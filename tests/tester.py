from .dimacs import *
import os, time

def run_tests(test_num, function, directed = False, graph_converter = 'list', runall = True, without = [], subdir = ''):
    def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
    def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

    pass_counter = test_counter = 0
    start_time = time.monotonic()
    
    directory = rf'{os.path.dirname(os.path.abspath(__file__))}/graphs-lab{test_num}/{subdir}'
    all_files = os.listdir(directory)
    if not runall: all_files = all_files[:5]

    for graph in all_files:
        
        if graph in without: continue

        file_path = os.path.join(directory, graph)

        with open(file_path) as f:
            print(f"TESTING GRAPH: {graph}")

            if not directed: V,L = loadWeightedGraph(file_path)
            else: V,L = loadDirectedWeightedGraph(file_path)

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
                case 'dirlist' :
                    G = [[] for _ in range(V)]
                    for u, v, c in L:
                        u -= 1
                        v -= 1
                        G[u].append((v,c))
                case 'raw' :
                    G = (V,L)
                
            read_sol = readSolution(file_path)

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