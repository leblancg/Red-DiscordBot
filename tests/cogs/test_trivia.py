import yaml


def test_trivia_lists():
    from redbot.cogs.trivia import get_core_lists

    list_names = get_core_lists()
    assert list_names
    problem_lists = []
    for l in list_names:
        with l.open(encoding="utf-8") as f:
            try:
                dict_ = yaml.safe_load(f)
            except yaml.error.YAMLError as e:
                problem_lists.append((l.stem, "YAML error:\n{!s}".format(e)))
            else:
                for key in list(dict_.keys()):
                    if key == "CONFIG":
                        if not isinstance(dict_[key], dict):
                            problem_lists.append((l.stem, "CONFIG is not a dict"))
                    elif key == "AUTHOR":
                        if not isinstance(dict_[key], str):
                            problem_lists.append((l.stem, "AUTHOR is not a string"))
                    else:
                        if not isinstance(dict_[key], list):
                            problem_lists.append(
                                (l.stem, "The answers for '{}' are not a list".format(key))
                            )
    if problem_lists:
        msg = ""
        for l in problem_lists:
            msg += "{}: {}\n".format(l[0], l[1])
        raise TypeError("The following lists contain errors:\n" + msg)


def test_trivia_lists_schema():
    from redbot.cogs.trivia import get_core_lists
    from schema import Schema, Optional, Or, SchemaError

    schema = Schema(
        {
            Optional("AUTHOR"): str,
            Optional("CONFIG"): {
                Optional("max_score"): int,
                Optional("timeout"): Or(int, float),
                Optional("delay"): Or(int, float),
                Optional("bot_plays"): bool,
                Optional("reveal_answer"): bool,
                Optional("payout_multiplier"): Or(int, float),
            },
            str: [
                str,
                int,
                bool,
                float,
            ],
        }
    )
    list_names = get_core_lists()
    assert list_names
    problem_lists = []
    for l in list_names:
        with l.open(encoding="utf-8") as f:
            try:
                dict_ = yaml.safe_load(f)
            except yaml.error.YAMLError as e:
                problem_lists.append((l.stem, "YAML error:\n{!s}".format(e)))
            else:
                try:
                    schema.validate(dict_)
                except SchemaError as e:
                    problem_lists.append((l.stem, "SCHEMA error:\n{!s}".format(e)))
    if problem_lists:
        msg = ""
        for l in problem_lists:
            msg += "{}: {}\n".format(l[0], l[1])
        raise TypeError("The following lists contain errors:\n" + msg)
