# Catflucks Application 

Here is a newer version of catflucks with added login feature. It is only partially implemented, but enough to give you the general idea of how to perform password checking on hashed passwords.

+ To login, you need to create an account **from the mongo shell** first, for which you know the unhashed password!
+ For testing purposes, here is an account to insert, which has the password, \`**password'**:

		db.accounts.insertOne({
		... "joined": new Date(),
		... "username":"tester",
		... "name":{"last":"Harriet","first":"Sorrel"},
		... "password":"$2b$12$DXvBoOurVX7GnCr35P.iZ.DG2cH.qQarJL7m9xhhRvrqkDsE1/aFC",
		... "is_admin":1,
		... "email":"sharr003@gold.ac.uk"
		... })

+ You can change the name and email etc, but don't change the password!

