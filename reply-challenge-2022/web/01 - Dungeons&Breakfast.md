# Dungeons & Breakfast

After clicking the door, we are presented with different functionalities, among them there is the `register` button that we can click in order to register an account and then log in.
After the loging, we can see that in the `Profile` page we can change password.
In the source page of `Main Menu` we can see an interesting variable:

![image](https://user-images.githubusercontent.com/32301476/196949860-1ca05c4e-162c-4ad9-ac52-3642645ccbe3.png)

which looks like the email of the master user.

Since the change password functionality requires an email address, we can try to modify the password of the master user now that we have its email address by abusing a IDOR vulnerability.
So we need to use the email found, our password as the old one (guessing the the backend code might be checking against the logged in user's password but not that the email matches) and a new password of our choice.
Now we can log in as user master!

In the Master portal looks like we can include files (LFI), trying with something like /etc/passwd we are redirected to `/troll` and in the source code we can notice the following comment:
```
<!-- TODO: review all the /secret notes and make them accessible. See: https://pastebin.com/TJMXHEB9 -->
```

Checking the link, we get a portion of the backend code:
```
@app.route('/admin', methods=["GET","POST"])
@login_required
def admin():
    if current_user.is_authenticated and current_user.is_admin:
        notes = ['campaign.txt', 'player1.txt', 'player2.txt']
 
 
        selected_note = 'campaign.txt'
        if request.method == 'POST' and request.form.get('note'):
            selected_note = request.form.get('note')
 
        path = os.path.join('notes', selected_note)
        path = remove_dot_slash_recursive(path)
        if allowed_path(path):
            try:
                file = open(path, 'r')
                note_content = file.readlines()
            except Exception as e:
                note_content = ['This note does not exist\n']   
 
            return render_template('admin.html', notes=notes, note_content=note_content, selected_note=selected_note)
        return redirect('troll')
    else:
        return 'You are not the master!:('
```

So, the `../` is stripped first thanks to `remove_dot_slash_recursive()` function, which means that a full LFI is not possible, but we can escape the `notes` directory by abusing the fact that `os.path.join` will generate absolute paths if the second paramter starts with a `/`, which means that we can use the `/secret` directorty that is mentioned in the comment above.
Guessing the file that contains the flag, we can do the following in Burp:

![image](https://user-images.githubusercontent.com/32301476/196957786-9d922a4a-a2d4-4907-ab24-f2c3b529be6d.png)

to get the flag:

![image](https://user-images.githubusercontent.com/32301476/196957844-1203e966-66f0-4900-863e-3435fb7b03ed.png)

