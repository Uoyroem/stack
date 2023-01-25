
def get_general_specifications(product_list):
    general = set()
    for product in product_list:
        for specification in product.specifications():
            general.add(specification)
    return general


def get_values_specifications(product_list):
  values = {}
  for specification in get_general_specifications(product_list):
    values[specification] = {}
    for product in product_list:
      if specification in (specifications := product.specifications()):
        if specifications[specification] not in values[specification]:
          values[specification][specifications[specification]] = 1
        else:
          values[specification][specifications[specification]] += 1
  return values
