from collections import OrderedDict

def helper(data, prop, is_data=False):
    pr =  prop.split('.')
    pr1= prop.split('.')
    count=0
    for p in pr:
        if count == 2:
            return None
        count+=1
        pr1=pr1[1:]
        nextprop = '.'.join(pr1)
        if hasattr(data, p):
            if nextprop=='':
                return getattr(data, p)
            return helper(getattr(data, p), nextprop, True)

        elif type(data) == dict or isinstance(data, OrderedDict):
            if nextprop=='':
                return data[p]
            ret = helper(data[p], nextprop, True) if p in data else None
            return ret

        elif type(data) == list or type(data) == tuple or type(data)==str:
            try:
                if nextprop=='':
                    return data[int(p)]
                return helper(data[int(p)], nextprop, True)
            except (ValueError, TypeError, IndexError):
                return None
        else:
            return None

    if is_data:
        return data
    else:
        return None
