def filter_nested_lists(nested_list, result=[]):
    for item in nested_list:
        if isinstance(item, list):
            filter_nested_lists(item, result)
        else:
            result.append(nested_list)
            break
    return result
