from operator import attrgetter


def get_general_specifications(product_list):
    general = set()
    for product in product_list:
        for specification in product.specifications():
            general.add(specification)
    return general


def get_values_specifications(product_list, get):
  values = {}
  for specification in get_general_specifications(product_list):
    values[specification] = {}
    for product in product_list:
      if specification in (specifications := product.specifications()):
        value = specifications[specification]
        if value not in values[specification]:
          values[specification][value] = [1, value if value in get else None]
        else:
          values[specification][value][0] += 1
  return values

def get_minmax_products(product_list):
  sorted_products = sorted(product_list, key=attrgetter('price'))
  return sorted_products[0], sorted_products[-1]