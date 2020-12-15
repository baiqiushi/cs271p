## CS271P Fall20 Benchmark TSP Problems

**Note:**
Refer to `../fall20-benchmark-parameters.txt` for how these problems are generated.

##### each file has name:
`tsp-problem-{n}-{k}-{u}-{v}-{i}.txt`

###### where 
 - `{n}` - number of locations,
 - `{k}` - number of distinct distance values to use,
 - `{u}` - mean of normal distribution for distances (for files in this folder, **`u is always 100`**),
 - `{v}` - variance (standard deviation) of normal distribution for distances, 
 - `{i}` - is the index (1 ~ p) of the problem instance (for files in this folder, **`i is always 1`**);

##### each file follows format:
 - first row  -> `{n}`
 - all other (`n`) rows compose the adjacency matrix for a complete graph,
   - row `i` are writen with distances from location `i` to all other locations,
   - distances are delimited by whitespace.
