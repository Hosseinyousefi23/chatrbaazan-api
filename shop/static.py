FIELD_NAMES = {
    'category': {
        'company': {'name': 'category_company', 'iterable': True},
        'product': {'name': 'product_category', 'iterable': True},
    },
    'company': {
        'category': {'name': 'category', 'iterable': False},
        'product': {'name': 'product_company', 'iterable': True},
    },

    'product': {
        'company': {'name': 'company', 'iterable': True},
        'category': {'name': 'category', 'iterable': True},
    }
}
