Title: re-encrypt .password-store using new gpg key
Category: Blog
Date: 2022-01-02
Tags: Komputer
Slug: reencrypt-password-store
Lang: en

I wanted to import my current password store into a new machine, and re-encrypt all passwords with a new gpg key. A
similar question was asked
[here](https://superuser.com/questions/1238892/how-to-re-encrypt-password-store-using-new-gpg-key). This is how I solved
it:

- on your new machine, create a new gpg key
    - `gpg --generate-key`
- to decrypt the current pass db, you need the old gpg key
- go to your old machine and run
    - `gpg --export KEY_ID > gpg_public.key`
    - `gpg --export-secret-keys KEY_ID > gpg_private.key`
- copy both files to your new machine and import them
    - `gpg --import gpg_public.key`
    - `gpg --import gpg_private.key`
- copy the remote password store to your new machine, f.e. by
    - `git clone $REMOTE:.password-store`
- you might want to get rid of your old git history
    - `rm -rf .password-store/.git`
- now you can re-encrypt all passwords with your new gpg key
    - `pass init NEW_KEY_ID`
    - you have to type the password of your old gpg key to decrypt all passwords in the database
- I also like to make the password store a git repo
    - `pass git init`

That's it.
