import csv
import json

with open ("users.txt", "r") as file:
    content = file.read()
    #replace single quote and newlines 
    content = content.strip().replace("\n", ",").replace("'", '"')
    content = f"[{content}]"


content = json.loads(content)

for i in content:
    print(i)


output_filename = "output.csv"
with open(output_filename, "w", newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['name', 'url', 'username', 'password', 'note'])

    # Write data to CSV
    for user_data in content:
        name = 'www.unhinged.ai'
        url = 'https://www.unhinged.ai/signup'
        username = user_data.get('email', '')
        password = user_data.get('password', '')
        note = ''

        csv_writer.writerow([name, url, username, password, note])   
