from typing import Any

__all__ = ["merge_with_template"]


def merge_with_template(
    target: dict[Any, Any], template: dict[Any, Any]
) -> dict[Any, Any]:
    result = target.copy()
    for key, template_value in template.items():
        if key not in result:
            result[key] = template_value
        elif isinstance(template_value, dict) and isinstance(result[key], dict):
            result[key] = merge_with_template(result[key], template_value)
    return result


if __name__ == "__main__":
    template = {
        "name": "unknown",
        "settings": {
            "theme": "light",
            "language": "zh",
            "notifications": {
                "email": True,
                "sms": False,
            },
        },
        "version": 1,
    }

    target = {
        "name": "Alice",
        "settings": {
            "theme": "dark",
            # missing "language" and "notifications"
        },
        # missing "version"
    }

    result = merge_with_template(target, template)
    print(result)
