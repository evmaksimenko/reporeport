import ast
import collections
import git
import util.wordcounter as wc
from nltk import pos_tag
from urllib.parse import urlparse


def clone_remote_repo(url, dir):
    repo_addr = urlparse(url)[1]
    if repo_addr == "github.com":
        print('Cloning github repository from ' + url + ' to ' + dir + '..', end='', flush=True)
        try:
            repo = git.Repo.clone_from(url, dir)
            print('done')
        except git.exc.GitCommandError:
            print('\nError cloning repository. Make sure the directory is empty and you have enough rights to write.')
            return False
        return True
    else:
        print('Unknown repository address')
        return False


def create_report(w_dir, rep_lang, rep_type, topmost):
    wc.get_top_functions_names_in_path(w_dir)
    return 1


def format_result(rep_result, rep_format):
    return 1


def report_output(outfile):
    return 1