def make_list(_item):
    _type = type(_item).__name__

    if _type in ["tuple", "set"]:
        res = list(_item)
    elif _type == "dict":
        res = [list(_item.keys()), list(_item.values())]
    elif _type == "list":
        res = _item
    elif _type is None:
        res = []
    else:
        res = [_item]
    return res
