# OTUS WebDev homework #01
> Домашняя работа по курсу OTUS WebDev

Библиотека подсчитывает самые популярные глаголы и самые популярные названия методов в исходниках на Python

## Installation

```bash
git clone https://github.com/pythonist77/otus_webdev_homework_01.git
cd otus_webdev_homework_01
pip install -r requirements.txt 
python -c "from dclnt import setup; setup()"
```

## Usage example

```python
top_size = 200

verbs += get_top_verbs_in_path(path)
print('total %s verbs, %s unique' % (len(verbs), len(set(verbs))))
for verb, occurence in collections.Counter(verbs).most_common(top_size):
    print(verb, occurence)

functions += get_top_functions_names_in_path(path)
print('total %s functions, %s unique' % (len(functions), len(set(functions))))
for word, occurence in collections.Counter(functions).most_common(top_size):
    print(word, occurence)
```

## Release History

* 0.1.0
    * The first proper release
