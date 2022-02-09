import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input Filename", dest="infile")
    parser.add_argument("--output", type=str, help="Output Filename", dest="outfile")
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    data = []

    with open(infile) as f:
        # NOTE: Skip header
        for line in f.readlines()[1:]:
            name, value, card_type, effect = line.strip().split("\t")
            data.append(
                {
                    "name": name,
                    "value": value,
                    "type": card_type,
                    "effect": effect,
                }
            )
    with open(outfile, "w") as fout:
        json.dump(fp=fout, obj=data)


if __name__ == "__main__":
    main()
