arr01 = [1]
arr02 = [1, 0, 1]
arr03 = [0, 0, 0, 0, 0, 0, 0, 1]
arr04 = [1, 0, 0, 0, 0, 0, 0, 0]

arr05 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
arr06 = [11,12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
arr07 = [27, 28]
arr08 = [29, 30, 31]
arr09 = [32]


last = []
def shit(lista):
    global last
    print("Received: ", lista, " ;last: ", last)
    lista = [str(i) for i in lista]
    temp_l = len(last)
    temp_last = last + lista[0: 8 - temp_l]
    control = 0
    if len(temp_last) == 8:
        print("temp_l ", temp_last)
        control = 8 - temp_l
        last = []
    print("lenList: ", len(lista), " ; control: ", control)
    while len(lista) - control > 8:
        # print("Control: ", control)
        print("temp_l2 ", "".join(lista[control: (control + 8)]))
        control += 8

    print("Control2: ", control)
    if len(last) == 8:
        print("temp_l3 ", "".join(lista[control:]))
    last = last + lista[control:]
    print("----")

shit(arr05)
shit(arr06)
shit(arr07)
shit(arr08)
shit(arr09)
