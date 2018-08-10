from functools import reduce

identity = lambda x: x
is_truthy = bool
NOTHING = ''

def to_dict(named_tuple):
  return dict(zip(named_tuple._fields, named_tuple))

def enum_values(enum):
  return (member.value for member in enum)

def get_enum_member(enum, value):
  for member in enum:
    if member.value == value:
      return member

def join(*items):
  return NOTHING.join(items)

def curry(prior, *additional):
  def curried(*args):
    return prior(*(args + additional))
  return curried

def skip_falsy_and_join(*items):
  return join(*filter(is_truthy, items))
