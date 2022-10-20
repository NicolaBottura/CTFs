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
