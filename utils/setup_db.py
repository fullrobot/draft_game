import argparse
import sqlite3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input Filename", dest="infile")
    args = parser.parse_args()
    infile = args.infile

    conn = sqlite3.connect("assets/cards.db")
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS cards;')
    c.execute("""
        CREATE TABLE IF NOT EXISTS cards 
        (
            [id] INTEGER PRIMARY KEY,
            [name] TEXT,
            [value] INTEGER,
            [type] TEXT,
            [effect] TEXT
        );
        """
    )
    conn.commit()

    with open(infile) as f:
        # NOTE: Skip header
        for index, line in enumerate(f.readlines()[1:], start=1):
            name, value, card_type, effect = line.strip().split("\t")
            sql = f"""
                INSERT INTO cards (id, name, value, type, effect)
                VALUES({index}, "{name}", {value}, "{card_type}", "{effect}");
                """
            print(sql)
            c.execute(sql)
            conn.commit()


if __name__ == "__main__":
    main()
