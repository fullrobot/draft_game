import argparse
from os import environ
from dotenv import load_dotenv
from slugify import slugify

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input Filename", dest="infile")
    args = parser.parse_args()
    infile = args.infile

    load_dotenv()

    host = environ["POSTGRES_HOST"]
    port = environ["POSTGRES_PORT"]
    user = environ["POSTGRES_USER"]
    password = environ["POSTGRES_PASSWORD"]
    db = environ["POSTGRES_DB"]
    dbtype = "postgresql"

    uri = f"{dbtype}://{user}:{password}@{host}:{port}/{db}"

    engine = create_engine(uri)

    db = scoped_session(sessionmaker(bind=engine))

    with open(infile) as f:
        # NOTE: Skip header
        for line in f.readlines()[1:]:
            name, value, card_type, effect = line.replace("'", "").strip().split("\t")
            slug = slugify(name)
            sql = text(f"""
                INSERT INTO cards (name, value, card_type, effect, slug)
                VALUES('{name}', {value}, '{card_type}', '{effect}', '{slug}');
                """)
            db.execute(sql)

            db.commit()

    db.close()


if __name__ == "__main__":
    main()
