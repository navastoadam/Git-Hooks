from src.correct_docstrings.utils.config import DocstringFormatterConfig
from src.correct_docstrings.utils.docstring_filters import (
    DocstringFormatter,
    ThirdPersonConverter,
    EmptyLineBetweenDescriptionAndParams,
    RemoveUnwantedPrefixes,
    NoRepeatedWhitespaces,
    EndOfSentencePunctuation,
    EnsureColonInParamDescription,
    IndentMultilineParamDescription,
    SentenceCapitalization,
    LineWrapping,
    DoubleDotFilter,
)


def test_assert_empty_line_between_description_and_param_list():
    # correct docstring: function shouldn't change anything
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    expected = docstring
    formatter = EmptyLineBetweenDescriptionAndParams()

    result = formatter.format(docstring)
    assert result == expected

    # missing empty line between description and param list
    docstring = [
        '   """',
        "    Description",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    formatter = EmptyLineBetweenDescriptionAndParams()

    result = formatter.format(docstring)
    assert result == expected

    # multiple empty lines between description and param list
    docstring = [
        '   """',
        "    Description",
        "",
        "",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    formatter = EmptyLineBetweenDescriptionAndParams()

    result = formatter.format(docstring)
    assert result == expected

    # no params in docstring
    docstring = [
        '"""',
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        '"""',
    ]
    expected = [
        '"""',
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        '"""',
    ]
    formatter = EmptyLineBetweenDescriptionAndParams()

    result = formatter.format(docstring)
    assert result == expected


def test_assert_no_unnecessary_prefixes():
    docstring = [
        '   """',
        "    Description",
        "",
        " ., :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    formatter = RemoveUnwantedPrefixes()
    result = formatter.format(docstring)
    assert result == expected


def test_assert_single_whitespace_after_second_semicolon():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1:   description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    formatter = NoRepeatedWhitespaces()
    result = formatter.format(docstring)
    assert result == expected


def test_assert_line_wrapping():
    docstring = [
        '   """',
        "    This function takes in a dataset of customer information and generates a report that summarizes key metrics and insights about the data. The report includes information about customer demographics, purchasing behavior, and overall satisfaction with the company's products and services.",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2 that is too long to fit on one line and should be wrapped",
        "    :param param3: description of param3",
        "    :return: description of return value that is also too long to fit on one line and should be wrapped",
        '    """',
    ]
    expected = [
        '   """',
        "    This function takes in a dataset of customer",
        "    information and generates a report that summarizes key",
        "    metrics and insights about the data. The report",
        "    includes information about customer demographics,",
        "    purchasing behavior, and overall satisfaction with the",
        "    company's products and services.",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2 that is too long",
        "    to fit on one line and should be wrapped",
        "    :param param3: description of param3",
        "    :return: description of return value that is also too",
        "    long to fit on one line and should be wrapped",
        '    """',
    ]
    formatter = LineWrapping(max_length=60)
    result = formatter.format(docstring)
    assert result == expected


def test_convert_to_third_person():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]

    config = DocstringFormatterConfig()
    converter = ThirdPersonConverter(config.blocking_words, config.modals, config.verbs)

    expected = docstring
    result = converter.format(docstring)
    assert result == expected

    docstring = [
        '   """',
        "    use unlimited option of giving a better life.",
        "   Can do some more specific calculations",
        "",
        "    :param param1: can do many things",
        "    :param param2: is usually employed for taxes",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    uses unlimited option of giving a better life.",
        "   Can do some more specific calculations",
        "",
        "    :param param1: can do many things",
        "    :param param2: is usually employed for taxes",
        "    :return: description of return value",
        '    """',
    ]
    config = DocstringFormatterConfig()
    converter = ThirdPersonConverter(config.blocking_words, config.modals, config.verbs)

    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_end_of_sentence_punctuation():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1?",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3.",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description.",
        "",
        "    :param param1: description of param1?",
        "    :param param2: multiline description ",
        "      of param2.",
        "    :param param3: description of param3.",
        "    :return: description of return value.",
        '    """',
    ]
    converter = EndOfSentencePunctuation()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_ensure_colon_in_param_description():
    # everything fine

    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    converter = EnsureColonInParamDescription()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    # missing colon
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1 description of param1",
        "    :param param2 multiline: description ",
        "      of param2",
        "    :param param3::: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline: description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    converter = EnsureColonInParamDescription()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_indent_multiline_param_description():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    converter = IndentMultilineParamDescription()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "   of param2",
        "    :param param3: description of param3 ",
        "    spanning 1",
        "    spanning 2",
        "    spanning 3 lines!!!",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3 ",
        "      spanning 1",
        "      spanning 2",
        "      spanning 3 lines!!!",
        "    :return: description of return value",
        '    """',
    ]
    converter = IndentMultilineParamDescription()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        '    """',
    ]
    converter = IndentMultilineParamDescription()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    docstring = [
        '   """',
        "        Create an instance.",
        "",
        "    :param reflection_plane: Reflection plane defined by :class:`ReflectionPlane`",
        "      enum.",
        '    """',
    ]

    expected = [
        '   """',
        "        Create an instance.",
        "",
        "    :param reflection_plane: Reflection plane defined by :class:`ReflectionPlane`",
        "      enum.",
        '    """',
    ]
    converter = IndentMultilineParamDescription()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line



def test_double_dot_filter():
    docstring = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "    .. note::",
        "        Some note",
        "        Some note",
        "    Some more text",
        "",
        "    :return: Return value",
        '"""',
    ]
    expected = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "",
        "    .. note::",
        "        Some note",
        "        Some note",
        "",
        "    Some more text",
        "",
        "    :return: Return value",
        '"""',
    ]
    filter_ = DoubleDotFilter()
    result = filter_.format(docstring)
    assert result == expected

    docstring = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "    .. note::",
        "        Some note",
        "        Some note",
        "",
        "    :return: Return value",
        '"""',
    ]
    expected = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "",
        "    .. note::",
        "        Some note",
        "        Some note",
        "",
        "    :return: Return value",
        '"""',
    ]
    filter_ = DoubleDotFilter()
    result = filter_.format(docstring)
    assert result == expected

    docstring = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "    .. note::",
        "        Some note",
        "        Some note",
        '"""',
    ]
    expected = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "",
        "    .. note::",
        "        Some note",
        "        Some note",
        '"""',
    ]
    filter_ = DoubleDotFilter()
    result = filter_.format(docstring)
    assert result == expected


def test_docstring_formatter():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description.",
        "",
        "    :param param1: Description of param1.",
        "    :param param2: Multiline description ",
        "      of param2.",
        "    :param param3: Description of param3.",
        "    :return: Description of return value.",
        '    """',
    ]
    docstring_filters = [
        EmptyLineBetweenDescriptionAndParams(),
        NoRepeatedWhitespaces(),
        RemoveUnwantedPrefixes(),
        EndOfSentencePunctuation(),
        EnsureColonInParamDescription(),
        IndentMultilineParamDescription(),
        SentenceCapitalization(),
    ]
    formatter = DocstringFormatter(docstring_filters)
    result = formatter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line
