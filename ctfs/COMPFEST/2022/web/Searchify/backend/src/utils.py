def filter_items(items, keys):
    excluded_keys = [v for v in items.keys() if v not in keys]
    for key in excluded_keys:
        del items[key]
        
    return items

def normalize(elements):
    results = []
    for enum, element in enumerate(elements):
        items = dict()

        for key, val in element.items():
            if key == 'title' or key == 'name':
                mod_key = 'site_name'
            elif key == 'href' or key == 'url':
                mod_key = 'site_link'
            elif key == 'body' or key == 'snippet':
                mod_key = 'site_meta'
   
            items[mod_key] = val
        
        results.append((enum, items))

    return dict(results)
