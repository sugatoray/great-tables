from __future__ import annotations
from ._gt_data import GTData
from great_tables.gt import _get_column_of_values, GT
from great_tables import GT
from typing import List, Any, Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ._formats import DateStyle, TimeStyle


def _make_one_col_table(vals: Union[Any, List[Any]]) -> GTData:
    """
    Create a one-column table from a list of values.

    Args:
        val_list (Union[Any, List[Any]]): The list of values to be converted into a table.

    Returns:
        GTData: The GTData object representing the one-column table.
    """
    from pandas import DataFrame

    # Upgrade a single value to a list
    if type(vals) != list:
        vals = [vals]

    # Convert the list to a Pandas DataFrame and then to a GTData object
    gt_obj = GT(DataFrame({"x": vals}), auto_align=False)
    return gt_obj


def val_fmt_number(
    x: Union[Any, List[Any]],
    decimals: int = 2,
    n_sigfig: Optional[int] = None,
    drop_trailing_zeros: bool = False,
    drop_trailing_dec_mark: bool = True,
    use_seps: bool = True,
    scale_by: float = 1,
    compact: bool = False,
    pattern: str = "{x}",
    sep_mark: str = ",",
    dec_mark: str = ".",
    force_sign: bool = False,
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format numeric values.

    With numeric values in a list, we can perform number-based formatting so that the values are
    rendered with some level of precision. The following major options are available:

    - decimals: choice of the number of decimal places, option to drop trailing zeros, and a choice
    of the decimal symbol
    - digit grouping separators: options to enable/disable digit separators and provide a choice of
    separator symbol
    - scaling: we can choose to scale targeted values by a multiplier value
    - large-number suffixing: larger figures (thousands, millions, etc.) can be autoscaled and
    decorated with the appropriate suffixes
    - pattern: option to use a text pattern for decoration of the formatted values
    - locale-based formatting: providing a locale ID will result in number formatting specific to
    the chosen locale

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    decimals : int
        The `decimals` values corresponds to the exact number of decimal places to use. A value such
        as `2.34` can, for example, be formatted with `0` decimal places and it would result in
        `"2"`. With `4` decimal places, the formatted value becomes `"2.3400"`. The trailing zeros
        can be removed with `drop_trailing_zeros=True`. If you always need `decimals = 0`, the
        [`val_fmt_integer()`](`great_tables._formats_vals.val_fmt_integer`) function should be
        considered.
    n_sigfig : Optional[int]
        A option to format numbers to *n* significant figures. By default, this is `None` and thus
        number values will be formatted according to the number of decimal places set via
        `decimals`. If opting to format according to the rules of significant figures, `n_sigfig`
        must be a number greater than or equal to `1`. Any values passed to the `decimals` and
        `drop_trailing_zeros` arguments will be ignored.
    drop_trailing_zeros : bool
        A boolean value that allows for removal of trailing zeros (those redundant zeros after the
        decimal mark).
    drop_trailing_dec_mark : bool
        A boolean value that determines whether decimal marks should always appear even if there are
        no decimal digits to display after formatting (e.g., `23` becomes `23.` if `False`). By
        default trailing decimal marks are not shown.
    use_seps : bool
        The `use_seps` option allows for the use of digit group separators. The type of digit group
        separator is set by `sep_mark` and overridden if a locale ID is provided to `locale`. This
        setting is `True` by default.
    scale_by : float
        All numeric values will be multiplied by the `scale_by` value before undergoing formatting.
        Since the `default` value is `1`, no values will be changed unless a different multiplier
        value is supplied.
    compact : bool
        A boolean value that allows for compact formatting of numeric values. Values will be scaled
        and decorated with the appropriate suffixes (e.g., `1230` becomes `1.23K`, and `1230000`
        becomes `1.23M`). The `compact` option is `False` by default.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    sep_mark : str
        The string to use as a separator between groups of digits. For example, using `sep_mark=","`
        with a value of `1000` would result in a formatted value of `"1,000"`. This argument is
        ignored if a `locale` is supplied (i.e., is not `None`).
    dec_mark : str
        The string to be used as the decimal mark. For example, using `dec_mark=","` with the value
        `0.152` would result in a formatted value of `"0,152"`). This argument is ignored if a
        `locale` is supplied (i.e., is not `None`).
    force_sign : bool
        Should the positive sign be shown for positive values (effectively showing a sign for all
        values except zero)? If so, use `True` for this option. The default is `False`, where only
        negative numbers will display a minus sign. This option is disregarded when using accounting
        notation with `accounting = True`.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_number(
        columns="x",
        decimals=decimals,
        n_sigfig=n_sigfig,
        drop_trailing_zeros=drop_trailing_zeros,
        drop_trailing_dec_mark=drop_trailing_dec_mark,
        use_seps=use_seps,
        scale_by=scale_by,
        compact=compact,
        pattern=pattern,
        sep_mark=sep_mark,
        dec_mark=dec_mark,
        force_sign=force_sign,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_integer(
    x: Union[Any, List[Any]],
    use_seps: bool = True,
    scale_by: float = 1,
    compact: bool = False,
    pattern: str = "{x}",
    sep_mark: str = ",",
    force_sign: bool = False,
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format values as integers.

    With numeric values in a list, we can perform number-based formatting so that the input values
    are always rendered as integer values. The following major options are available:

    We can have fine control over integer formatting with the following options:

    - digit grouping separators: options to enable/disable digit separators and provide a choice of
    separator symbol
    - scaling: we can choose to scale targeted values by a multiplier value
    - large-number suffixing: larger figures (thousands, millions, etc.) can be autoscaled and
    decorated with the appropriate suffixes
    - pattern: option to use a text pattern for decoration of the formatted values
    - locale-based formatting: providing a locale ID will result in number formatting specific to
    the chosen locale

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    use_seps : bool
        The `use_seps` option allows for the use of digit group separators. The type of digit group
        separator is set by `sep_mark` and overridden if a locale ID is provided to `locale`. This
        setting is `True` by default.
    scale_by : float
        All numeric values will be multiplied by the `scale_by` value before undergoing formatting.
        Since the `default` value is `1`, no values will be changed unless a different multiplier
        value is supplied.
    compact : bool
        A boolean value that allows for compact formatting of numeric values. Values will be scaled
        and decorated with the appropriate suffixes (e.g., `1230` becomes `1K`, and `1230000`
        becomes `1M`). The `compact` option is `False` by default.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    sep_mark : str
        The string to use as a separator between groups of digits. For example, using `sep_mark=","`
        with a value of `1000` would result in a formatted value of `"1,000"`. This argument is
        ignored if a `locale` is supplied (i.e., is not `None`).
    force_sign : bool
        Should the positive sign be shown for positive values (effectively showing a sign for all
        values except zero)? If so, use `True` for this option. The default is `False`, where only
        negative numbers will display a minus sign. This option is disregarded when using accounting
        notation with `accounting = True`.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_integer(
        columns="x",
        use_seps=use_seps,
        scale_by=scale_by,
        compact=compact,
        pattern=pattern,
        sep_mark=sep_mark,
        force_sign=force_sign,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_scientific(
    x: Union[Any, List[Any]],
    decimals: int = 2,
    n_sigfig: Optional[int] = None,
    drop_trailing_zeros: bool = False,
    drop_trailing_dec_mark: bool = True,
    scale_by: float = 1,
    exp_style: str = "x10n",
    pattern: str = "{x}",
    sep_mark: str = ",",
    dec_mark: str = ".",
    force_sign_m: bool = False,
    force_sign_n: bool = False,
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format values to scientific notation.

    With numeric values in a list, we can perform formatting so that the input values are rendered
    in scientific notation, where extremely large or very small numbers can be expressed in a more
    practical fashion. Here, numbers are written in the form of a mantissa (`m`) and an exponent
    (`n`) with the construction *m* x 10^*n* or *m*E*n*. The mantissa component is a number between
    `1` and `10`. For instance, `2.5 x 10^9` can be used to represent the value 2,500,000,000 in
    scientific notation. In a similar way, 0.00000012 can be expressed as `1.2 x 10^-7`. Due to its
    ability to describe numbers more succinctly and its ease of calculation, scientific notation is
    widely employed in scientific and technical domains.

    We have fine control over the formatting task, with the following options:

    - decimals: choice of the number of decimal places, option to drop trailing zeros, and a choice
    of the decimal symbol
    - scaling: we can choose to scale targeted values by a multiplier value
    - pattern: option to use a text pattern for decoration of the formatted values
    - locale-based formatting: providing a locale ID will result in formatting specific to the
    chosen locale

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    decimals : int
        The `decimals` values corresponds to the exact number of decimal places to use. A value such
        as `2.34` can, for example, be formatted with `0` decimal places and it would result in
        `"2"`. With `4` decimal places, the formatted value becomes `"2.3400"`. The trailing zeros
        can be removed with `drop_trailing_zeros=True`.
    n_sigfig : Optional[int]
        A option to format numbers to *n* significant figures. By default, this is `None` and thus
        number values will be formatted according to the number of decimal places set via
        `decimals`. If opting to format according to the rules of significant figures, `n_sigfig`
        must be a number greater than or equal to `1`. Any values passed to the `decimals` and
        `drop_trailing_zeros` arguments will be ignored.
    drop_trailing_zeros : bool
        A boolean value that allows for removal of trailing zeros (those redundant zeros after the
        decimal mark).
    drop_trailing_dec_mark : bool
        A boolean value that determines whether decimal marks should always appear even if there are
        no decimal digits to display after formatting (e.g., `23` becomes `23.` if `False`). By
        default trailing decimal marks are not shown.
    scale_by : float
        All numeric values will be multiplied by the `scale_by` value before undergoing formatting.
        Since the `default` value is `1`, no values will be changed unless a different multiplier
        value is supplied.
    exp_style : str
        Style of formatting to use for the scientific notation formatting. By default this is
        `"x10n"` but other options include using a single letter (e.g., `"e"`, `"E"`, etc.), a
        letter followed by a `"1"` to signal a minimum digit width of one, or `"low-ten"` for using
        a stylized `"10"` marker.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    sep_mark : str
        The string to use as a separator between groups of digits. For example, using `sep_mark=","`
        with a value of `1000` would result in a formatted value of `"1,000"`. This argument is
        ignored if a `locale` is supplied (i.e., is not `None`).
    dec_mark : str
        The string to be used as the decimal mark. For example, using `dec_mark=","` with the value
        `0.152` would result in a formatted value of `"0,152"`). This argument is ignored if a
        `locale` is supplied (i.e., is not `None`).
    force_sign_m : bool
        Should the plus sign be shown for positive values of the mantissa (first component)? This
        would effectively show a sign for all values except zero on the first numeric component of
        the notation. If so, use `True` (the default for this is `False`), where only negative
        numbers will display a sign.
    force_sign_n : bool
        Should the plus sign be shown for positive values of the exponent (second component)? This
        would effectively show a sign for all values except zero on the second numeric component of
        the notation. If so, use `True` (the default for this is `False`), where only negative
        numbers will display a sign.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_scientific(
        columns="x",
        decimals=decimals,
        n_sigfig=n_sigfig,
        drop_trailing_zeros=drop_trailing_zeros,
        drop_trailing_dec_mark=drop_trailing_dec_mark,
        scale_by=scale_by,
        exp_style=exp_style,
        pattern=pattern,
        sep_mark=sep_mark,
        dec_mark=dec_mark,
        force_sign_m=force_sign_m,
        force_sign_n=force_sign_n,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_percent(
    x: Union[Any, List[Any]],
    decimals: int = 2,
    drop_trailing_zeros: bool = False,
    drop_trailing_dec_mark: bool = True,
    scale_values: bool = True,
    use_seps: bool = True,
    pattern: str = "{x}",
    sep_mark: str = ",",
    dec_mark: str = ".",
    force_sign: bool = False,
    placement: str = "right",
    incl_space: bool = False,
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format values as a percentage.

    With numeric values in a list, we can perform percentage-based formatting. It is assumed the
    input numeric values are proportional values and, in this case, the values will be automatically
    multiplied by `100` before decorating with a percent sign (the other case is accommodated though
    setting `scale_values` to `False`). For more control over percentage formatting, we can use the
    following options:

    - percent sign placement: the percent sign can be placed after or before the values and a space
    can be inserted between the symbol and the value.
    - decimals: choice of the number of decimal places, option to drop trailing zeros, and a choice
    of the decimal symbol
    - digit grouping separators: options to enable/disable digit separators and provide a choice of
    separator symbol
    - value scaling toggle: choose to disable automatic value scaling in the situation that values
    are already scaled coming in (and just require the percent symbol)
    - pattern: option to use a text pattern for decoration of the formatted values
    - locale-based formatting: providing a locale ID will result in number formatting specific to
    the chosen locale

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    decimals : int
        The `decimals` values corresponds to the exact number of decimal places to use. A value such
        as `2.34` can, for example, be formatted with `0` decimal places and it would result in
        `"2"`. With `4` decimal places, the formatted value becomes `"2.3400"`. The trailing zeros
        can be removed with `drop_trailing_zeros=True`.
    drop_trailing_zeros : bool
        A boolean value that allows for removal of trailing zeros (those redundant zeros after the
        decimal mark).
    drop_trailing_dec_mark : bool
        A boolean value that determines whether decimal marks should always appear even if there are
        no decimal digits to display after formatting (e.g., `23` becomes `23.` if `False`). By
        default trailing decimal marks are not shown.
    scale_values : bool
        Should the values be scaled through multiplication by 100? By default this scaling is
        performed since the expectation is that incoming values are usually proportional. Setting to
        `False` signifies that the values are already scaled and require only the percent sign when
        formatted.
    use_seps : bool
        The `use_seps` option allows for the use of digit group separators. The type of digit group
        separator is set by `sep_mark` and overridden if a locale ID is provided to `locale`. This
        setting is `True` by default.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    sep_mark : str
        The string to use as a separator between groups of digits. For example, using `sep_mark=","`
        with a value of `1000` would result in a formatted value of `"1,000"`. This argument is
        ignored if a `locale` is supplied (i.e., is not `None`).
    dec_mark : str
        The string to be used as the decimal mark. For example, using `dec_mark=","` with the value
        `0.152` would result in a formatted value of `"0,152"`). This argument is ignored if a
        `locale` is supplied (i.e., is not `None`).
    force_sign : bool
        Should the positive sign be shown for positive values (effectively showing a sign for all
        values except zero)? If so, use `True` for this option. The default is `False`, where only
        negative numbers will display a minus sign. This option is disregarded when using accounting
        notation with `accounting = True`.
    placement : str
        This option governs the placement of the percent sign. This can be either be `"right"` (the
        default) or `"left"`.
    incl_space : bool
        An option for whether to include a space between the value and the percent sign. The default
        is to not introduce a space character.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_percent(
        columns="x",
        decimals=decimals,
        drop_trailing_zeros=drop_trailing_zeros,
        drop_trailing_dec_mark=drop_trailing_dec_mark,
        scale_values=scale_values,
        use_seps=use_seps,
        pattern=pattern,
        sep_mark=sep_mark,
        dec_mark=dec_mark,
        force_sign=force_sign,
        placement=placement,
        incl_space=incl_space,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_currency(
    x: Union[Any, List[Any]],
    currency: Optional[int] = None,
    use_subunits: bool = True,
    decimals: Optional[int] = None,
    drop_trailing_dec_mark: bool = True,
    use_seps: bool = True,
    scale_by: float = 1,
    pattern: str = "{x}",
    sep_mark: str = ",",
    dec_mark: str = ".",
    force_sign: bool = False,
    placement: str = "left",
    incl_space: bool = False,
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format values as currencies.

    With numeric values, we can perform currency-based formatting with the `val_fmt_currency()`
    function. This supports both automatic formatting with a three-letter currency code. We have
    fine control over the conversion from numeric values to currency values, where we could take
    advantage of the following options:

    - the currency: providing a currency code or common currency name will procure the correct
    currency symbol and number of currency subunits
    - currency symbol placement: the currency symbol can be placed before or after the values
    - decimals/subunits: choice of the number of decimal places, and a choice of the decimal symbol,
    and an option on whether to include or exclude the currency subunits (the decimal portion)
    - digit grouping separators: options to enable/disable digit separators and provide a choice of
    separator symbol
    - scaling: we can choose to scale targeted values by a multiplier value
    - pattern: option to use a text pattern for decoration of the formatted currency values
    - locale-based formatting: providing a locale ID will result in currency formatting specific to
    the chosen locale; it will also retrieve the locale's currency if none is explicitly given

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    currency : Union[str, None]
        The currency to use for the numeric value. This input can be supplied as a 3-letter currency
        code (e.g., `"USD"` for U.S. Dollars, `"EUR"` for the Euro currency).
    use_subunits: bool
        An option for whether the subunits portion of a currency value should be displayed. For
        example, with an input value of `273.81`, the default formatting will produce `"$273.81"`.
        Removing the subunits (with `use_subunits = False`) will give us `"$273"`.
    decimals : int
        The `decimals` values corresponds to the exact number of decimal places to use. This value
        is optional as a currency has an intrinsic number of decimal places (i.e., the subunits).
        A value such as `2.34` can, for example, be formatted with `0` decimal places and if the
        currency used is `"USD"` it would result in `"$2"`. With `4` decimal places, the formatted
        value becomes `"$2.3400"`.
    drop_trailing_dec_mark : bool
        A boolean value that determines whether decimal marks should always appear even if there are
        no decimal digits to display after formatting (e.g., `23` becomes `23.` if `False`). By
        default trailing decimal marks are not shown.
    use_seps : bool
        The `use_seps` option allows for the use of digit group separators. The type of digit group
        separator is set by `sep_mark` and overridden if a locale ID is provided to `locale`. This
        setting is `True` by default.
    scale_by : float
        All numeric values will be multiplied by the `scale_by` value before undergoing formatting.
        Since the `default` value is `1`, no values will be changed unless a different multiplier
        value is supplied.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    sep_mark : str
        The string to use as a separator between groups of digits. For example, using `sep_mark=","`
        with a value of `1000` would result in a formatted value of `"1,000"`. This argument is
        ignored if a `locale` is supplied (i.e., is not `None`).
    dec_mark : str
        The string to be used as the decimal mark. For example, using `dec_mark=","` with the value
        `0.152` would result in a formatted value of `"0,152"`). This argument is ignored if a
        `locale` is supplied (i.e., is not `None`).
    force_sign : bool
        Should the positive sign be shown for positive values (effectively showing a sign for all
        values except zero)? If so, use `True` for this option. The default is `False`, where only
        negative numbers will display a minus sign. This option is disregarded when using accounting
        notation with `accounting = True`.
    placement : str
        The placement of the currency symbol. This can be either be `"left"` (as in `"$450"`) or
        `"right"` (which yields `"450$"`).
    incl_space : bool
        An option for whether to include a space between the value and the currency symbol. The
        default is to not introduce a space character.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_currency(
        columns="x",
        currency=currency,
        use_subunits=use_subunits,
        decimals=decimals,
        drop_trailing_dec_mark=drop_trailing_dec_mark,
        use_seps=use_seps,
        scale_by=scale_by,
        pattern=pattern,
        sep_mark=sep_mark,
        dec_mark=dec_mark,
        force_sign=force_sign,
        placement=placement,
        incl_space=incl_space,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_roman(
    x: Union[Any, List[Any]],
    case: str = "upper",
    pattern: str = "{x}",
) -> List[str]:
    """
    Format values as Roman numerals.

    With numeric values we can transform those to Roman numerals, rounding values as necessary.

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    case : str
        Should Roman numerals should be rendered as uppercase (`"upper"`) or lowercase (`"lower"`)
        letters? By default, this is set to `"upper"`.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_roman(
        columns="x",
        case=case,
        pattern=pattern,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_bytes(
    x: Union[Any, List[Any]],
    standard: str = "decimal",
    decimals: int = 1,
    n_sigfig: Optional[int] = None,
    drop_trailing_zeros: bool = True,
    drop_trailing_dec_mark: bool = True,
    use_seps: bool = True,
    pattern: str = "{x}",
    sep_mark: str = ",",
    dec_mark: str = ".",
    force_sign: bool = False,
    incl_space: bool = True,
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format values as bytes.

    With numeric values in a list, we can transform those to values of bytes with human readable
    units. The `val_fmt_bytes()` function allows for the formatting of byte sizes to either of two
    common representations: (1) with decimal units (powers of 1000, examples being `"kB"` and
    `"MB"`), and (2) with binary units (powers of 1024, examples being `"KiB"` and `"MiB"`). It is
    assumed the input numeric values represent the number of bytes and automatic truncation of
    values will occur. The numeric values will be scaled to be in the range of 1 to <1000 and then
    decorated with the correct unit symbol according to the standard chosen. For more control over
    the formatting of byte sizes, we can use the following options:

    - decimals: choice of the number of decimal places, option to drop trailing zeros, and a choice
    of the decimal symbol
    - digit grouping separators: options to enable/disable digit separators and provide a choice of
    separator symbol
    - pattern: option to use a text pattern for decoration of the formatted values
    - locale-based formatting: providing a locale ID will result in number formatting specific to
    the chosen locale

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    standard: str
        The form of expressing large byte sizes is divided between: (1) decimal units (powers of
        1000; e.g., `"kB"` and `"MB"`), and (2) binary units (powers of 1024; e.g., `"KiB"` and
        `"MiB"`). The default is to use decimal units with the `"decimal"` option. The alternative
        is to use binary units with the `"binary"` option.
    decimals : int
        This corresponds to the exact number of decimal places to use. A value such as `2.34` can,
        for example, be formatted with `0` decimal places and it would result in `"2"`. With `4`
        decimal places, the formatted value becomes `"2.3400"`. The trailing zeros can be removed
        with `drop_trailing_zeros=True`.
    drop_trailing_zeros : bool
        A boolean value that allows for removal of trailing zeros (those redundant zeros after the
        decimal mark).
    drop_trailing_dec_mark : bool
        A boolean value that determines whether decimal marks should always appear even if there are
        no decimal digits to display after formatting (e.g., `23` becomes `23.` if `False`). By
        default trailing decimal marks are not shown.
    use_seps : bool
        The `use_seps` option allows for the use of digit group separators. The type of digit group
        separator is set by `sep_mark` and overridden if a locale ID is provided to `locale`. This
        setting is `True` by default.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    sep_mark : str
        The string to use as a separator between groups of digits. For example, using `sep_mark=","`
        with a value of `1000` would result in a formatted value of `"1,000"`. This argument is
        ignored if a `locale` is supplied (i.e., is not `None`).
    dec_mark : str
        The string to be used as the decimal mark. For example, using `dec_mark=","` with the value
        `0.152` would result in a formatted value of `"0,152"`). This argument is ignored if a
        `locale` is supplied (i.e., is not `None`).
    force_sign : bool
        Should the positive sign be shown for positive values (effectively showing a sign for all
        values except zero)? If so, use `True` for this option. The default is `False`, where only
        negative numbers will display a minus sign. This option is disregarded when using accounting
        notation with `accounting = True`.
    incl_space : bool
        An option for whether to include a space between the value and the currency symbol. The
        default is to not introduce a space character.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_bytes(
        columns="x",
        standard=standard,
        decimals=decimals,
        n_sigfig=n_sigfig,
        drop_trailing_zeros=drop_trailing_zeros,
        drop_trailing_dec_mark=drop_trailing_dec_mark,
        use_seps=use_seps,
        pattern=pattern,
        sep_mark=sep_mark,
        dec_mark=dec_mark,
        force_sign=force_sign,
        incl_space=incl_space,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_date(
    x: Union[Any, List[Any]],
    date_style: DateStyle = "iso",
    pattern: str = "{x}",
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format values as dates.

    Format input values to time values using one of 17 preset date styles. Input can be in the form
    of `date` type or as a ISO-8601 string (in the form of `YYYY-MM-DD HH:MM:SS` or `YYYY-MM-DD`).

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    date_style: str
        The date style to use. By default this is the short name `"iso"` which corresponds to
        ISO 8601 date formatting. There are 41 date styles in total and their short names can be
        viewed using `info_date_style()`.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Formatting with the `date_style` argument
    -----------------------------------------

    We need to supply a preset date style to the `date_style` argument. The date styles are numerous
    and can handle localization to any supported locale. The following table provides a listing of
    all date styles and their output values (corresponding to an input date of `2000-02-29`).

    |    | Date Style            | Output                  |
    |----|-----------------------|-------------------------|
    | 1  | `"iso"`               | `"2000-02-29"`          |
    | 2  | `"wday_month_day_year"`| `"Tuesday, February 29, 2000"`  |
    | 3  | `"wd_m_day_year"`     | `"Tue, Feb 29, 2000"`   |
    | 4  | `"wday_day_month_year"`| `"Tuesday 29 February 2000"`    |
    | 5  | `"month_day_year"`    | `"February 29, 2000"`   |
    | 6  | `"m_day_year"`        | `"Feb 29, 2000"`        |
    | 7  | `"day_m_year"`        | `"29 Feb 2000"`         |
    | 8  | `"day_month_year"`    | `"29 February 2000"`    |
    | 9  | `"day_month"`         | `"29 February"`         |
    | 10 | `"day_m"`             | `"29 Feb"`              |
    | 11 | `"year"`              | `"2000"`                |
    | 12 | `"month"`             | `"February"`            |
    | 13 | `"day"`               | `"29"`                  |
    | 14 | `"year.mn.day"`       | `"2000/02/29"`          |
    | 15 | `"y.mn.day"`          | `"00/02/29"`            |
    | 16 | `"year_week"`         | `"2000-W09"`            |
    | 17 | `"year_quarter"`      | `"2000-Q1"`             |

    We can use the `info_date_style()` function within the console to view a similar table of date
    styles with example output.

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_date(
        columns="x",
        date_style=date_style,
        pattern=pattern,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_time(
    x: Union[Any, List[Any]],
    time_style: TimeStyle = "iso",
    pattern: str = "{x}",
    locale: Union[str, None] = None,
) -> List[str]:
    """
    Format values as times.

    Format input values to time values using one of 5 preset time styles. Input can be in the form
    of `time` values, or strings in the ISO 8601 forms of `HH:MM:SS` or `YYYY-MM-DD HH:MM:SS`.

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.
    time_style: str
        The time style to use. By default this is the short name `"iso"` which corresponds to how
        times are formatted within ISO 8601 datetime values. There are 5 time styles in total and
        their short names can be viewed using `info_time_style()`.
    pattern : str
        A formatting pattern that allows for decoration of the formatted value. The formatted value
        is represented by the `{x}` (which can be used multiple times, if needed) and all other
        characters will be interpreted as string literals.
    locale : str
        An optional locale identifier that can be used for formatting values according the locale's
        rules. Examples include `"en"` for English (United States) and `"fr"` for French (France).

    Formatting with the `time_style` argument
    -----------------------------------------

    We need to supply a preset time style to the `time_style` argument. The time styles are numerous
    and can handle localization to any supported locale. The following table provides a listing of
    all time styles and their output values (corresponding to an input time of `14:35:00`).

    |    | Time Style    | Output                          | Notes         |
    |----|---------------|---------------------------------|---------------|
    | 1  | `"iso"`       | `"14:35:00"`                    | ISO 8601, 24h |
    | 2  | `"iso-short"` | `"14:35"`                       | ISO 8601, 24h |
    | 3  | `"h_m_s_p"`   | `"2:35:00 PM"`                  | 12h           |
    | 4  | `"h_m_p"`     | `"2:35 PM"`                     | 12h           |
    | 5  | `"h_p"`       | `"2 PM"`                        | 12h           |

    We can use the `info_time_style()` function within the console to view a similar table of time
    styles with example output.

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_time(
        columns="x",
        time_style=time_style,
        pattern=pattern,
        locale=locale,
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt


def val_fmt_markdown(
    x: Union[Any, List[Any]],
) -> List[str]:
    """
    Format Markdown text.

    Any Markdown-formatted text can be transformed to HTML when using the `fmt_markdown()` function.

    Parameters
    ----------
    x : Union[Any, List[Any]]
        A list of values to be formatted.

    Returns
    -------
    List[str]
        A list of formatted values is returned.
    """

    gt_obj: GTData = _make_one_col_table(vals=x)

    gt_obj_fmt = gt_obj.fmt_markdown(
        columns="x",
    )

    vals_fmt = _get_column_of_values(gt=gt_obj_fmt, column_name="x", context="html")

    return vals_fmt
