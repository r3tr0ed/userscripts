
import time
import random
import hashlib

def generate_id():
    # Get the current time in milliseconds
    current_time = int(time.time() * 1000)
    
    # Convert the current time to a hexadecimal string
    time_hex = hex(current_time)[2:]
    
    # Generate a random number and convert it to hexadecimal
    random_number = random.getrandbits(64)
    random_hex = hex(random_number)[2:]
    
    # Create a base ID using the time and random number
    base_id = time_hex[:6] + random_hex[:18]
    
    # Hash the base ID to ensure uniform length and format
    final_id = hashlib.sha1(base_id.encode()).hexdigest()[:24]
    
    return final_id

# Generate a few sample IDs
for _ in range(5):
    print(generate_id())
