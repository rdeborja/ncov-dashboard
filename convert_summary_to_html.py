#!/usr/bin/env python

"""
Import the QC summary file from the ncov-tools pipeline and generate a dashboard
web page.
"""

import argparse
import csv
import sys
import jinja2


def init_parser():
    parser = argparse.ArgumentParser(description="Create the dashboard web page")
    parser.add_argument('-q', '--qc',
                        help='full path to the _summary_qc.tsv QC file from the ncov-tools pipeline')
    parser.add_argument('-r', '--run_name', help='name of the run')
    parser.add_argument('-t', '--template', help='path to the html template file')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def main():
    args = init_parser()
    templateLoader = jinja2.FileSystemLoader(searchpath='.')
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(args.template)
    qc = list()

    with open(args.qc, 'r') as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        for item in reader:
            qc.append(item)
    fh.close()

    outputText = template.render(qc=qc, run_name=args.run_name)
    print(outputText)


if __name__ == "__main__":
    main()

