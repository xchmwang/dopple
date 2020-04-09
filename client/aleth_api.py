
import argparse
import json
import string

import util


class aleth_api:

    def __init__(self):
        self.header_get = 'Accept: application/json'
        self.header_post = 'Content-Type: application/json'
        self.host = 'localhost:8111'


    def eth_blockNumber(self):
        method = 'eth_blockNumber'
        d = {
                'method': method,
                'params': [],
                'id': 1,
                'jsonrpc': '2.0'
                }
        cmd = '''curl -s --data '%s' -H %s -X POST %s''' % (json.dumps(d), self.header_post, self.host)
        ret = util.run_cmd(cmd)
        return ret


    def eth_getBalance(self, address, height):
        assert isinstance(address, str)
        assert isinstance(height, int)
        if not height:
            ret = self.eth_blockNumber()
            data = json.loads(ret)
            height = int(data['result'],16)

        method = 'eth_getBalance'
        d = {
                'method': method,
                'params': [address, hex(height)],
                'id': 1,
                'jsonrpc': '2.0'
                }
        cmd = '''curl -s --data '%s' -H %s -X POST %s''' % (json.dumps(d), self.header_post, self.host)
        ret = util.run_cmd(cmd)
        return ret


    def eth_sendTransaction(self, source, target, value, data, filename):
        assert isinstance(source, str)
        assert isinstance(target, str)
        assert isinstance(value, str)
        assert isinstance(data, str)
        data = util.read_file(filename) if filename else data
        assert all(ch in string.hexdigits for ch in data)
        method = 'eth_sendTransaction'
        d = {
                'method': method,
                'params': [{
                    'from': source,
                    'to': target,
                    'value': value,
                    'gas': '0xfffff',
                    'data': data
                    }],
                'id': 1,
                'jsonrpc': '2.0'
                }
        cmd = '''curl -s --data '%s' -H %s -X POST %s''' % (json.dumps(d), self.header_post, self.host)
        ret = util.run_cmd(cmd)
        return ret


    def eth_getTransactionByHash(self, txhash):
        assert isinstance(txhash, str)
        method = 'eth_getTransactionByHash'
        d = {
                'method': method,
                'params': [txhash],
                'id': 1,
                'jsonrpc': '2.0'
                }
        cmd = '''curl -s --data '%s' -H %s -X POST %s''' % (json.dumps(d), self.header_post, self.host)
        ret = util.run_cmd(cmd)
        return ret


def parse_args():
    parser = argparse.ArgumentParser(description='aleth rpc api',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--method', type=str, default='eth_blockNumber', help='aleth rpc method')

    parser.add_argument('--address', type=str, help='ethereum address')
    parser.add_argument('--height', type=int, default=1, help='block height')

    parser.add_argument('--source', type=str, help='transaction address send from')
    parser.add_argument('--target', type=str, help='transaction address send to')
    parser.add_argument('--value', type=str, help='transaction value')
    parser.add_argument('--data', type=str, help='transaction payload')
    parser.add_argument('--filename', type=str, help='transaction payload in file')

    parser.add_argument('--txhash', type=str, help='transaction hash')
    args = parser.parse_args()
    return args


def wrapper_eth_sendTransaction(params):
    api = aleth_api()
    ret = api.eth_sendTransaction(params.source, params.target, params.value, params.data, params.filename)
    print(ret)
    return ret


def gen_transactions(params):
    t = util.repeat_timer(0.5, wrapper_eth_sendTransaction, [params])
    t.start()


def main():
    args = parse_args()
    op_code = {
            'eth_blockNumber': 'aleth_api().eth_blockNumber()',
            'eth_getBalance': 'aleth_api().eth_getBalance(args.address, args.height)',
            'eth_sendTransaction': 'aleth_api().eth_sendTransaction(args.source, args.target, args.value, args.data, args.filename)',
            'eth_getTransactionByHash': 'aleth_api().eth_getTransactionByHash(args.txhash)',
            'gen_transactions': 'gen_transactions(args)'
            }
    ret = eval(op_code[args.method])
    print(ret)


if __name__ == '__main__':
    main()
