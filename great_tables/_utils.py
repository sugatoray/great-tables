from typing import Optional, Union, List, Any
import pandas as pd
import json
import re


def heading_has_title(title: Optional[str]) -> bool:
    return title is not None


def heading_has_subtitle(subtitle: Optional[str]) -> bool:
    return subtitle is not None


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


def _assert_list_is_subset(x: List[Any], set_list: List[Any]) -> None:
    if not set(x).issubset(set(set_list)):
        raise AssertionError("The columns provided are not present in the table.")

    return


def _str_scalar_to_list(x: str):
    _assert_str_scalar(x)
    return [x]


def _unique_set(x: Union[List[Any], None]) -> Union[List[Any], None]:
    if x is None:
        return None
    return list({k: True for k in x})


def _as_css_font_family_attr(fonts: List[str], value_only: bool = False) -> str:
    fonts_w_spaces = list(map(lambda x: f"'{x}'" if " " in x else x, fonts))

    fonts_str = ", ".join(fonts_w_spaces)

    if value_only is True:
        return fonts_str

    return f"font-family: {fonts_str};"


def _object_as_dict(v: Any) -> Any:
    try:
        return v.object_as_dict()
    except Exception:
        pass
    if type(v) == pd.DataFrame:
        return v.to_dict()
    if type(v) in [tuple, list]:
        return list(_object_as_dict(i) for i in v)
    if type(v) == dict:
        return dict((k, _object_as_dict(val)) for (k, val) in v.items())
    if type(v) == type(_object_as_dict):  # FIXME figure out how to get "function"
        return f"<function {v.__name__}>"
    try:
        d = vars(v)
    except TypeError:
        try:
            json.dumps(v)
        except TypeError:
            return "JSON_UNSERIALIZABLE"
        return v
    return dict((k, _object_as_dict(v)) for (k, v) in d.items())


def prettify_gt_object(v: Any) -> str:
    return json.dumps(_object_as_dict(v), indent=2)


def _collapse_list_elements(lst, separator=""):
    """
    Concatenates all elements of a list into a single string, separated by a given separator.

    Args:
        lst (list): The list to be collapsed.
        separator (str, optional): The separator to be used. Defaults to "".

    Returns:
        str: The collapsed string.
    """
    return separator.join(lst)


def _insert_into_list(lst: List[Any], el: Any) -> List[Any]:
    """
    Inserts an element into the beginning of a list and returns the updated list.

    Args:
        lst (List[Any]): The list to insert the element into.
        el (Any): The element to insert.

    Returns:
        List[Any]: The updated list with the element inserted at the beginning.
    """
    lst.insert(0, el)
    return lst


def _str_replace(string: str, pattern: str, replace: str) -> str:
    return string.replace(pattern, replace)


def _str_detect(string: str, pattern: str) -> bool:
    return bool(re.match(pattern, string))
