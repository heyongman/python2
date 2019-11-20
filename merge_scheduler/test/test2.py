import logging
import json


def main():
    log = logging.getLogger('root')
    log.info('test2 info')
    # with open('./test.json', 'w') as f:
    #     f.write(json.dumps([{'a': 1}]))

    with open('./appids.json', 'r') as f:
        res = json.load(f)

    for dic in res:
        print dic['app_id']


def test1():
    dic = {}
    dic['a'] = dic.get(None)
    print dic


if __name__ == '__main__':
    main()
