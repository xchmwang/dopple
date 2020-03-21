
import json
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


def parse_args():
    parser = argparse.ArgumentParser(description='aleth rpc api',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--method', type=str, default='eth_blockNumber', help='aleth rpc method')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    op_code = {
            'eth_blockNumber': 'aleth_api().eth_blockNumber()'
            }
    ret = eval(op_code[args.method])
    print(ret)


if __name__ == '__main__':
    main()
