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
So, by adding 4 to each character with CyberChef we can obtain from the input string `wBHC6,r/nh0ll/`[-1[_,,hy` the flag `{FLG:0v3rl4pp3d_15_c00l}`.
