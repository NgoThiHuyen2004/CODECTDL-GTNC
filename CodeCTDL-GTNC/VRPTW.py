
import math

class Customer:
    def __init__(self, id, x, y, demand, ready, due, service):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready = ready
        self.due = due
        self.service = service

def distance(c1, c2):
    return math.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)

def can_visit(current, customer, current_time):
    travel = distance(current, customer)
    arrival = current_time + travel

    if arrival > customer.due:
        return False

    start_service = max(arrival, customer.ready)
    return start_service + customer.service

def solve_vrptw(customers, depot, capacity):

    unvisited = customers[:]
    routes = []

    while unvisited:

        route = [depot]
        load = 0
        time = 0
        current = depot

        while True:

            best_customer = None
            best_cost = float("inf")
            best_finish_time = None

            for c in unvisited:

                if load + c.demand > capacity:
                    continue

                result = can_visit(current, c, time)
                if result is False:
                    continue

                cost = distance(current, c)

                if cost < best_cost:
                    best_customer = c
                    best_cost = cost
                    best_finish_time = result

            if best_customer is None:
                break

            route.append(best_customer)
            load += best_customer.demand
            time = best_finish_time
            current = best_customer
            unvisited.remove(best_customer)

        route.append(depot)
        routes.append(route)

    return routes

depot = Customer(0, 50, 50, 0, 0, 999, 0)

customers = [
    Customer(1, 10, 10, 10, 0, 200, 10),
    Customer(2, 20, 40, 15, 10, 200, 10),
    Customer(3, 60, 20, 20, 30, 200, 10),
    Customer(4, 80, 80, 10, 50, 200, 10),
    Customer(5, 30, 70, 25, 20, 200, 10),
]

capacity = 50

routes = solve_vrptw(customers, depot, capacity)

for i, r in enumerate(routes):
    print(f"Route {i+1}: ", end="")
    for c in r:
        print(c.id, end=" -> ")
    print()
