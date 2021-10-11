from typing import Any

from glom import glom


def get_all_values(data: Any, spec: Any, n_flatten: int) -> Any:
    glm = glom(data, spec)

    for i in range(n_flatten):
        glm = [x for y in glm if y for x in y]

    return glm
