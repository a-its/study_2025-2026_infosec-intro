import argparse
import secrets
import sys
from pathlib import Path


def hex_text(data):
    return " ".join("{:02X}".format(value) for value in data)


def load_hex(path):
    data = bytes.fromhex(Path(path).read_text(encoding="utf-8"))
    if not data:
        raise ValueError("Пустой HEX-файл: " + path)
    return data


def xor_bytes(left, right):
    if len(left) != len(right):
        raise ValueError(
            "Длины не совпадают: {} и {} байт".format(len(left), len(right))
        )
    return bytes(a ^ b for a, b in zip(left, right))


def save_hex(path, data):
    if path:
        with open(path, "x", encoding="utf-8") as stream:
            stream.write(hex_text(data) + "\n")
        print("Файл HEX:", path)


def show_table(left, right, result, labels):
    print("Байты: {} XOR {} = {}".format(*labels))
    print(" i  {}   {}   {}".format(*labels))
    for i, values in enumerate(zip(left, right, result), 1):
        print("{:2d}  {:02X}  {:02X}  {:02X}".format(i, *values))


def main():
    parser = argparse.ArgumentParser(description="ЛР 7: XOR-гаммирование байтов")
    commands = parser.add_subparsers(dest="command", required=True)
    genkey = commands.add_parser("genkey", help="Создать случайную гамму")
    genkey.add_argument("--length", type=int, required=True)
    genkey.add_argument("--out", required=True)
    for command in ("encrypt", "decrypt", "derive"):
        item = commands.add_parser(command)
        if command in ("encrypt", "derive"):
            item.add_argument("--text", required=True)
            item.add_argument("--encoding", default="cp1251")
        if command in ("decrypt", "derive"):
            item.add_argument("--data-file", required=True)
        if command in ("encrypt", "decrypt"):
            item.add_argument("--key-file", required=True)
        if command == "decrypt":
            item.add_argument("--encoding", default="cp1251")
        item.add_argument("--out")
        item.add_argument("--table", action="store_true")
    args = parser.parse_args()
    if args.command == "genkey":
        if args.length <= 0:
            raise ValueError("Длина ключа должна быть положительной")
        result = secrets.token_bytes(args.length)
        print("Длина ключа:", len(result), "байт")
        print("K HEX:", hex_text(result))
        save_hex(args.out, result)
        return
    if args.command in ("encrypt", "derive"):
        plain = args.text.encode(args.encoding)
        if not plain:
            raise ValueError("Пустой открытый текст")
        print("Текст:", args.text)
        print("Кодировка:", args.encoding)
        print("Длина текста:", len(plain), "байт")
        print("P HEX:", hex_text(plain))
    if args.command == "encrypt":
        key = load_hex(args.key_file)
        result = xor_bytes(plain, key)
        left, right, labels = plain, key, ("P", "K", "C")
        print("K HEX:", hex_text(key))
        print("C HEX:", hex_text(result))
    elif args.command == "decrypt":
        cipher = load_hex(args.data_file)
        key = load_hex(args.key_file)
        result = xor_bytes(cipher, key)
        left, right, labels = cipher, key, ("C", "K", "P")
        print("C HEX:", hex_text(cipher))
        print("K HEX:", hex_text(key))
        print("P HEX:", hex_text(result))
        print("Длина текста:", len(result), "байт")
        print("Кодировка:", args.encoding)
        print("Текст:", result.decode(args.encoding))
    else:
        cipher = load_hex(args.data_file)
        result = xor_bytes(cipher, plain)
        left, right, labels = cipher, plain, ("C", "P", "K")
        print("C HEX:", hex_text(cipher))
        print("K HEX:", hex_text(result))
        print("Проверка C XOR K = P:", xor_bytes(cipher, result) == plain)
    save_hex(args.out, result)
    if args.table:
        show_table(left, right, result, labels)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, LookupError) as error:
        print("ОШИБКА:", error, file=sys.stderr)
        sys.exit(2)
