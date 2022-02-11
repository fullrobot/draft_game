import argparse
import sqlite3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input Filename", dest="infile")
    args = parser.parse_args()
    infile = args.infile

    conn = sqlite3.connect("app/cards.db")
    c = conn.cursor()

    with open(infile) as f:
        # NOTE: Skip header
        for index, line in enumerate(f.readlines()[1:], start=1):
            name, value, card_type, effect = line.strip().split("\t")
            sql = f"""
                INSERT INTO cards (name, value, card_type, effect)
                VALUES("{name}", {value}, "{card_type}", "{effect}");
                """
            c.execute(sql)
            conn.commit()


if __name__ == "__main__":
    main()
