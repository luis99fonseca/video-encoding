import numpy as np

# ola = np.array([1,2,3,4,5,6]).reshape(2, 3)
# print(ola.shape())
# print("array: \n", ola)
# print("shape: ", ola.shape)
# print("repeat:\n ", ola.repeat(2, 1))
# print("array2: \n", ola)

file01 = open("ola.txt", "wb")
file01.write("adeus".encode("utf-8"))
file01.close()