## CS271P Fall20 Benchmark Max-SAT Problems

**Note:**
Refer to `../fall20-benchmark-parameters.txt` for how these problems are generated.

##### each file has name:
`max-sat-problem-{n}-{k}-{m}-{i}.txt`

###### where 
 - `{n}` - number of variables,
 - `{k}` - number of literals per clause (for files in this folder, **`k` is always `3`**),
 - `{m}` - number of clauses, 
 - `{i}` - is the index (1 ~ p) of the problem instance (for files in this folder, **`i is always 1`**);

##### each file follows format:
 - first row  -> `{n}`
 - second row -> `{k}`
 - third row  -> `{m}`
 - all other (`m`) rows have one clause per row,
    - each clause is a disjunction of literals,
    - each variable is represented by its index (1 ~ N), e.g, `X5` is written as `5`
    - if a variable is negated, it has a `-` symbol before it, e.g., `~X5` is written as `-5`
    - all literals are delimited by a whitespace, e.g., if the clause is `X1 v ~X5 v X35`, the row is `1 -5 35`
