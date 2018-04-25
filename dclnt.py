import ast
import os
import collections

from nltk import pos_tag, download


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def only_ext(ext):
    def compare(file_name): return file_name.endswith(ext)
    return compare


def get_trees_file_names(tree_root_path):
    file_names = []

    for dir_name, _, files in os.walk(tree_root_path, topdown=True):
        for file in filter(only_ext('.py'), files):
            file_names.append(os.path.join(dir_name, file))

    return file_names


def get_file_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as attempt_handler:
        return attempt_handler.read()


def parse_file_content(content):
    try:
        return ast.parse(content)
    except SyntaxError as e:
        print(e)
        return None


def get_trees(tree_root_path, with_filenames=False, with_file_content=False):

    trees = []
    file_names = get_trees_file_names(tree_root_path)

    print('total %s files' % len(file_names))
    for filename in file_names:
        file_content = get_file_content(filename)
        tree = parse_file_content(file_content)
        if with_filenames:
            if with_file_content:
                trees.append((filename, file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)

    print('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if n]


def get_all_words_in_path(path):
    trees = [t for t in get_trees(path) if t]
    function_names = [f for f in flat([get_all_names(t) for t in trees]) if not (f.startswith('__') and f.endswith('__'))]
    return flat([split_snake_case_name_to_words(function_name) for function_name in function_names])


def get_lower_case_function_names(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_flat_lower_case_function_names(trees):
    return flat([get_lower_case_function_names(t) for t in trees])


def get_function_names(path):
    trees = [t for t in get_trees(path) if t]
    return [f for f in get_flat_lower_case_function_names(trees) if not (f.startswith('__') and f.endswith('__'))]


def get_top_verbs_in_path(path, top_size=10):
    functions = get_function_names(path)
    print('functions extracted. count =', len(functions))
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in functions])
    return collections.Counter(verbs).most_common(top_size)


def get_top_functions_names_in_path(path, top_size=10):
    functions = get_function_names(path)
    return collections.Counter(functions).most_common(top_size)


def setup():
    try:
        pos_tag(['apple'])
        print("NLTK data already installed")
    except LookupError:
        print("Installing NLTK data...")
        download('averaged_perceptron_tagger')


if __name__ == '__main__':

    setup()

    verbs = []
    functions = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    for project in projects:
        path = os.path.join('.', project)
        verbs += get_top_verbs_in_path(path)
        functions += get_top_functions_names_in_path(path)

    top_size = 200
    print('total %s verbs, %s unique' % (len(verbs), len(set(verbs))))
    for verb, occurence in collections.Counter(verbs).most_common(top_size):
        print(verb, occurence)

    print('total %s functions, %s unique' % (len(functions), len(set(functions))))
    for func_name, occurence in collections.Counter(functions).most_common(top_size):
        print(func_name, occurence)
