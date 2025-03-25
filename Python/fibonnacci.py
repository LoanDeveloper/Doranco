import time

max_value = int(input("Entrez un nombre: "))

nombres = [i for i in range(max_value)]

# Mesurer le temps de création des structures
start_time = time.time()
list_fibo = []
for i in range(max_value):
    if i == 0:
        list_fibo.append(0)
    elif i == 1:
        list_fibo.append(1)
    else:
        list_fibo.append(list_fibo[i-1] + list_fibo[i-2])
list_time = time.time() - start_time

start_time = time.time()
tuple_fibo = ()
for i in range(max_value):
    if i == 0:
        tuple_fibo += (0,)
    elif i == 1:
        tuple_fibo += (1,)
    else:
        tuple_fibo += (tuple_fibo[i-1] + tuple_fibo[i-2],)
tuple_time = time.time() - start_time

start_time = time.time()
dict_fibo = {}
for i in range(max_value):
    if i == 0:
        dict_fibo[i] = 0
    elif i == 1:
        dict_fibo[i] = 1
    else:
        dict_fibo[i] = dict_fibo[i-1] + dict_fibo[i-2]
dict_time = time.time() - start_time

start_time = time.time()
set_fibo = set()
a, b = 0, 1
for i in range(max_value):
    set_fibo.add(a)
    a, b = b, a + b
set_time = time.time() - start_time

# Mesurer le temps d'accès
start_time = time.time()
_ = list_fibo[max_value // 2]
list_access_time = time.time() - start_time

start_time = time.time()
_ = tuple_fibo[max_value // 2]
tuple_access_time = time.time() - start_time

start_time = time.time()
_ = dict_fibo[max_value // 2]
dict_access_time = time.time() - start_time

start_time = time.time()
_ = max_value in set_fibo
set_access_time = time.time() - start_time

# Résultats
print(f"Temps de création :\n  - List: {list_time:.6f}s\n  - Tuple: {tuple_time:.6f}s\n  - Dict: {dict_time:.6f}s\n  - Set: {set_time:.6f}s")
print(f"Temps d'accès :\n  - List: {list_access_time:.6f}s\n  - Tuple: {tuple_access_time:.6f}s\n  - Dict: {dict_access_time:.6f}s\n  - Set: {set_access_time:.6f}s")
