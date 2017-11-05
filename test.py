import requests
import sys
import time

if len(sys.argv) > 1:
    if sys.argv[1] == 'local':
        NODE = 'http://localhost:5000'
    else:
        print('Please specify endpoint')
else:
    NODE = 'https://411d4537.ngrok.io'

KEYS = {
    0: {
        'public': '043ca613e39568764fb7ad50cfcd5b3e4aaa7b9118882fb2a55d6152bf96fbf9dd78a6d7d61e61538325716267dc1fcec3efbc2347ae35a7a3605ab488f89245cc',
        'private': '138eb6808f343f53b192636aaf20d771742b1fc007ddf37f00f1e2c01e78c836'
    },
    1: {
        'public': '04ea339a161ebbb283fdf65e770addf8e0342514380e2e590996dc05684ea827738d20a41ce7d9d4d256b9f81c8d5014da87022478e226299c34c3a947edd6c905',
        'private': 'f7abfa34bdd2294d42eaf135ce5c73828d792579caf09d4501e675c9ee949091'
    }
}

def mine():
    print('Mining...')
    # Mine my own chain
    requests.get('{}/mine'.format(NODE))
    # Check other chain
    requests.get('http://416866a5.ngrok.io/chain')
    time.sleep(2)

def register_node(nodes):
    data = {'nodes': nodes}
    requests.get('{}/nodes/reset'.format(NODE))
    r = requests.post('{}/nodes/register'.format(NODE), json=data)
    print(r.json())

def new_transaction(sender, recipient, amount):
    data = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    r = requests.post('{}/transactions/new'.format(NODE), json=data)
    print(r.json())
    return r.json()

def get_balance(address):
    data = {
        'address': address
    }
    r = requests.get('{}/address/balance'.format(NODE), json=data)
    if r.ok:
        print(r.json())
        return r.json()

def consensus():
    r = requests.get('{}/nodes/resolve'.format(NODE))
    if r.ok:
        return r.json()

def main():
    sender = KEYS[0]['public']
    recipient = KEYS[1]['public']
    new_transaction(sender, recipient, 10)
    get_balance(recipient)
    [mine() for _ in range(3)]
    consensus()

if __name__ == '__main__':
    register_node([
        'http://6c7892c2.ngrok.io/',
    ])

    while 1:
        main()
