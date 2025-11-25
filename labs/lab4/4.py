chislo = input()
if int(chislo[-1])%2 == 0 and sum(int (x)for x in chislo)%3==0:
    print("делится")
else:
    print("не делится")
