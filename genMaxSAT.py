import argparse
import random


###########################################################
#  genMaxSAT.py
#
# Purpose:
#   generate random Max-SAT problems
#
# Parameters:
#   -n  --  number of variables
#   -k  --  number of literals per clause
#   -m  --  number of clauses
#   -p  --  number of problem instances to generate
#
# Dependencies:
#   (1) Python 2.7+ & pip
#   (2) pip install argparse
#
# Output: [p] files
#   each file has name:
#       max-sat-problem-{n}-{k}-{m}-{i}.txt
#         (where {n}, {k}, {m} are the corresponding parameters, and {i} is the index (1~p) of the problem instance)
#   each file follows format:
#       - first row  -> {n}
#       - second row -> {k}
#       - third row  -> {m}
#       - all other (m) rows have one clause per row,
#           each clause is a disjunction of literals,
#           each variable is represented by its index (1~N), e.g, X5 is written as "5" (without quotes)
#           if a variable is negated, it has a "-" symbol before it, e.g., ~X5 is written as "-5" (without quotes)
#           all literals are delimited by a whitespace,
#             e.g., if the clause is X1 v ~X5 v X35, the row is "1 -5 35" (without quotes)
#
# Author:
#   Qiushi Bai (qbai1@uci.edu)
#
# Version:
#   Nov-28-2020
#
###########################################################

if __name__ == "__main__":

    # parse parameters
    parser = argparse.ArgumentParser(description="Generate random Max-SAT problems.")
    parser.add_argument("-n", "--n", help="N: number of variables", required=True, type=int)
    parser.add_argument("-k", "--k", help="K: number of literals per clause", required=True, type=int)
    parser.add_argument("-m", "--m", help="M: number of clauses", required=True, type=int)
    parser.add_argument("-p", "--p", help="P: number of problem instances to generate (default: 1)", required=False, type=int, default=1)
    args = parser.parse_args()

    n = args.n
    k = args.k
    m = args.m
    p = args.p

    if n < 1:
        print("[Error parameters] N can NOT be < 1. Exit.")
        exit(0)

    if k < 1:
        print("[Error parameters] K can NOT be < 1. Exit.")
        exit(0)

    if m < 1:
        print("[Error parameters] M can NOT be < 1. Exit.")
        exit(0)

    if p < 1:
        print("[Error parameters] P can NOT be < 1. Exit.")
        exit(0)

    if n > k * m:
        print("[Warning] N > K * M, which means there must be variables not existing in any clause.")

    print("generating " + str(p) + " problems with parameters: N=" + str(n) + ", K=" + str(k) + ", M=" + str(m) + "...")
    filename_prefix = "max-sat-problem-" + str(n) + "-" + str(k) + "-" + str(m) + "-"
    # loop problem instances
    for i in range(1, p + 1):
        filename = filename_prefix + str(i) + ".txt"
        outfile = open(filename, "w")
        outfile.write(str(n) + "\n")
        outfile.write(str(k) + "\n")
        outfile.write(str(m) + "\n")
        # init candidate vars list
        x_candidates = range(1, n + 1)
        # loop m clauses
        for j in range(0, m):
            # randomly sample k vars from candidate vars list without replacement (no duplicates)
            selected_x = random.sample(x_candidates, k)
            # remove selected x from candidate vars list
            x_candidates = [x for x in x_candidates if x not in selected_x]
            # loop k vars selected
            clause = []
            for x in selected_x:
                # generate positive or negative symbol for var
                pos_x = random.randint(0, 1)
                if pos_x == 0:
                    x = -x
                clause.append(str(x))
            outfile.write(" ".join(clause) + "\n")

            # re-populate candidate vars list if it has not enough candidates
            if len(x_candidates) < k:
                x_candidates = range(1, n + 1)
        outfile.close()
    print("generation is done.")

