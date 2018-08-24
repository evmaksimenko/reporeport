import git
import util.wordcounter as wc
import util.common as common
from urllib.parse import urlparse
import json

rep_fn_dict = {
    'vcf': wc.get_filtered_words_in_functions_names,
    'vcl': wc.get_filtered_words_in_local_names,
    'ncf': wc.get_filtered_words_in_functions_names,
    'ncl': wc.get_filtered_words_in_local_names,
    }

filter_fn_dict = {
    'vcf': wc.get_verbs_from_name,
    'vcl': wc.get_verbs_from_name,
    'ncf': wc.get_nouns_from_name,
    'ncl': wc.get_nouns_from_name,
    }

lang_ext_dict = {
    'python': '.py'
}

format_fn_dict = {
    'json': json.dumps,
    'plain': str,
    'csv': common.report_to_csv_string,
}


def clone_remote_repo(url, dir):
    repo_addr = urlparse(url)[1]
    if repo_addr == "github.com":
        print('Cloning github repository from ' + url + ' to ' +
              dir + '..', end='', flush=True)
        try:
            git.Repo.clone_from(url, dir)
            print('done')
        except git.exc.GitCommandError:
            print('\nError cloning repository. Make sure the directory '
                  'is empty and you have enough rights to write.')
            return False
        return True
    else:
        print('Unknown repository address')
        return False


def create_report(w_dir, rep_lang, rep_type, topmost):
    rep_fn = rep_fn_dict.get(rep_type)
    filter_fn = filter_fn_dict.get(rep_type)
    lang_ext = lang_ext_dict.get(rep_lang)
    rep = rep_fn(w_dir, lang_ext, filter_fn, topmost)
    return rep


def format_result(rep_result, rep_format):
    format_fn = format_fn_dict.get(rep_format)
    return format_fn(rep_result)


def report_output(outfile, formatted_result):
    if not outfile:
        print(formatted_result)
        return
    try:
        with open(outfile, 'x') as f:
            print(formatted_result, file=f)
    except IOError as err:
        print("Error writing to file. Make sure it's not exists and you "
              "have enough rights to write.")
