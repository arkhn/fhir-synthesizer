from typing import Any

from glom import glom


def glom_getter(data: Any, spec: Any, n_flatten: int) -> Any:
    """Use glom to access a resource or attribute in the input `data`."""
    glm = glom(data, spec)

    for _ in range(n_flatten):
        glm = [x for y in glm if y for x in y]

    return glm
