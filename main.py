import re
import string
import time
from typing import List
from math import comb, perm
import numpy as np
from itertools import permutations

operation_num = 4
tol = 1e-6


def my_is_equal(x1, x2):
    if abs(x1 - x2) < tol:
        return True
    else:
        return False


def return_prio(ope):
    if ope == '+' or ope == '-':
        return 1
    if ope == '/' or ope == '*':
        return 2
    return 0


def my_ope(x1, x2, ope_ind, x1_in_string, x2_in_string):
    if len(x1_in_string) > 3:
        x1_in_string_new = f"({x1_in_string})"
    else:
        x1_in_string_new = x1_in_string
    if len(x2_in_string) > 3:
        x2_in_string_new = f"({x2_in_string})"
    else:
        x2_in_string_new = x2_in_string

    if ope_ind == 0:
        return x1 + x2, f"{x1_in_string_new} + {x2_in_string_new}"
    elif ope_ind == 1:
        return x1 - x2, f"{x1_in_string_new} - {x2_in_string_new}"
    elif ope_ind == 2:
        return x1 * x2, f"{x1_in_string_new} * {x2_in_string_new}"
    else:
        # do not allow "/0"
        if my_is_equal(x2, 0):
            return None, None
        else:
            return x1 / x2, f"{x1_in_string_new} / {x2_in_string_new}"


def search_answer(number_list, target, number_list_in_string):
    # print(number_list)

    _permus = permutations(range(len(number_list)), len(number_list))
    all_answers_in_str = []
    for ind, _one_permu in enumerate(_permus):
        # select 2 numbers and do operation
        # print(ind, _one_permu)
        for ope1 in range(operation_num):
            new_number_list = []
            new_number_list_in_string = []
            new_num1, new_num1_in_str = my_ope(
                number_list[_one_permu[0]],
                number_list[_one_permu[1]],
                ope1,
                number_list_in_string[_one_permu[0]],
                number_list_in_string[_one_permu[1]]
            )
            if new_num1 is None:
                continue
            new_number_list.append(new_num1)
            new_number_list_in_string.append(new_num1_in_str)

            if len(_one_permu) == 2:
                if my_is_equal(new_num1, target):
                    all_answers_in_str.append(new_num1_in_str)
                    return True, all_answers_in_str
            else:
                for ind_of_remain_num in range(2, len(_one_permu)):
                    new_number_list.append(number_list[_one_permu[ind_of_remain_num]])
                    new_number_list_in_string.append(number_list_in_string[_one_permu[ind_of_remain_num]])

                has_answer, answers_in_str = search_answer(new_number_list, target, new_number_list_in_string)
                all_answers_in_str.extend(answers_in_str)
    if len(all_answers_in_str) > 0:
        return True, all_answers_in_str
    else:
        return False, []


def find_corresponding_left_bracket(expression, right_bracket_index):
    stack = []

    # Traverse the string from the start up to the given right bracket
    for i, char in enumerate(expression[:right_bracket_index + 1]):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                # Pop the last unmatched '(' from the stack
                left_bracket_index = stack.pop()
                # If this is the right bracket we care about, return the index of its corresponding '('
                if i == right_bracket_index:
                    return left_bracket_index

    # If no matching bracket is found, return None
    return None


def find_operators_outside_nested_brackets(expression, left_bracket_index, right_bracket_index):
    idx_of_found_operators = []
    nested_level = 0
    # Traverse the substring between the given brackets
    for i in range(left_bracket_index + 1, right_bracket_index):
        if expression[i] == '(':
            nested_level += 1
        elif expression[i] == ')':
            nested_level -= 1
        elif return_prio(expression[i]) != 0 and nested_level == 0:
            idx_of_found_operators.append(i)

    return idx_of_found_operators


def sort_str_by_ope(str):
    # print(str)
    if str == "(11)":
        pass
    idx_of_ope = find_operators_outside_nested_brackets(str, left_bracket_index=-1, right_bracket_index=len(str))
    if not idx_of_ope:
        if str[0] == '(' and str[-1] == ')':
            return f"({sort_str_by_ope(str[1:-1])})"
        else:
            return str
    idx_of_ope.append(None)

    if str[idx_of_ope[0]] == '+' or str[idx_of_ope[0]] == '-':
        identifier = ['+', '-']
    else:
        identifier = ['*', '/']
    positive_items = [sort_str_by_ope(str[: idx_of_ope[0]])]
    negative_items = []
    for i in range(len(idx_of_ope) - 1):
        if str[idx_of_ope[i]] == identifier[0]:
            positive_items.append(sort_str_by_ope(str[idx_of_ope[i] + 1: idx_of_ope[i + 1]]))
        else:
            negative_items.append(sort_str_by_ope(str[idx_of_ope[i] + 1: idx_of_ope[i + 1]]))
    sorted_positive_items = sorted(positive_items)
    sorted_negative_items = sorted(negative_items)
    sorted_str = identifier[0].join(sorted_positive_items)
    if sorted_negative_items:
        sorted_str += identifier[1]
        sorted_str += identifier[1].join(sorted_negative_items)
    return sorted_str


# remove brackets, however, doesn't return '='
def remove_brackets(_str):
    _str += '='
    # step1: remove brackets
    bracket_and_ope_stack = ""
    number_stack = []
    number_char = ""
    for char in _str:
        if char in string.digits:
            number_char += char
        else:
            if number_char != "":
                number_stack.append(int(number_char))
                number_char = ""

            if char in set("+-*/()="):
                bracket_and_ope_stack += char

            # judge whether the '(' and ')' could be removed
            if len(bracket_and_ope_stack) > 2 and bracket_and_ope_stack[-2] == ')':

                # find the two (maybe one) operators outside "()" and the sup operator inside "()"
                ind_of_right_br = len(bracket_and_ope_stack) - 2
                ind_of_left_br = find_corresponding_left_bracket(bracket_and_ope_stack,
                                                                 right_bracket_index=ind_of_right_br)
                # find the two (maybe one) operators outside "()"
                left_ope_outside = right_ope_outside = None
                # the right side
                if return_prio(bracket_and_ope_stack[-1]) != 0:
                    right_ope_outside = bracket_and_ope_stack[-1]
                # the left side
                if ind_of_left_br != 0 and return_prio(bracket_and_ope_stack[ind_of_left_br - 1]) != 0:
                    left_ope_outside = bracket_and_ope_stack[ind_of_left_br - 1]

                # find all sup operator inside "()"
                idx_of_sup_ope_inside = find_operators_outside_nested_brackets(bracket_and_ope_stack,
                                                                               left_bracket_index=ind_of_left_br,
                                                                               right_bracket_index=ind_of_right_br)

                canbe_removed = True
                if idx_of_sup_ope_inside:
                    if left_ope_outside is not None and return_prio(left_ope_outside) != return_prio(
                            bracket_and_ope_stack[idx_of_sup_ope_inside[0]]):
                        canbe_removed = False
                    if right_ope_outside is not None and return_prio(right_ope_outside) != return_prio(
                            bracket_and_ope_stack[idx_of_sup_ope_inside[0]]):
                        canbe_removed = False

                if canbe_removed:
                    # if "-(...)", the "-" or "+" inside "(...)" must be changed
                    # if "/(...)", the "/" or "*" inside "(...)" must be changed
                    if left_ope_outside == "/":
                        for ind in idx_of_sup_ope_inside:
                            if bracket_and_ope_stack[ind] == '/':
                                bracket_and_ope_stack = bracket_and_ope_stack[: ind] + '*' + bracket_and_ope_stack[
                                                                                             ind + 1:]
                            elif bracket_and_ope_stack[ind] == '*':
                                bracket_and_ope_stack = bracket_and_ope_stack[: ind] + '/' + bracket_and_ope_stack[
                                                                                             ind + 1:]
                            else:
                                print(bracket_and_ope_stack)
                                print(bracket_and_ope_stack[ind_of_left_br: ind_of_right_br + 1])
                                raise Exception("error: sup_opes_inside has multiple priorities")

                    if left_ope_outside == "-":
                        for ind in idx_of_sup_ope_inside:
                            if bracket_and_ope_stack[ind] == '-':
                                bracket_and_ope_stack = bracket_and_ope_stack[: ind] + '+' + bracket_and_ope_stack[
                                                                                             ind + 1:]
                            elif bracket_and_ope_stack[ind] == '+':
                                bracket_and_ope_stack = bracket_and_ope_stack[: ind] + '-' + bracket_and_ope_stack[
                                                                                             ind + 1:]
                            else:
                                print(bracket_and_ope_stack)
                                print(bracket_and_ope_stack[ind_of_left_br: ind_of_right_br + 1])
                                raise Exception("error: sup_opes_inside has multiple priorities")

                    new_bracket_and_ope_stack = bracket_and_ope_stack[: ind_of_left_br] + \
                                                bracket_and_ope_stack[ind_of_left_br + 1: ind_of_right_br] + \
                                                bracket_and_ope_stack[ind_of_right_br + 1:]
                    bracket_and_ope_stack = new_bracket_and_ope_stack
    if number_char != "":
        number_stack.append(int(number_char))
    # output string
    formatted_str = ""
    while True:
        if bracket_and_ope_stack.__len__() == 0 or bracket_and_ope_stack[0] == '=':
            break
        # output brackets
        if bracket_and_ope_stack[0] == "(":
            formatted_str += bracket_and_ope_stack[0]
            bracket_and_ope_stack = bracket_and_ope_stack[1:]
            continue

        # output numbers
        if len(formatted_str) == 0 or formatted_str[-1] != ")":
            formatted_str += str(number_stack[0])
            number_stack.pop(0)
        # output operators
        formatted_str += bracket_and_ope_stack[0]
        bracket_and_ope_stack = bracket_and_ope_stack[1:]
    if number_stack:
        formatted_str += str(number_stack[0])
        number_stack.pop(0)
    return formatted_str


def format_answer(answer_in_string, target):
    formatted_str = remove_brackets(answer_in_string)
    # 3 + (( 4 + 5 ) * 7)   : do nothing
    # (3 + ( 4 + 5 )) + 7     : remove
    # step2: sort elements
    # extract "/1" and "*1", and then add it after sorted
    # Use a regular expression to match "*1" or "/1" not followed by a digit
    patterns = [r"[\*/]1(?!\d)", r"(?<!\d)1\*"]
    count_times_one = 0
    modified_formatted_str = formatted_str
    for pattern in patterns:
        # Find all matches
        matches = re.findall(pattern, modified_formatted_str)
        count_times_one += len(matches)
        # Remove all occurrences
        modified_formatted_str = re.sub(pattern, '', modified_formatted_str)
    # remove twice
    formatted_str2 = remove_brackets(modified_formatted_str)
    # sort elements
    # print(formatted_str, formatted_str2)
    sorted_str = sort_str_by_ope(formatted_str2)
    for i in range(count_times_one):
        sorted_str += "*1"
    sorted_str += f"={target}"
    return sorted_str


if __name__ == "__main__":
    start_time = time.time()
    limit = 13
    target = 24
    count_problems = count_dead_problems = 0
    for x1 in np.arange(1, limit + 1):
        for x2 in np.arange(x1, limit + 1):
            for x3 in np.arange(x2, limit + 1):
                for x4 in np.arange(x3, limit + 1):
                    number_list = [x1, x2, x3, x4]
                    number_list_in_string = [str(number_i) for number_i in number_list]
                    has_answer, answers_in_str = search_answer(number_list, target, number_list_in_string)
                    # calculate weight
                    _remove_dup_num = len(set(number_list))
                    if _remove_dup_num == 1:
                        weight = perm(4, 4)
                    elif _remove_dup_num == 4:
                        weight = perm(4, 4) * (4 ** 4)
                    elif _remove_dup_num == 3:
                        weight = perm(4, 2) * (4 ** 2) * perm(4, 2)
                    else:
                        if x2 == x3:
                            # a, a, a, b or a, b, b, b
                            weight = perm(4, 1) * (4 ** 1) * perm(4, 3)
                        else:
                            # a, a, b, b
                            weight = comb(4, 2) * perm(4, 2) * perm(4, 2)

                    if has_answer:
                        count_problems += 1
                        # count_problems += weight

                        answers_remove_duplication = set()

                        for answer_in_str in answers_in_str:
                            formatted_answer_in_str = format_answer(answer_in_str, target)
                            # print("\t", answer_in_str, "\t", formatted_answer_in_str)
                            answers_remove_duplication.add(formatted_answer_in_str)
                        # all_answer_use_minus_and_div = True
                        # for answer_in_str in answers_remove_duplication:
                        #     if any([char in answer_in_str for char in set('+*')]):
                        #         all_answer_use_minus_and_div = False
                        # if len(answers_remove_duplication) == 1:
                        # if all_answer_use_minus_and_div:
                        # print(number_list)
                        # print(f"found {len(answers_remove_duplication)} answers:")
                        # print("\t" + "\n\t".join(answers_remove_duplication))
                    else:
                        count_dead_problems += 1
                        # count_dead_problems += weight



    print("total problems:", count_problems)
    print("dead problems:", count_dead_problems)
    print(f"ratio: {count_problems / (count_problems + count_dead_problems) * 100: 02.2f}%")
    print(f"cost time: {time.time() - start_time:.2f} s")
