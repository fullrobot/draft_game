import argparse
from os import environ
from dotenv import load_dotenv
from slugify import slugify
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input JSON", dest="infile")
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

    with open(infile, "r") as f:
        data = json.load(f)
        for card in data:
            name = card["name"]
            value = card["value"]
            card_type = card["type"]
            effect = card["effect"]
            slug = slugify(name)

            effect_description = effect["description"]
            effect_type = effect["effect_type"].upper()
            value_change = effect["value_change"]
            condition = effect["condition"]
            game_effect = effect["game_effect"]

            sql = text(f"""
                INSERT INTO effects (description, effect_type, value_change, condition, game_effect)
                VALUES('{effect_description}', '{effect_type}', {value_change}, '{condition}', '{game_effect}')
                RETURNING id;
                """)
            effect_id = db.execute(sql).fetchone()[0]

            sql = text(f"""
                INSERT INTO cards (name, slug, value, card_type, effect_id)
                VALUES('{name}', '{slug}', {value}, '{card_type}', {effect_id});
                """)

            db.execute(sql)

            db.commit()

    db.close()


if __name__ == "__main__":
    main()
