import argparse
import csv
import io
import os
import tempfile


def report_to_csv_string(rep):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(rep)
    return output.getvalue()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action='store',
                        help="repository URL", required=True)
    parser.add_argument('-l', '--lang', action='store',
                        choices=['python'], default='python',
                        help='parsing programming language')
    parser.add_argument('-r', '--report', action='store',
                        choices=['vcf', 'vcl', 'ncf', 'ncl'], default='vcf',
                        help='report type: '
                             ' vcf - verbs count in function names; '
                             ' vcl - verbs count in local variables; '
                             ' ncf - nouns count in function names; '
                             ' ncl - nouns count in local variables '
                        )
    parser.add_argument('-f', '--format', action='store',
                        choices=['plain', 'json', 'csv'], default='plain',
                        help='output format')
    parser.add_argument('-t', '--topmost', action='store', type=int,
                        default=0, help='set the number of records '
                                        'to show (default 0 - all records)')
    parser.add_argument('-o', '--out', action='store',
                        help='output report file name')
    parser.add_argument('-d', '--dir', action='store',
                        help='directory to store repository')
    return parser


def parse_input_parameters():
    parser = create_parser()
    params = parser.parse_args()
    return params


def get_working_dir(dir):
    if dir:
        if not os.path.isdir(dir):
            # create a directory
            os.mkdir(dir)
        return dir
    else:
        # create temp dir
        return tempfile.gettempdir()
