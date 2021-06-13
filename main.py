transactions = []  # to store all valid transaction id, weight and fees
parent = set()
MAX_WEIGHT = 40_00_000
# cleaning the csv file, remove all invalid transactions whose parent transaction id is coming before transaction
with open('mempool.csv') as file:
    for line in file:
        txid, fee, weight, *parent_txids = line.strip().split(',')
        if parent_txids[0]:
            for parent_txid in parent_txids:
                if parent_txid not in parent:
                    break
            else:
                for parent_txid in parent_txids:
                    parent.add(txid)
                transactions.append((txid, int(weight), int(fee)))
        else:
            transactions.append((txid, int(weight), int(fee)))
            parent.add(txid)

n = len(transactions)
transactions.sort(key=(lambda x: (x[2]/x[1])), reverse=True)  # sorting on the basis of max fees per weights
total_weight = 0
total_fees = 0
with open('block.txt', 'w') as f:
    for transaction in transactions:
        total_weight += transaction[1]
        if total_weight <= MAX_WEIGHT:
            total_fees += transaction[2]
            f.write(transaction[0] + '\n')
        elif total_weight > MAX_WEIGHT:
            total_weight -= transaction[1]
        else:
            break

