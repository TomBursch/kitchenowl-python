"""KitchenOwl API types."""

# TypedDict for now as it allows for changes in the API return values

from typing import NotRequired, TypedDict


class KitchenOwlShoppingListCategory(TypedDict):
    """A KitchenOwl category for an item for a shopping list."""

    name: str
    id: int
    ordering: int
    household_id: int
    description: str
    updated_at: int
    created_at: int
    default: bool
    default_key: str


class KitchenOwlItem(TypedDict):
    """A KitchenOwl item for a shopping list."""

    name: str
    id: int
    ordering: NotRequired[int]
    category: NotRequired[KitchenOwlShoppingListCategory]
    category_id: NotRequired[int]
    household_id: NotRequired[int]
    updated_at: NotRequired[int]
    created_at: NotRequired[int]
    default: NotRequired[bool]
    default_key: NotRequired[str]
    icon: NotRequired[str]
    support: NotRequired[int]


class KitchenOwlShoppingListItem(KitchenOwlItem):
    """A KitchenOwl item on a shopping list."""

    description: str


class KitchenOwlShoppingList(TypedDict):
    """A KitchenOwl shopping list."""

    created_at: int
    household_id: int
    id: int
    name: str
    updated_at: int


class KitchenOwlUser(TypedDict):
    """A user entry."""

    admin: bool
    created_at: int
    id: int
    name: str
    owner: bool
    photo: str | None
    updated_at: int
    username: str


class KitchenOwlHousehold(TypedDict):
    """A KitchenOwl household."""

    created_at: int
    default_shopping_list: KitchenOwlShoppingList
    expenses_feature: bool
    id: int
    language: str
    member: list[KitchenOwlUser]
    name: str
    photo: str | None
    planner_feature: bool
    updated_at: int
    view_ordering: list[str]


class KitchenOwlHouseholdsResponse(list[KitchenOwlHousehold]):
    """The households response from KitchenOwl."""


class KitchenOwlShoppingListsResponse(list[KitchenOwlShoppingList]):
    """The shopping lists response from KitchenOwl."""


class KitchenOwlShoppingListItemsResponse(list[KitchenOwlShoppingListItem]):
    """The response for shopping list items from KitchenOwl."""
