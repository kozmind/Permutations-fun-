import itertools as it
import time

REPEATS = 7
DIGIT = '2'
SIGNS = ('+', '-', '*', '/')
RESULTS_FROM = 100
RESULTS_TO = 2000

declension = {
    1: 'вариант',
    2: 'варианта',
    3: 'варианта',
    4: 'варианта',
    5: 'вариантов',
    6: 'вариантов',
    7: 'вариантов',
    8: 'вариантов',
    9: 'вариантов',
    0: 'вариантов',
}


def find_combinations():
    """Перебирает комбинации, проверяет их на условие."""
    correct_variants = {}
    expand_signs = it.chain(SIGNS, ('',))
    signs_sets = it.combinations_with_replacement(expand_signs, REPEATS)
    copy_set, signs_sets = it.tee(signs_sets, 2)
    count_of_items = len(list(copy_set))
    counter = it.count()
    for signs_set in signs_sets:
        permut_sings = it.permutations(signs_set)
        for _ in permut_sings:
            test = ''.join(it.chain.from_iterable(it.product(_, DIGIT)))
            if test[0] not in ('*', '/'):
                res = eval(test)
                if res % 1 == 0 and RESULTS_FROM <= res <= RESULTS_TO:  # условие
                    res_s = str(int(res))
                    if not correct_variants.get(res_s):
                        correct_variants[res_s] = set()
                    correct_variants[res_s].add(test)
        print(next(counter), 'из', count_of_items)  # прогресс
    return correct_variants


def default_format(expression):
    """Приводит вариант к универсальному формату, чтобы отсечь повторения."""
    if expression[0] == '+':
        expression = expression[1:]
    prev, split_exp = 0, []
    for _num, _symbol in enumerate(expression[1:]):
        if _symbol == '+':
            split_exp.append(expression[prev:_num + 1])
            prev = _num + 2
        elif _symbol == '-':
            split_exp.append(expression[prev:_num + 1])
            prev = _num + 1
    split_exp.append(expression[prev:])
    for n, sub_split_exp in enumerate(split_exp):
        if sub_split_exp[0] == '-':
            minus = '-'
            sub_split_exp = sub_split_exp[1:]
        else:
            minus = ''
        prev, sub_list = 0, []
        for _num, _symbol in enumerate(sub_split_exp[1:]):
            if _symbol == '*' or _symbol == '/':
                if prev == 0:
                    sub_list.append(f'*{sub_split_exp[prev:_num + 1]}')
                    prev = _num + 1
                else:
                    sub_list.append(sub_split_exp[prev:_num + 1])
                    prev = _num + 1
        sub_list.append(sub_split_exp[prev:])
        sub_list.sort(key=lambda _: _.count('/'))
        sub_list.sort(key=len, reverse=True)
        split_exp[n] = f"{minus}{''.join(sub_list)}".replace('-*', '-')
        if split_exp[n][0] == '*':
            split_exp[n] = split_exp[n][1:]
    split_exp.sort(key=lambda _: _.count('/'))
    split_exp.sort(key=lambda _: _.count('-'))
    split_exp.sort(key=len, reverse=True)
    return '+'.join(split_exp).replace('+-', '-')


def delete_duplicates(variants):
    for _value in variants:
        new_value = set()
        for _variant in variants[_value]:
            new_value.add(default_format(_variant))
        variants[_value] = new_value
    return variants


def print_results(variants):
    for _value in variants:
        variants_count = len(variants[_value])
        print(f'{_value} имеет {variants_count} {declension[variants_count % 10]}')
        for _variant in variants[_value]:
            print(_variant)


start_moment = time.perf_counter()
start_time = time.process_time()

good_variants = find_combinations()
perfect_variants = delete_duplicates(good_variants)
print_results(perfect_variants)

stop_moment = time.perf_counter()
stop_time = time.process_time()
print(f'Выполнилось за {stop_moment-start_moment} с по perf_counter')
print(f'Выполнилось за {(stop_time-start_time)} с по process_time')
