import pyparsing as _pp


def register_res_parse_rule(cls):
    begin_function_map = _pp.Keyword("BEGIN_FUNCTION_MAP").suppress()
    begin_data_map = _pp.Keyword("BEGIN_DATA_MAP").suppress()
    end_data_map = _pp.Keyword("END_DATA_MAP").suppress()
    end_function_map = _pp.Keyword("END_FUNCTION_MAP").suppress()

    begin_block = _pp.Keyword("begin").suppress()
    end_block = _pp.Keyword("end").suppress()

    semicolon = _pp.Literal(";").suppress()
    valid_metadata_words = _pp.Word(
        _pp.pyparsing_unicode.Korean.alphas + _pp.alphas + _pp.printables + r" \t",
        excludeChars=",;",
    )
    comma_separated_row = _pp.delimitedList(valid_metadata_words) + _pp.Optional(
        semicolon
    )

    type_tab = {
        "char": str,
        "date": str,
        "long": int,
        "int": int,
        "float": float,
        "double": float,
    }

    def parse_field(x):

        cur_type = type_tab[x[3]]
        return [
            [
                x[2],
                {
                    "desc": x[0],
                    "_reserved": x[1],
                    "type": cur_type,
                    "size": cur_type(x[4]),
                },
            ]
        ]

    function_metadata = comma_separated_row.setResultsName("__FUNC_META")
    data_metadata = comma_separated_row.setResultsName("__DATA_META")
    field_metadata = _pp.Dict(comma_separated_row.setParseAction(parse_field))

    data_block = _pp.Group(
        data_metadata
        + begin_block
        + _pp.ZeroOrMore(~end_block + field_metadata)
        + end_block
    )
    data_blocks = _pp.Group(
        begin_data_map + _pp.OneOrMore(data_block) + end_data_map
    ).setResultsName("DATA_BLOCKS")
    function_block = _pp.Group(
        begin_function_map + function_metadata + data_blocks + end_function_map
    ).setResultsName("FUNC_BLOCK")

    cls._parser = function_block
    return cls


@register_res_parse_rule
class ResParser:
    @classmethod
    def parse(cls, content):
        return cls._parser.parseString(content).asDict()
