from typing import Any

from glom import glom


def get_all_values(data: Any, resource_type: str, spec: Any, n_flatten: int) -> Any:
    resource_data = data[resource_type]
    glm = glom(resource_data, spec)

    for i in range(n_flatten):
        glm = [x for y in glm if y for x in y]

    return glm
