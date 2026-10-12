import argparse
import sys
from pathlib import Path


ENCODING = 'cp1251'


def read_text(name):
    return Path(name).read_text(encoding='utf-8')


def read_hex(name):
    value = bytes.fromhex(read_text(name))
    if not value:
        raise ValueError('HEX-файл пуст')
    return value


def to_bytes(value):
    result = value.encode(ENCODING)
    if not result:
        raise ValueError('Текст пуст')
    return result


def xor_equal(left, right):
    if len(left) != len(right):
        raise ValueError('Длины не совпадают: {} и {} байт'.format(len(left), len(right)))
    if not left:
        raise ValueError('Пустые данные')
    return bytes(a ^ b for a, b in zip(left, right))


def hex_line(value):
    return ' '.join('{:02X}'.format(item) for item in value)


def save_text(name, value):
    with open(name, 'x', encoding='utf-8') as stream:
        stream.write(value)


def save_hex(name, value):
    save_text(name, hex_line(value) + '\n')


def build_parser():
    parser = argparse.ArgumentParser(description='ЛР 8: повторное применение XOR-гаммы')
    commands = parser.add_subparsers(dest='mode', required=True)
    encrypt = commands.add_parser('encrypt', help='Шифрование с известным ключом')
    encrypt.add_argument('--text-file', required=True)
    encrypt.add_argument('--key-file', required=True)
    encrypt.add_argument('--out', required=True)
    decrypt = commands.add_parser('decrypt', help='Расшифрование с известным ключом')
    decrypt.add_argument('--cipher-file', required=True)
    decrypt.add_argument('--key-file', required=True)
    decrypt.add_argument('--out', required=True)
    mixed = commands.add_parser('xor', help='C1 XOR C2 без ключа')
    recover = commands.add_parser('recover', help='Другой текст по известному фрагменту')
    table = commands.add_parser('table', help='Таблица равенства C1 XOR C2 = P1 XOR P2')
    for command in (mixed, recover, table):
        command.add_argument('--c1-file', required=True)
        command.add_argument('--c2-file', required=True)
        command.add_argument('--out', required=True)
    known = recover.add_mutually_exclusive_group(required=True)
    known.add_argument('--known-text')
    known.add_argument('--known-file')
    recover.add_argument('--offset', type=int, default=0)
    table.add_argument('--p1-file', required=True)
    table.add_argument('--p2-file', required=True)
    return parser


def run(args):
    if args.mode == 'encrypt':
        plain = to_bytes(read_text(args.text_file))
        key = read_hex(args.key_file)
        cipher = xor_equal(plain, key)
        save_hex(args.out, cipher)
        print('Текст:', plain.decode(ENCODING))
        print('Длины P, K, C:', len(plain), len(key), len(cipher))
        print('P HEX:', hex_line(plain))
        print('C HEX:', hex_line(cipher))
    elif args.mode == 'decrypt':
        cipher = read_hex(args.cipher_file)
        key = read_hex(args.key_file)
        plain = xor_equal(cipher, key)
        text = plain.decode(ENCODING)
        save_text(args.out, text)
        print('Длины C, K, P:', len(cipher), len(key), len(plain))
        print('Открытый текст:', text)
    elif args.mode == 'xor':
        c1 = read_hex(args.c1_file)
        c2 = read_hex(args.c2_file)
        combined = xor_equal(c1, c2)
        save_hex(args.out, combined)
        print('Длины C1, C2:', len(c1), len(c2))
        print('C1 XOR C2:', hex_line(combined))
        print('Ключ не является входом этой операции')
    elif args.mode == 'recover':
        c1 = read_hex(args.c1_file)
        c2 = read_hex(args.c2_file)
        combined = xor_equal(c1, c2)
        known_text = args.known_text
        if args.known_file is not None:
            known_text = read_text(args.known_file)
        known = to_bytes(known_text)
        start = args.offset
        end = start + len(known)
        if start < 0 or end > len(combined):
            raise ValueError('Фрагмент выходит за границы шифротекстов')
        recovered = xor_equal(combined[start:end], known).decode(ENCODING)
        save_text(args.out, recovered)
        print('Известный фрагмент:', known_text)
        print('Смещение от нуля:', start, '| Длина:', len(known), 'байт')
        print('Восстановленный фрагмент:', recovered)
        print('Другой текст:', '?' * start + recovered + '?' * (len(combined) - end))
        print('Вычисление: C1 XOR C2 XOR известный текст; ключ не используется')
    elif args.mode == 'table':
        p1 = to_bytes(read_text(args.p1_file))
        p2 = to_bytes(read_text(args.p2_file))
        c1 = read_hex(args.c1_file)
        c2 = read_hex(args.c2_file)
        plain_xor = xor_equal(p1, p2)
        cipher_xor = xor_equal(c1, c2)
        xor_equal(p1, c1)
        if plain_xor != cipher_xor:
            raise ValueError('Равенство C1 XOR C2 = P1 XOR P2 не выполнено')
        lines = ['i\tP1\tP2\tC1\tC2\tP1^P2\tC1^C2\tEqual']
        for i, values in enumerate(zip(p1, p2, c1, c2, plain_xor, cipher_xor), 1):
            lines.append(str(i) + '\t' + '\t'.join('{:02X}'.format(v) for v in values) + '\tTrue')
        save_text(args.out, '\n'.join(lines) + '\n')
        print('C1 XOR C2 = P1 XOR P2:', plain_xor == cipher_xor)
        print('Строк таблицы:', len(p1))
    print('Сохранено:', args.out)


def main():
    args = build_parser().parse_args()
    try:
        run(args)
    except (OSError, ValueError) as error:
        print('Ошибка:', error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
