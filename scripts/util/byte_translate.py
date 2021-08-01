import math

__kb = 1024
__mb = __kb * 1024
__gb = __mb * 1024


def __rounding_div(a, b) -> float:
    return math.floor(a / b * 100) / 100


def translate(count: int) -> str:
    if count is None:
        return "-"

    if count >= __gb:
        return f"{__rounding_div(count, __gb)} GB"
    elif count >= __mb:
        return f"{__rounding_div(count, __mb)} MB"
    elif count >= __kb:
        return f"{__rounding_div(count, __kb)} KB"
    elif count > 0:
        return f"{count} B"
    else:
        return "-"
