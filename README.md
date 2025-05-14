# Bill & Coin Splitter

A Python CLI tool that helps you split a target dollar amount into bills and coins as evenly as possible.  
It uses a backtracking (DFS) algorithm to enumerate all valid combinations, then picks the one with the lowest standard deviation in usage counts (“most even” distribution).

---

## Table of Contents

1. [Features](#features)  
2. [Requirements](#requirements)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [How It Works](#how-it-works)  
   - [1. Backtracking to Enumerate Combinations](#1-backtracking-to-enumerate-combinations)  
   - [2. Measuring “Evenness” via Standard Deviation](#2-measuring-evenness-via-standard-deviation)  
   - [3. Filtering Denominations](#3-filtering-denominations)  
   - [4. Partitioning Bills vs. Coins](#4-partitioning-bills-vs-coins)  
6. [License](#license)  

---

## Features

- Prompt the user for quantities of each bill and coin denomination  
- Specify how many dollars to form with bills and with coins separately  
- Exclude certain denominations (e.g. \$100, \$50, \$2 bills or \$1 coin)  
- Find **all** valid combinations via DFS/backtracking  
- Compute standard deviation of usage counts and choose the “most even” solution  
- Display which bills and coins to use, plus any leftovers  

---

## Requirements

- Python 3.6+  
- No external dependencies  

---

## Installation

```bash
git clone https://github.com/fightforhash/CoinCalculator.git
```

## Usage

```bash
# On Windows:
python HMART.py

# On macOS / Linux:
python3 HMART.py
```

You will be prompted to:
- Enter quantities for each bill (\$100, \$50, \$20, \$10, \$5, \$2, \$1)
- Enter quantities for each coin (\$1, \$0.50, \$0.25, \$0.10, \$0.05, \$0.01)
- Specify how many dollars to form with bills (e.g., 190)
- Specify how many dollars to form with coins (e.g., 10)

The program then prints:
- Which bills to use and leftover bills
- Which coins to use and leftover coins
- Total leftover value

## How It Works

### 1. Backtracking to enumerate combinations
```python
def find_all_combinations(denom_list, index, target_cents, used_counts, solutions):
    if index == len(denom_list):
        if target_cents == 0:
            solutions.append(used_counts[:])
        return

    denom_cents, max_qty = denom_list[index]
    for count in range(max_qty + 1):
        cost = count * denom_cents
        if cost > target_cents:
            break
        used_counts[index] = count
        find_all_combinations(
            denom_list,
            index + 1,
            target_cents - cost,
            used_counts,
            solutions
        )
    used_counts[index] = 0
```
### 2. Measuring “Evenness” via Standard Deviation

```python
mean = sum(usage_counts) / len(usage_counts)
variance = sum((x - mean)**2 for x in usage_counts) / len(usage_counts)
std_dev = math.sqrt(variance)
```
The solution with the lowest std_dev is deemed most even.

### 3. Filtering Denominations

Before running the backtracking solver, you can remove any denominations you don’t want to consider by filtering your `bills` and `coins` dictionaries. 
For example, to exclude \$100, \$50 and \$2 bills, and the \$1 coin:

```python
    filtered_bills = {}
    for d, qty in bills.items():
        if d not in {100.0, 50.0, 2.0}:  
            filtered_bills[d] = qty
    
    filtered_coins = {}
    for d, qty in coins.items():
        if d != 1.0:  
            filtered_coins[d] = qty
```

### 4. Partitioning Bills vs. Coins
  
We solve two independent subproblems:

- Form BILL_TARGET dollars using filtered bills
- Form COIN_TARGET dollars using filtered coins
  
Each uses the same backtracking + standard-deviation logic, then we merge results.


## License

MIT License

Copyright (c) 2025 Thomas Ha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
