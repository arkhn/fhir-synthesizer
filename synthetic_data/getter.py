from typing import Any

from glom import glom


def get_all_values(data: Any, resource_type: str, spec: Any, all_pages: bool = False) -> Any:
    resource_data = data[resource_type]
    glm = glom(resource_data, spec)

    glm = [x for y in glm for x in y]
    glm = [x for y in glm for x in y]
    if all_pages:
        glm = [x for y in glm for x in y]

    return glm
