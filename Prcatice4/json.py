import json
with open('lab 4/JSON/sample-data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
dn = [item['l1PhysIf']['attributes']['dn'] for item in data['imdata']]
speed = [item['l1PhysIf']['attributes']['speed'] for item in data['imdata']]
mtu = [item['l1PhysIf']['attributes']['mtu'] for item in data['imdata']]
print('''Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------''')
for d, s, m in zip(dn, speed, mtu):
    print(f"{d:<71} {s:<9} {m:<10}")