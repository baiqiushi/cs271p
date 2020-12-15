import genMaxSAT
import genTSP


# generate 100 Max-3SAT problems
K = 3
Ns = [100, 200, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
ms = [7.50, 7.15, 6.80, 6.45, 6.10, 5.75, 5.40, 5.05, 4.70, 4.35]

print("===============================")
print("       Max-3SAT problems")
print("===============================")

for N in Ns:
    for m in ms:
        M = int(N / m)
        genMaxSAT.gen_max_sat(N, K, M, 1)

print("===============================")

# generate 100 TSP problems
Ns = [25, 50, 75, 100, 200, 300, 400, 600, 800, 1000]
ks = [0.01, 0.05, 0.1, 0.2, 0.4]
vs = [0.05, 0.25]
U = 100

print("===============================")
print("        TSP problems")
print("===============================")

for N in Ns:
    for k in ks:
        K = int(k * N * N)
        for v in vs:
            V = int(v * U)
            genTSP.gen_tsp(N, K, U, V, 1)

print("===============================")

