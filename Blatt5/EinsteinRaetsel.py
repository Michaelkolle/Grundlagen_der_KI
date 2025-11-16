import time
import random
from collections import defaultdict, deque

def eq_constraint(a, b):
    return a == b


def neq_constraint(a, b):
    return a != b


def left_of(a, b):
    return a == b + 1


def neighbor(a, b):
    return abs(a - b) == 1

class CSP:
    def __init__(self, variables, domains, constraints):

        self.variables = variables
        self.domains = {v: list(domains[v]) for v in variables}
        self.constraints = constraints

        # adjacency list
        self.neighbors = defaultdict(list)
        for (xi, xj) in constraints:
            self.neighbors[xi].append(xj)
            self.neighbors[xj].append(xi)

    # Check consistency of value assignment
    def is_consistent(self, var, value, assignment):
        for other in self.neighbors[var]:
            if other in assignment:
                for f in self.constraints.get((var, other), []):
                    if not f(value, assignment[other]):
                        return False
                for f in self.constraints.get((other, var), []):
                    if not f(assignment[other], value):
                        return False
        return True

def ac3(csp):
    queue = deque(csp.constraints.keys())
    while queue:
        (xi, xj) = queue.popleft()
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True


def revise(csp, xi, xj):
    revised = False
    for x in csp.domains[xi][:]:
        if not any(
                all(f(x, y) for f in csp.constraints.get((xi, xj), []))
                for y in csp.domains[xj]
        ):
            csp.domains[xi].remove(x)
            revised = True
    return revised

class Stats:
    def __init__(self):
        self.assignments = 0
        self.backtracks = 0


def select_unassigned_var(assignment, csp):

    unassigned = [v for v in csp.variables if v not in assignment]
    mrv = min(unassigned, key=lambda v: len(csp.domains[v]))

    degree_counts = [(v, len(csp.neighbors[v])) for v in unassigned if len(csp.domains[v]) == len(csp.domains[mrv])]
    return max(degree_counts, key=lambda x: x[1])[0]


def backtracking_search(csp):
    return backtrack({}, csp, Stats())


def backtrack(assignment, csp, stats):
    if len(assignment) == len(csp.variables):
        return assignment, stats

    var = select_unassigned_var(assignment, csp)
    for value in csp.domains[var]:
        stats.assignments += 1
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value
            result = backtrack(assignment, csp, stats)
            if result:
                return result
        stats.backtracks += 1
        assignment.pop(var, None)
    return None

def min_conflicts(csp, max_steps=20000):
    assignment = {v: random.choice(csp.domains[v]) for v in csp.variables}

    for step in range(max_steps):
        conflicted = [v for v in csp.variables if not is_var_ok(v, assignment, csp)]
        if not conflicted:
            return assignment

        v = random.choice(conflicted)
        best_vals = []
        best_conflicts = 999

        for val in csp.domains[v]:
            assignment[v] = val
            c = count_conflicts(v, assignment, csp)
            if c < best_conflicts:
                best_conflicts = c
                best_vals = [val]
            elif c == best_conflicts:
                best_vals.append(val)

        assignment[v] = random.choice(best_vals)

    return None


def is_var_ok(var, assignment, csp):
    return csp.is_consistent(var, assignment[var], assignment)

def count_conflicts(var, assignment, csp):
    val = assignment[var]
    conflicts = 0
    for other in csp.neighbors[var]:
        if not all(
                f(val, assignment[other])
                for f in csp.constraints.get((var, other), [])
        ):
            conflicts += 1
    return conflicts

def build_einstein_csp():
    positions = [1, 2, 3, 4, 5]

    colors = ["Red", "Green", "White", "Yellow", "Blue"]
    nations = ["Englishman", "Spaniard", "Ukrainian", "Norwegian", "Japanese"]
    drinks = ["Coffee", "Tea", "Milk", "OrangeJuice", "Water"]
    smokes = ["OldGold", "Kools", "Chesterfield", "LuckyStrike", "Parliament"]
    pets = ["Dog", "Snails", "Fox", "Horse", "Zebra"]

    variables = (
            ["Color_" + c for c in colors] +
            ["Nationality_" + n for n in nations] +
            ["Drink_" + d for d in drinks] +
            ["Smoke_" + s for s in smokes] +
            ["Pet_" + p for p in pets]
    )

    domains = {v: positions[:] for v in variables}

    # unary constraints:
    domains["Nationality_Norwegian"] = [1]
    domains["Drink_Milk"] = [3]

    constraints = defaultdict(list)

    def bind(xi, xj, f):
        constraints[(xi, xj)].append(f)

    # AllDifferent constraints (pairwise !=)
    def all_diff(vars_list):
        for i in range(len(vars_list)):
            for j in range(i + 1, len(vars_list)):
                bind(vars_list[i], vars_list[j], neq_constraint)
                bind(vars_list[j], vars_list[i], neq_constraint)

    all_diff(["Color_" + c for c in colors])
    all_diff(["Nationality_" + n for n in nations])
    all_diff(["Drink_" + d for d in drinks])
    all_diff(["Smoke_" + s for s in smokes])
    all_diff(["Pet_" + p for p in pets])

    # Specific constraints
    equal_pairs = [
        ("Nationality_Englishman", "Color_Red"),
        ("Nationality_Spaniard", "Pet_Dog"),
        ("Drink_Coffee", "Color_Green"),
        ("Nationality_Ukrainian", "Drink_Tea"),
        ("Smoke_OldGold", "Pet_Snails"),
        ("Smoke_Kools", "Color_Yellow"),
        ("Drink_OrangeJuice", "Smoke_LuckyStrike"),
        ("Nationality_Japanese", "Smoke_Parliament"),
    ]

    for a, b in equal_pairs:
        bind(a, b, eq_constraint)
        bind(b, a, eq_constraint)

    bind("Color_White", "Color_Green", left_of)
    bind("Pet_Fox", "Pet_Horse", neighbor)
    bind("Smoke_Chesterfield", "Pet_Fox", neighbor)

    # Norwegian lives next to Blue house
    bind("Nationality_Norwegian", "Color_Blue", neighbor)

    return CSP(variables, domains, constraints)

if __name__ == "__main__":
    csp = build_einstein_csp()

    print("\nbacktracking")
    csp_plain = build_einstein_csp()
    t1 = time.perf_counter()
    sol1, stats1 = backtracking_search(csp_plain)
    t1 = time.perf_counter() - t1
    print("Solution found:", sol1 is not None)
    print("Time:", t1, "s")
    print("Assignments:", stats1.assignments, "Backtracks:", stats1.backtracks)

    print("\nAC3 + MRV")
    csp2 = build_einstein_csp()
    ac3(csp2)
    t2 = time.perf_counter()
    sol2, stats2 = backtracking_search(csp2)
    t2 = time.perf_counter() - t2
    print("Solution found:", sol2 is not None)
    print("Time:", t2, "s")
    print("Assignments:", stats2.assignments, "Backtracks:", stats2.backtracks)

    print("\nmin-conflicts")
    csp3 = build_einstein_csp()
    t3 = time.perf_counter()
    sol3 = min_conflicts(csp3)
    t3 = time.perf_counter() - t3
    print("Solution found:", sol3 is not None, "Time:", t3, "s")

    print("\nfinal sulution (from MRV+Degree)")
    sol = sol2

    houses = {i: {} for i in range(1, 6)}
    for var, pos in sol.items():
        category, value = var.split("_")
        houses[pos][category] = value

    for i in range(1, 6):
        print(f"House {i}: {houses[i]}")
