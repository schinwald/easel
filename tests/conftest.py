from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


def pytest_itemcollected(item: "pytest.Item") -> None:
    if item.config.getoption("verbose") > 0:
        doc = item.function.__doc__  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        if doc:
            lines = doc.strip().splitlines()
            item._nodeid = f"\n\n{'\n'.join(lines)}\n\n"
