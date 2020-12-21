import csv
import glob
import os

# 0. init common data structures
#    a list of teams (teams), each team has a list of (student id, student_name) tuples
teams = []

# 1. read roster.csv to build student_id -> student_name map (roster), student_unet_id -> student_id map (roster2)
roster = {}
roster2 = {}
with open("roster.csv", "r") as csv_in:
    csv_reader = csv.reader(csv_in, delimiter=',', quotechar='"')
    next(csv_reader)  # ignore header
    for row in csv_reader:
        roster[row[0]] = row[1]
        email = row[2]
        unet_id = email.split("@")[0].lower()
        roster2[unet_id] = row[0]


# print(roster)
# print(roster2)


# handle case when student_id is uci net id
def verify_student_id(student_id):
    if student_id.isdigit():
        return student_id
    else:
        # lookup in the roster2 assuming student_id is the unet_id
        if student_id.lower() in roster2.keys():
            student_id = roster2[student_id.lower()]
            return student_id
        else:
            return None


# 2. loop 2 problem types (Max-SAT/TSP), 2 methods (SLS/BnB) to build a map (categories)
#    with 4 keys (problem type, method),
#       for each key, value is a map (results)
#       with with 100 keys (problem-file-name),
#           for each key, value is a list of results from different teams
categories = {("max-sat", "sls"): {},
              ("max-sat", "bnb"): {},
              ("tsp", "sls"): {},
              ("tsp", "bnb"): {}}

# init Max-SAT problem file names
max_sat_filenames = []
K = 3
Ns = [100, 200, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
ms = [4.35, 4.70, 5.05, 5.40, 5.75, 6.10, 6.45, 6.80, 7.15, 7.50]
for N in Ns:
    for m in ms:
        M = int(m * N)
        filename = "max-sat-problem-" + str(N) + "-" + str(K) + "-" + str(M) + "-1.txt"
        categories[("max-sat", "sls")][filename] = []
        categories[("max-sat", "bnb")][filename] = []
        max_sat_filenames.append(filename)

# init TSP problem file names
tsp_filenames = []
Ns = [25, 50, 75, 100, 200, 300, 400, 600, 800, 1000]
ks = [0.01, 0.05, 0.1, 0.2, 0.4]
vs = [0.05, 0.25]
U = 100
for N in Ns:
    for k in ks:
        K = int(k * N * N)
        for v in vs:
            V = int(v * U)
            filename = "tsp-problem-" + str(N) + "-" + str(K) + "-" + str(U) + "-" + str(V) + "-1.txt"
            categories[("tsp", "sls")][filename] = []
            categories[("tsp", "bnb")][filename] = []
            tsp_filenames.append(filename)

# print(categories)


# 3. read all results files (*.csv) in the current folder
#      for each file:
for filename in glob.glob('./competition/*.csv'):
    print("Process file [" + filename + "]...")
    with open(os.path.join(os.getcwd(), filename), "r", encoding='utf-8-sig') as csv_in:
        csv_reader = csv.reader(csv_in, delimiter=',', quotechar='"')
        #        3.1. read the first line, extract the list of student_ids:
        #               lookup in teams list, if student_ids exist there, use offset as the team_id
        #                                     otherwise, append a new team there, use offset as the team_id
        row1 = next(csv_reader)
        student_id = row1[0].strip()  # first student_id
        student_id = verify_student_id(student_id)
        if student_id is None:
            print("[ERROR] Invalid student_id in row")
            print(row1)
            exit(-1)

        team_id = None
        # find existing team with student_id
        for team in teams:
            for student in team:
                if student_id == student[0]:
                    team_id = teams.index(team)
        # otherwise, create a new team with all students in row1
        if team_id is None:
            # print("team with student_id " + student_id + " not found.")
            team = []
            for student_id in row1:
                student_id = student_id.strip()
                student_id = verify_student_id(student_id)
                if student_id is None:
                    print("[ERROR] Invalid student_id in row")
                    print(row1)
                    exit(-1)
                if student_id not in roster.keys():
                    print("[ERROR] Can NOT find student_id (" + student_id + ") in roster! File = " + filename)
                    exit(-1)
                else:
                    team.append((student_id, roster[student_id]))
            team_id = len(teams)
            teams.append(team)
        #        3.2. read the second + third lines, get the method and problem_type
        #               find the (results) map from the (categories) map with key: (problem_type, method),
        method = next(csv_reader)[0].lower()
        problem_type = next(csv_reader)[0].lower()
        print("    This file is about (" + problem_type + ", " + method + ")")
        results = categories[(problem_type, method)]
        # print(filename)
        # print("    " + problem_type)
        # print("    " + method)
        #        3.3. read the remaining lines, for each line:
        #               get the (problem-file-name, result),
        #                 append a new tuple (team_id, result) to the value (a list of results) in the (results) map,
        #                 with key: (problem-file-name)
        count = 0
        for row in csv_reader:
            if len(row) < 2:
                print("    [ERROR] column > 2, skip row: " + str(row))
                continue
            problem_file_name = row[0]
            # handle case when it has path
            if "/" in problem_file_name:
                problem_file_name = problem_file_name[problem_file_name.rfind("/") + 1:]
            # ignore not benchmark problems
            if problem_file_name not in results:
                print("    [ERROR] " + problem_file_name + " not recognized, skip row: " + str(row))
                continue
            # ignore entry where no result value output
            try:
                result = float(row[1])
            except ValueError:
                print("    [ERROR] invalid result value " + row[1] + ", skip row: " + str(row))
                continue
            results[problem_file_name].append((team_id, result))
            count += 1
        print("    " + str(count) + " result values counted.")


# output teams
# Team_{id}:
#    (student_id, student_name)
#    ...
print("\n\n\n")
print("======================================= Teams =======================================")
for team_id in range(len(teams)):
    print("Team_" + str(team_id) + ":")
    for student in teams[team_id]:
        print("    (" + student[0] + ", " + student[1] + ")")
print("=====================================================================================")


# 4. process the (categories) map,
# loop 2 problem types (Max-SAT/TSP), 2 methods (SLS/BNB) in the (categories) map,
for problem_type in ["max-sat", "tsp"]:
    for method in ["sls", "bnb"]:
        print("\n\n\n")
        print("==============================================================================")
        print("    " + problem_type + ",    " + method)
        print("==============================================================================")
        results = categories[(problem_type, method)]

        # create a map (team_scores) of {team_id -> score},
        team_scores = {}

        # output orderings for each problem to file "{problem_type}_{method}_results.csv",
        results_filename = problem_type + "_" + method + "_results.csv"
        with open(results_filename, "w") as csv_out:
            csv_writer = csv.writer(csv_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # for Max-SAT problems
            if problem_type == "max-sat":
                # for each problem file
                for filename in max_sat_filenames:
                    result_list = results[filename]
                    # sort the list of results (team_id, result) by result value in descending order
                    result_list = sorted(result_list, key=lambda x: x[1], reverse=True)
                    # print a line to the file: problem-file-name, first team_id, result, second_team_id, result, ...
                    row = [filename]
                    row.extend(result_list)
                    csv_writer.writerow(row)
                    # print a line to the screen: problem-file-name: first (team_id, result), second (team_id, result), ...
                    row = ""
                    for team in result_list:
                        row += " (" + str(team[0]) + ", " + str(team[1]) + ")"
                    print(filename + ": " + row)
                    # add 1 score to the first team_id in the (teams_scores) map
                    if len(result_list) > 0:
                        top_team = result_list[0]
                        top_team_id = top_team[0]
                        top_team_result = top_team[1]
                        if top_team_id in team_scores:
                            team_scores[top_team_id] += 1
                        else:
                            team_scores[top_team_id] = 1

            # for TSP problems
            if problem_type == "tsp":
                # for each problem file
                for filename in tsp_filenames:
                    result_list = results[filename]
                    # sort the list of results (team_id, result) by result value in ascending order
                    result_list = sorted(result_list, key=lambda x: x[1])
                    # print a line to the file: problem-file-name, first team_id, result, second_team_id, result, ...
                    row = [filename]
                    row.extend(result_list)
                    csv_writer.writerow(row)
                    # print a line to the screen: problem-file-name: first (team_id, result), second (team_id, result), ...
                    row = ""
                    for team in result_list:
                        row += " (" + str(team[0]) + ", " + str(team[1]) + ")"
                    print(filename + ": " + row)
                    # add 1 score to the first team_id in the (teams_scores) map
                    top_team = result_list[0]
                    top_team_id = top_team[0]
                    top_team_result = top_team[1]
                    if top_team_id in team_scores:
                        team_scores[top_team_id] += 1
                    else:
                        team_scores[top_team_id] = 1

        print("------------------------------------------------------------------------------")
        print("    Team Scores")
        print("------------------------------------------------------------------------------")
        # output team_scores for this category to file "{problem_type}_{method}_team_scores.csv"
        team_scores_filename = problem_type + "_" + method + "_team_scores.csv"
        # sort team_scores by score in descending order
        sorted_team_scores = dict(sorted(team_scores.items(), key=lambda item: item[1], reverse=True))
        with open(team_scores_filename, "w") as csv_out:
            csv_writer = csv.writer(csv_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # print header to the file
            csv_writer.writerow("Team_Id,    Score")
            for team_score in sorted_team_scores.items():
                # print a line to the file: Team_Id, Score
                csv_writer.writerow(["Team_" + str(team_score[0]), team_score[1]])
                # print a line to screen: Team_Id: Score
                print("Team_" + str(team_score[0]) + ": " + str(team_score[1]))


