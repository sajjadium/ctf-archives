import json


def test_chain(links, start, end):
    current = start
    for link in links:
        current = int(''.join(
            str(int(current & component != 0))
            for component in link
        ), 2)
    return end == current & end


def main():
    try:
        with open('hyperlink.json', 'r') as f:
            data = json.load(f)
    except IOError:
        print('Could not open hyperlink.json')
        return

    print('Welcome to the chain building game.')
    print('Enter a chain and see if it works:')

    chain = input()

    legal_chars = set('abcdefghijklmnopqrstuvwxyz{}_')
    if any(c not in legal_chars for c in chain):
        print('Chain contains illegal characters!')
        return

    try:
        links = [data['links'][c] for c in chain]
        result = test_chain(links, data['start'], data['target'])
    except Exception:
        print('Something went wrong!')
        return

    if result:
        print('Chain works! Congratulations.')
    else:
        print('Oh no! Chain does not reach the target.')


if __name__ == '__main__':
    main()
