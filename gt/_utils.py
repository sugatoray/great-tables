from typing import Optional, List, Any


def heading_has_title(title: Optional[str]) -> bool:
    if title is None:
        return False
    else:
        return True


def heading_has_subtitle(subtitle: Optional[str]) -> bool:
    if subtitle is None:
        return False
    else:
        return True


def _match_arg(x: str, lst: List[str]) -> str:

    # Ensure that `lst` has at least one element
    if len(lst) == 0:
        raise ValueError("The `lst` object must contain at least one element.")

    # Ensure that all elements in `lst` are strings
    if not all(isinstance(el, str) for el in lst):
        raise ValueError("All elements in the `lst` object must be strings.")

    # Ensure that `lst` does not have duplicates by comparing against
    # a set based on `lst` (using `set()` will remove duplicates)
    if len(lst) != len(set(lst)):
        raise ValueError("The `lst` object must contain unique elements.")

    matched = [el for el in lst if x in el]

    # Raise error if there is no match
    if len(matched) == 0:
        raise ValueError(f"The supplied value (`{x}`) is not an allowed option.")

    return matched.pop()


def _assert_str_scalar(x: Any) -> None:
    if type(x).__name__ != "str":
        raise AssertionError(f"The supplied value (`{x}`) is not a string.")


def _assert_str_list(x: Any) -> None:
    if type(x).__name__ != "list":
        raise AssertionError(f"The supplied value (`{x}`) is not a list.")
    if not all(map(lambda x: isinstance(x, str), x)):
        raise AssertionError("Not all elements of the supplied list are strings.")


def _assert_str_in_set(x: str, set: List[str]):
    while x not in set:
        raise AssertionError(f"The string `{x}` is not part of the defined `set`.")

