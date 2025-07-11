import json

with open("users.txt", "r") as file:
    content = file.read()
    content = json.loads(content)
    print(content)

with open("users.txt", "w") as file:
    file.write(content)
