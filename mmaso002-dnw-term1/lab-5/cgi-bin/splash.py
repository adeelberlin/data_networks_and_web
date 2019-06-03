#!/usr/bin/env python3

import random

images = ["image_1","image_2","image_3","image_4"]

i = random.randint(0,len(images)-1)

print("Content-Type: text/html\n")
print("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Hello Caflucks</title>
</head>
<body>
<h1>Welcome to Catflucks</h1>
<p>You are viewing {}</p>
</body>
</html>""".format(images[i]))
