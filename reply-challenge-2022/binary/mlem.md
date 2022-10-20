# Mlem

```
   _____ __    _____ _____
  |     |  |  |   __|     |
  | | | |  |__|   __| | | |
  |_|_|_|_____|_____|_|_|_|
  v1.0 - Poeta Errante


  ,-.       _,---._ __  / \
 /  )    .-'       `./ /   \
(  (   ,'            `/    /|
 \  `-"             \'\   / |
  `.              ,  \ \ /  |
   /`.          ,'-`----Y   |
  (            ;        |   '
  |  ,-.    ,-'         |  /
  |  | (   |            | /
  )  |  \  `.___________|/
  `--'   `--'
```

After decompiling the binary with Ghidra, we can see that it asks for a word, make a lot of comparisons between each character of the input (that needs to be of 24 chars) and then it will print `Word found! But it\'s not the flag. Awww :3`, otherwise, if one of the checks is wrong it will print `Maybe you should search for a different length word! Meeoww`.

These are all the comparisons, where we need to solve some simple equations and then convert from decimal to ascii the result:

![image](https://user-images.githubusercontent.com/32301476/196969648-23700899-d9ed-4af8-b9c8-7fb0a8c41261.png)

We can notice that afer printing the message regarding a successfull result, it will loop for each character of the input string and passing it to a function:

![image](https://user-images.githubusercontent.com/32301476/196969883-bfa6f3ee-a1c9-4725-8bce-fd2db34b5b9a.png)

In Ghidra the content of suck function is empty, so I opened it with Ida to check what it does to each character and essentially, the operation is a `+4` to each character of the input string (obv in hex), `add al, 4`.
So, by adding 4 to each character with CyberChef we can obtain from the input string ``wBHC6,r/nh0ll/`[-1[_,,hy`` the flag `{FLG:0v3rl4pp3d_15_c00l}`.

## Note
To solve all the checks, we could also use `z3` and write a script in python to solve it like the following:
```
from z3 import *

s = Solver()
passw = []

for i in range(24):
   passw.append(Int(str(i)))
   s.add(passw[i]<128)
   s.add(passw[15] == 91)
   s.add(passw[18] == 91)
   s.add(passw[0] + passw[0] + 11 == passw[0] + 130)
   s.add(passw[23] + passw[23] + 6 == passw[23] + 127)
   s.add(7 * passw[1] == passw[1] + 396)
   s.add(passw[22] == 104)
   s.add(3 * (passw[2] + 2) - 2 == 4 * (passw[2] - 17))
   s.add(passw[21] == passw[21] + passw[21] - 44)
   s.add(passw[3] == 67)
   s.add(3 * (3 * passw[20] - 2) - 4 * (passw[20] * 5 + 2) == -8 * passw[20] -
   146)
   s.add((5 * passw[4] - 2) * 5 - (passw[4] + passw[4] + 7) * 6 == 33 *
   passw[4] - 1132)
   s.add(passw[19] == passw[3] + passw[20] - 16)
   s.add((passw[5] + passw[5]) == (passw[5] + 44))
   s.add(passw[17] == 49)
   s.add(passw[6] == 114)
   s.add(- passw[16] == (36 - passw[16])*5)
   s.add(passw[7] == 47)
   s.add(passw[14] * 2 == passw[14] + 48*2)
   s.add(passw[8] == 110)
   s.add(passw[13]*2 == passw[14] - 2)
   s.add(passw[9] == 104)
   s.add(passw[12] == passw[11])
   s.add(passw[11] == 108)
   s.add(passw[10] == 48 )

print(s.check())
for p in passw:
   print(chr(s.model()[p].as_long()), end="")
```
