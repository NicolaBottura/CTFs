# Don't Forget The Best Bits

The challenge provides us the following note:
```
# challenge title
Don't forget the best bits

# examples
Cleartext: message%3DFor%20a%20fullfilling%20experience%20embrace%20listen%20to%20new%20music%2E%20Pay%20attention%20to%20details%2C%20titles%20are%20important%2E%20And%20remember%2C%20music%20it%27s%20flipping%20amazing%26user%3Dmario

AES-CBC 128bit Ciphertext: 482c74deadaee362185c315aa10bcd02c96d2417fe3d1adf7fd90da2da95ca16ff9bb7b20b1ed3ac22c93bd3ac7f8d790768379407181f93bbc2c5bde5da5a4e47b400ed0827d815c47b4793349d894a557dd4436a7e2d7967b09faeff6b7037e5ba40202e850c0640414ffd651847bff2fe50ac248ac63cd595339b6fa9ee78f2835d29176d524ab9116894eab6ad5fd56c6600670d1f5bc4e48dfdaed740d1e3b3f1c05a067fbeb69e0a67226755569f185120d5b393131ecd3c209123994135a62d029cc5072264cd6ca306a7d1fc8a63ae9b9675ecace48745f049d5d742639e2df80675ad114938eb641a8b1704                                                                                                           
```

and also a code snippet regarding an AES CBC encryption/decryption:
```
import _aes

if request.method == 'POST':
        ct = request.form.get("ciphertext")
                pt = _aes.decrypt(ct)
                params = parse_qs(unquote(pt))
                message = ''.join(params['message'])
                user = ''.join(params['user'])
                if user == user_flag:
                        return make_response(flag,200)
                elif len(message) > 0:
                        return make_response("Thank you for your feedback!", 200)
```

Looking at the website provided, it seems like we need to forge a new encrypted message with the correct username in order to get the flag.

We can unquote the cleartext to make it readable without losing sight:
```
from urllib.parse import unquote

unquote('message%3DFor%20a%20fullfilling%20experience%20embrace%20listen%20to%20new%20music%2E%20Pay%20attention%20to%20details%2C%20titles%20are%20important%2E%20And%20remember%2C%20music%20it%27s%20flipping%20amazing%26user%3Dmario')
```

and the message we obtain is the following:
```
"message=For a fullfilling experience embrace listen to new music. Pay attention to details, titles are important. And remember, music it's flipping amazing&user=mario"
```

This means that the challenge title is fundamental to solve the challenge, maybe to obtain the correct username.
Googling for `Don't forget the best bits`, we can notice a song by Franz Ferdinand named `Billy goodbye`, so, `Billy` may be the correct name.

AES CBC mode XORs the previous block of ciphertext to next during decryption to forge a message.
So, to obtain the message with the correct user we can use the following script borrowed again from the winners of the challenge:
```
from pwn import *

d = unhex('482c74deadaee362185c315aa10bcd02c96d2417fe3d1adf7fd90da2da95ca16ff9bb7b20b1ed3ac22c93bd3ac7f8d790768379407181f93bbc2c5bde5da5a4e47b400ed0827d815c47b4793349d894a557dd4436a7e2d7967b09faeff6b7037e5ba40202e850c0640414ffd651847bff2fe50ac248ac63cd595339b6fa9ee78f2835d29176d524ab9116894eab6ad5fd56c6600670d1f5bc4e48dfdaed740d1e3b3f1c05a067fbeb69e0a67226755569f185120d5b393131ecd3c209123994135a62d029cc5072264cd6ca306a7d1fc8a63ae9b9675ecace48745f049d5d742639e2df80675ad114938eb641a8b1704')
d = bytearray(d)
d[-48:-32] = xor(d[-48:-32], xor('g%26user%3Dmario', b'g%26user%Dbilly'))
print(enhex(d))
```

and the message that we have to submit to the website is:
```
482c74deadaee362185c315aa10bcd02c96d2417fe3d1adf7fd90da2da95ca16ff9bb7b20b1ed3ac22c93bd3ac7f8d790768379407181f93bbc2c5bde5da5a4e47b400ed0827d815c47b4793349d894a557dd4436a7e2d7967b09faeff6b7037e5ba40202e850c0640414ffd651847bff2fe50ac248ac63cd595339b6fa9ee78f2835d29176d524ab9116894eab6ad5fd56c6600670d1f5bc4e48dfdaed740d1e3b3f1c05a067fbeb69e0a67226755569f185120d5b393131ecd3c209123994135a62d029cc5072264cd6cac0eb9d4ea8a63ae9b9675ecace48745f049d5d742639e2df80675ad114938eb641a8b1704
```

Flag: `{FLG:ju57_f3w_b17_7h47_m4k3_4ll_7h3_d1ff3r3nc3_:_3xp3r13nc3d_fl1pp3r}`.
