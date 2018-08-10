from .case import GrammaticalCase, get_case_processor
from .phonology import is_front, is_back
from .functional import join, NOTHING
from .suffix import Suffix

def subject(
  stem,
  is_plural=False,
  case=GrammaticalCase.NOMINATIVE,
):
  if is_plural:
    suffix = \
      Suffix.LER if is_front(stem) else Suffix.LAR
  else:
    suffix = NOTHING

  processor = get_case_processor(case)
  return processor(join(stem, suffix))
