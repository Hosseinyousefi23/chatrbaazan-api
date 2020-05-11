from shop.filters import ProductFilter, CompanyFilter, CategoryFilter

FIELD_NAMES = {
    'category': {
        'company': {'name': 'category_company', 'iterable': True},
        'product': {'name': 'product_category', 'iterable': True},
    },
    'company': {
        'category': {'name': 'category', 'iterable': True},
        'product': {'name': 'product_company', 'iterable': True},
    },

    'product': {
        'company': {'name': 'company', 'iterable': True},
        'category': {'name': 'category', 'iterable': True},
    }
}

FILTERS = {
    'product': ProductFilter,
    'company': CompanyFilter,
    'category': CategoryFilter,
}
