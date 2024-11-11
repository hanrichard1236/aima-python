import collections, sys, os
from logic import *
from planning import *

############################################################
# Problem: Planning 

# Blocks world modification
# def blocksWorldModPlan():
#     # BEGIN_YOUR_CODE (make modifications to the initial and goal states)
#     initial_state = 'On(A, B) & Clear(A) & OnTable(B) & OnTable(C) & Clear(C)'
#     goal_state = 'On(B, A) & On(C, B)'
#     # END_YOUR_CODE

#     planning_problem = \
#     PlanningProblem(initial=initial_state,
#                     goals=goal_state,
#                     actions=[Action('ToTable(x, y)',
#                                     precond='On(x, y) & Clear(x)',
#                                     effect='~On(x, y) & Clear(y) & OnTable(x)'),
#                              Action('FromTable(y, x)',
#                                     precond='OnTable(y) & Clear(y) & Clear(x)',
#                                     effect='~OnTable(y) & ~Clear(x) & On(y, x)')])
    
#     return Linearize(GraphPlan(planning_problem).execute())



#part 3
#initial and goal states
#Case 1 init = 'At(R1, D1) & On(C1, R1) & At(C2, D1) & At(C3, D2) & At(E, D3) & IsRobot(R1)' goal = 'At(C1, D3) & At(C2, D3) & At(C3, D3)' need the At(E, D3) as it would error without
#Case 2 init = 'At(R1, D1) & On(C1, R1) & At(C2, D1) & At(C3, D2) & IsRobot(R1)' goal = 'At(C1, D2)'
#Case 3 init = 'At(R1, D1) & On(C1, R1) & At(C2, D1) & At(C3, D2) & IsRobot(R1)' goal = 'At(C1, D1) & At(R1, D2)'
#Case 4 init = 'At(R1, D1) & On(C1, R1) & At(C2, D1) & At(C3, D2) & At(E, D3) & IsRobot(R1)' goal = 'At(C1, D1) & At(R1, D2) & On(C3, R1)'
def logisticsPlan():
    # BEGIN_YOUR_CODE (use the previous problem as a guide and uncomment the starter code below if you want!)
    initial_state = 'At(R1, D1) & On(C1, R1) & At(C2, D1) & At(C3, D2) & At(E, D3) & IsRobot(R1) & Hfull(R1) & Addable(C1, C3) & Addable(C3, C1)'
    goal_state = 'At(C1, D1) & At(R1, D2) & On(C3, R1)'
    planning_problem = \
    PlanningProblem(initial=initial_state,
                    goals=goal_state,
                    actions=[
                        Action('ELoad(r, b, d)',
                            precond='At(r, d) & At(b, d) & Empty(r) & IsRobot(r)',
                            effect='~Empty(r) & ~At(b, d) & On(b, r) & Hfull(r)'),
                        Action('Hload(r, b, b2, d)',
                            precond='At(r, d) & At(b, d) & IsRobot(r) & Hfull(r) & On(b2, r) & Addable(b, b2)',
                            effect='~Hfull(r) & ~At(b, d) & On(b, r) & Full(r)'),
                        Action('Funload(r, b, d)',
                            precond='At(r, d) & On(b, r) & IsRobot(r) & Full(r)',
                            effect='~On(b, r) & At(b, d) & Hfull(r) & ~Full(r)'),
                        Action('Hunload(r, b, d)',
                            precond='At(r, d) & On(b, r) & IsRobot(r) & Hfull(r)',
                            effect='~On(b, r) & At(b, d) & Empty(r) & ~Hfull(r)'),
                        Action('Move(r, s, e)',
                            precond='At(r, s) & IsRobot(r)',
                            effect='~At(r, s) & At(r, e)')
                            ])
    # END_YOUR_CODE

    return linearize(GraphPlan(planning_problem).execute())


def calculate_total_cost(plan):
    total_cost = 0
    
    for action in plan:
        # Get the action name and arguments
        action_name = action.op  # This will give the name of the action
        args = action.args         # This will give the list of arguments

        # Assign costs based on the action name and specific arguments
        if action_name == 'ELoad' or action_name == 'Hload' or action_name == 'Hunload' or action_name == 'Funload':
            total_cost += 1
        else:
            # Use args to identify start and end locations
            start, end = str(args[1]), str(args[2])  # args[0] is the robot, args[1] is the start, args[2] is the end
            if start == 'D1' and end == 'D2':
                total_cost += 3
            elif start == 'D2' and end == 'D3':
                total_cost += 5
            elif start == 'D1' and end == 'D3':
                total_cost += 10
            elif start == 'D2' and end == 'D1':
                total_cost += 3
            elif start == 'D3' and end == 'D2':
                total_cost += 5
            elif start == 'D3' and end == 'D1':
                total_cost += 10

    return total_cost

a = logisticsPlan()
print("Case4")
total_cost = calculate_total_cost(a)
print(f"Total Time Cost: {total_cost}")
print(a)