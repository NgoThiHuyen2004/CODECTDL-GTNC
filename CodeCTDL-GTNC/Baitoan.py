
import random
import math
import copy
import time
import pandas as pd
import matplotlib.pyplot as plt

# TẠO DỮ LIỆU (VRPTW)
def generate_data(n):
    customers = []

    for i in range(n):
        customers.append({
            "id": i,                     # ID khách hàng
            "x": random.randint(0, 100), # tọa độ X
            "y": random.randint(0, 100), # tọa độ Y
            "demand": random.randint(1, 10),  # nhu cầu
            "e": random.randint(0, 50),  # thời gian sớm
            "l": random.randint(50, 100),# thời gian muộn
            "service": random.randint(1, 5) # thời gian phục vụ
        })

    depot = {"x": 50, "y": 50}  # kho trung tâm
    return depot, customers


# KHOẢNG CÁCH
def dist(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


# TÍNH CHI PHÍ (VRPTW)
def cost(solution, depot):
    total = 0

    for route in solution:  # mỗi route = 1 xe
        prev = depot

        for cust in route:
            total += dist(prev, cust)
            prev = cust

        total += dist(prev, depot)

    return total


# KIỂM TRA RÀNG BUỘC VRPTW
def check_route(route, depot, capacity):
    load = 0
    time_now = 0
    prev = depot

    for cust in route:
        # kiểm tra tải trọng
        load += cust["demand"]
        if load > capacity:
            return False

        # di chuyển
        time_now += dist(prev, cust)

        # đảm bảo time window
        time_now = max(time_now, cust["e"])

        if time_now > cust["l"]:
            return False

        # thời gian phục vụ
        time_now += cust["service"]

        prev = cust

    return True


# DESTROY (ALNS)
def destroy(solution, remove_count):
    solution = copy.deepcopy(solution)
    removed = []

    for _ in range(remove_count):
        route = random.choice(solution)
        if route:
            cust = random.choice(route)
            route.remove(cust)
            removed.append(cust)

    return solution, removed


# REPAIR (ALNS)
def repair(solution, removed, depot, capacity):

    for cust in removed:
        best_position = None
        best_cost = float("inf")

        for route in solution:
            for i in range(len(route) + 1):

                temp = route[:i] + [cust] + route[i:]

                if check_route(temp, depot, capacity):
                    new_cost = cost([temp], depot)

                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_position = (route, i)

        # nếu tìm được vị trí tốt
        if best_position:
            best_position[0].insert(best_position[1], cust)
        else:
            solution.append([cust])  # tạo route mới

    return solution


# ALNS MAIN
def alns(customers, depot, capacity, iterations=300):

    # khởi tạo: mỗi khách 1 xe
    solution = [[c] for c in customers]

    best_solution = copy.deepcopy(solution)
    best_cost = cost(solution, depot)

    T = 100  # nhiệt độ ban đầu

    for _ in range(iterations):

        current = copy.deepcopy(solution)

        # phá nghiệm
        current, removed = destroy(current, max(1, len(customers)//5))

        # sửa nghiệm
        current = repair(current, removed, depot, capacity)

        current_cost = cost(current, depot)

        # Simulated Annealing
        if current_cost < best_cost or random.random() < math.exp((best_cost - current_cost)/T):
            solution = current

        if current_cost < best_cost:
            best_solution = copy.deepcopy(current)
            best_cost = current_cost

        T *= 0.995

    return best_solution, best_cost


# VẼ TUYẾN ĐƯỜNG
def plot_routes(solution, depot, title):

    plt.figure()

    for route in solution:
        x = [depot["x"]]
        y = [depot["y"]]

        for cust in route:
            x.append(cust["x"])  # khách hàng
            y.append(cust["y"])

        x.append(depot["x"])
        y.append(depot["y"])

        plt.plot(x, y, marker='o')  # đường đi

    plt.scatter(depot["x"], depot["y"], marker='s')  # depot
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


# THỰC NGHIỆM
def run_experiment():

    results = []

    for N in [10, 30, 50, 80, 100]:

        print(f"\nĐang chạy N = {N}...")

        depot, customers = generate_data(N)

        start = time.time()
        solution, total_cost_val = alns(customers, depot, capacity=30)
        end = time.time()

        results.append({
            "So_khach": N,
            "Chi_phi": round(total_cost_val, 2),
            "Thoi_gian": round(end - start, 4),
            "So_tuyen": len(solution)
        })

        # vẽ hình cho báo cáo
        if N in [10, 50, 100]:
            plot_routes(solution, depot, f"ALNS giải VRPTW (N={N})")

    df = pd.DataFrame(results)

    print("\n===== KẾT QUẢ THỰC NGHIỆM =====")
    print(df)

    # biểu đồ
    plt.figure()
    plt.plot(df["So_khach"], df["Chi_phi"], marker='o')
    plt.xlabel("Số khách hàng")
    plt.ylabel("Chi phí")
    plt.title("Chi phí theo số khách (ALNS - VRPTW)")
    plt.grid()
    plt.show()


# RUN
if __name__ == "__main__":
    run_experiment()