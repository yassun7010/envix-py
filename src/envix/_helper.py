ENVNAME_PATTERN = r"^[A-Z_]+$"
DOLLAR_ENVNAME_PATTERN = r"^\$[A-Z_]+$"


class Stdout:
    def __repr__(self) -> str:
        return "stdout"
