from rich import print


def print_list_field(msg: str, field: str, response: dict[str, str]):
    if len(response[field]) > 0:
        print(msg)
        for i, value in enumerate(response[field]):
            print(f"  {i + 1}. {value}")
