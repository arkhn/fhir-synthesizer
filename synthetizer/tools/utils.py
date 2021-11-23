from typing import Any

from glom import glom


def glom_getter(data: Any, spec: Any, n_flatten: int) -> Any:
    """Use glom to access a resource or attribute in the input `data` and flatten it, if needed."""
    glm = glom(data, spec)

    for _ in range(n_flatten):
        glm = [x for y in glm if y for x in y]

    return glm


def int_round(x: int, n: int) -> int:
    """Return the multiple of `n` the closest to the integer `x`."""
    return n * round(x / n)
