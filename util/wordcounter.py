import ast
import os
import collections
import logging

from nltk import pos_tag

verb_tags = ['VB', 'VBZ', 'VBN', 'VBG', 'VBD', 'BE', 'BEG',
             'BEM', 'BER', 'BEZ', 'BEN', 'BED', 'BEDZ', 'VERB']

noun_tags = ['N', 'NN', 'NOUN']


def flatten_list(list_to_flat):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in list_to_flat], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] in verb_tags


def is_noun(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] in noun_tags


def is_system_name(name):
    return name.startswith('__') and name.endswith('__')


def split_snake_case_name(name):
    return [n for n in name.split('_') if n]


def get_verbs_from_name(name):
    return [w for w in split_snake_case_name(name) if is_verb(w)]


def get_nouns_from_name(name):
    return [w for w in split_snake_case_name(name) if is_noun(w)]


def get_lang_filenames_in_path(path, lang_ext):
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith(lang_ext):
                filenames.append(os.path.join(dirname, file))
    return filenames


def build_ast_tree_for_file(filename):
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as e:
        logging.ERROR(e)
        tree = None
    return tree


def build_ast_trees(path, lang_ext):
    trees = []
    filenames = get_lang_filenames_in_path(path, lang_ext)
    for filename in filenames:
        tree = build_ast_tree_for_file(filename)
        if tree:
            trees.append(tree)
    return trees


def get_function_names_from_ast(tree):
    function_names = [n.name.lower() for n in ast.walk(tree)
                      if isinstance(n, ast.FunctionDef)]
    return function_names


def get_function_names_in_path(path, lang_ext):
    trees = build_ast_trees(path, lang_ext)
    func_names = flatten_list([get_function_names_from_ast(t) for t in trees])
    user_func_names = [n for n in func_names if not is_system_name(n)]
    return user_func_names


def get_filtered_words_in_functions_names(path, le, wff, t=None):
    func_names = get_function_names_in_path(path, le)
    filtered_words = flatten_list([wff(n) for n in func_names])
    if t != 0:
        return collections.Counter(filtered_words).most_common(t)
    else:
        return collections.Counter(filtered_words).most_common()


def get_local_names_from_ast(tree):
    local_names = [n.id for n in ast.walk(tree) if isinstance(n, ast.Name)]
    return local_names


def get_local_names_in_path(path, lang_ext):
    trees = build_ast_trees(path, lang_ext)
    local_names = flatten_list([get_local_names_from_ast(t) for t in trees])
    user_local_names = [n for n in local_names if not is_system_name(n)]
    return user_local_names


def get_filtered_words_in_local_names(path, lang_ext, word_filter_fn, t=0):
    func_names = get_local_names_in_path(path, lang_ext)
    filtered_words = flatten_list([word_filter_fn(n) for n in func_names])
    if t != 0:
        return collections.Counter(filtered_words).most_common(t)
    else:
        return collections.Counter(filtered_words).most_common()
