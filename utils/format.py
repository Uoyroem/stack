import re
from . import DEFAULT_DENOMINATION, DEFAULT_SEP


def format_price(x: float, /, *, sep: str | None = None, denomination: str | None = None) -> str:
  if denomination is None:
    denomination = DEFAULT_DENOMINATION
  if sep is None:
    sep = DEFAULT_SEP
  return sep.join(re.findall(r'\d{1,3}', str(round(x))[::-1]))[::-1] + ' ' + denomination
