import math

def get_bill_target():
    """
    Ask the user how many dollars should come from bills.
    사용자로부터 '지폐'로 구성할 금액을 입력받습니다.
    """
    target_str = input("\nHow many dollars do you want to form using bills? (e.g., 190): ")
    return float(target_str)

def get_coin_target():
    """
    Ask the user how many dollars should come from coins.
    사용자로부터 '동전'으로 구성할 금액을 입력받습니다.
    """
    target_str = input("How many dollars do you want to form using coins? (e.g., 10): ")
    return float(target_str)

def get_bills_from_user():
    """
    Asks the user to input quantities of various bill denominations.
    {denomination_float: quantity_int}.
    사용자로부터 각 지폐 단위의 개수를 입력받습니다.
    반환값: {지폐_단위_float: 개수_int}.
    """
    bills = {}
    bill_denominations = [100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.0]
    
    print("Bills :")
    for denom in bill_denominations:
        qty_str = input(f"Enter quantity for ${denom:.2f}: ")
        quantity = int(qty_str)
        bills[denom] = quantity
    
    return bills

def get_coins_from_user():
    """
    Asks the user to input quantities of various coin denominations.
    {denomination_float: quantity_int}.
    사용자로부터 각 동전 단위의 개수를 입력받습니다.
    반환값: {동전_단위_float: 개수_int}.
    """
    coins = {}
    coin_denominations = [1.0, 0.50, 0.25, 0.10, 0.05, 0.01]
    
    print("\nCoins :")
    for denom in coin_denominations:
        qty_str = input(f"Enter quantity for ${denom:.2f}: ")
        quantity = int(qty_str)
        coins[denom] = quantity

    return coins

def find_all_combinations(denom_list, index, target_cents, used_counts, solutions):
    """
    Backtracking to find all ways to reach target_cents using given denominations.
    깊이 우선 탐색(DFS)과 백트래킹을 사용하여 주어진 단위를 통해 사용자가 정한 동전의 총합을 달성하는 모든 조합을 찾습니다.
    """
    if index == len(denom_list):
        if target_cents == 0:
            # 조합을 찾은경우
            solutions.append(used_counts[:])
        return
    
    denom_cents, max_qty = denom_list[index]
    
    # 현재단위에 대해 0에서 최대개수 까지 시도
    for count in range(max_qty + 1):
        cost = count * denom_cents
        if cost > target_cents:
            break
        used_counts[index] = count
        find_all_combinations(denom_list, index + 1, target_cents - cost, used_counts, solutions)
    
    # 백트래킹 반환 전 초기화
    used_counts[index] = 0

def most_even_solution(target_amount, denominations):
    """
    Return the usage of each denom that sums to target_amount,
    with minimal standard deviation in usage counts.
    주어진 target_amount를 달성하는 가장 균등한 조합을 표준편차를 이용하여 반환합니다.
    denominations: {denom_float: quantity_int} (e.g., {50.0: 2, 20.0: 3, ...})
    """

    # 단위와 개수를 (센트, 최대 개수) 형식의 리스트로 변환, 최대 개수가 0인 단위는 제외
    denom_list = [(int(round(d * 100)), q) for (d, q) in denominations.items() if q > 0]
    
    target_cents = int(round(target_amount * 100))
    
    # 백트래킹을 통해 모든 조합 찾기
    solutions = []
    used_counts = [0] * len(denom_list)
    find_all_combinations(denom_list, 0, target_cents, used_counts, solutions)
    
    if not solutions:
        return None
    
    # 유효한 조합 중 표준편차가 가장 작은 조합이 우선순위
    best_solution = None
    best_std = float('inf')
    for usage_counts in solutions:
        mean = sum(usage_counts) / len(usage_counts)
        variance = sum((x - mean)**2 for x in usage_counts) / len(usage_counts)
        std_dev = math.sqrt(variance)
        if std_dev < best_std:
            best_std = std_dev
            best_solution = usage_counts[:]
    
    # best_solution 형태변환 후 최종 결과 반환
    result = {}
    for i, (cents, _) in enumerate(denom_list):
        count = best_solution[i]
        if count > 0:
            denom_float = cents / 100.0
            result[denom_float] = count
    
    return result

def main():
    # 1) 사용자에게 입력받습니다
    bills = get_bills_from_user()
    coins = get_coins_from_user()
    
    # 나누고 싶은 액수를 정합니다
    BILL_TARGET = get_bill_target()
    COIN_TARGET = get_coin_target()
    
    # 나눈 돈에는 100달러, 50달러, 2달러, 동전 1달러는 포함시키지 않는 로직
    filtered_bills = {}
    for d, qty in bills.items():
        if d not in {100.0, 50.0, 2.0}:  
            filtered_bills[d] = qty
    
    filtered_coins = {}
    for d, qty in coins.items():
        if d != 1.0:  
            filtered_coins[d] = qty
    
    # 2) 사용자가 설정한 지폐양을 달성하기 위한 지폐의 가장 균등한 조합을 찾습니다
    bill_solution = most_even_solution(BILL_TARGET, filtered_bills)
    if bill_solution is None:
        print(f"\nNo way to form ${BILL_TARGET} with your allowed bills.\n")
        return
    
    # 3) 사용자가 설정한 동전양을 달성하기 위한 동전의 가장 균등한 조합을 찾습니다
    coin_solution = most_even_solution(COIN_TARGET, filtered_coins)
    if coin_solution is None:
        print(f"\nNo way to form ${COIN_TARGET} with your allowed coins.\n")
        return
    
    # 조합 출력
    print(f"\nBILLS used to reach ${BILL_TARGET} (excluding $100 & $50 & $2):")
    for d in sorted(bill_solution.keys(), reverse=True):
        print(f"  ${d:.2f}: {bill_solution[d]}")
    
    print(f"\nCOINS used to reach ${COIN_TARGET} (excluding $1):")
    for d in sorted(coin_solution.keys(), reverse=True):
        print(f"  ${d:.2f}: {coin_solution[d]}")
    
    # 4) 남은 지폐 출력
    leftover_bills = {}
    for d, total_qty in bills.items():
        # 사용자가 선택한 지폐가 filtered_bills에 포함이 안되어있으면 사용되지 않은 지폐
        used_qty = bill_solution.get(d, 0) if d in bill_solution else 0
        leftover_bills[d] = total_qty - used_qty
    
    # 5) 남은 동전 출력
    leftover_coins = {}
    for d, total_qty in coins.items():
        used_qty = coin_solution.get(d, 0) if d in coin_solution else 0
        leftover_coins[d] = total_qty - used_qty
    
    # 6) 남은 총 가치 계산
    leftover_bills_value = sum(d * leftover_bills[d] for d in leftover_bills)
    leftover_coins_value = sum(d * leftover_coins[d] for d in leftover_coins)
    leftover_total = leftover_bills_value + leftover_coins_value
    
    print(f"\nLeftover bills (including $100 & 50 & $2 not used at all):")
    for d in sorted(leftover_bills.keys(), reverse=True):
        if leftover_bills[d] > 0:
            print(f"  ${d:.2f}: {leftover_bills[d]}")
    
    print("\nLeftover coins (including $1 not used at all):")
    for d in sorted(leftover_coins.keys(), reverse=True):
        if leftover_coins[d] > 0:
            print(f"  ${d:.2f}: {leftover_coins[d]}")
    
    print(f"\nTotal leftover value: ${leftover_total:.2f}")
    print("\nDone!") #돈게산이 끝났다는 메시지

if __name__ == '__main__':
    main()
