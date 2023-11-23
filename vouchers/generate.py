import sys
import json
import string
import random
credits = sys.argv[1]
count = sys.argv[2]


def generate_random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
with open('database/vouchers.json','r') as f:
    data = json.load(f)
if not credits in data:
    data[credits] = {
        "codes":[]
    }
for _ in range(int(count)):
    voucher = generate_random_string(32)
    data[credits]['codes'].append(voucher)
    print(f"Generated voucher: {voucher}")

with open('database/vouchers.json','w') as f:
    json.dump(data,f)