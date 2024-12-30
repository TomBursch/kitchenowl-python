"""Tests for the KitchenOwl API wrapper."""

import asyncio
from typing import Any, AsyncGenerator, Dict, Generator, Literal

import pytest
from aiohttp import ClientSession
from aiohttp.hdrs import METH_DELETE, METH_GET, METH_HEAD, METH_POST
from aioresponses import CallbackResult, aioresponses

from kitchenowl_python.exceptions import KitchenOwlAuthException, KitchenOwlRequestException
from kitchenowl_python.kitchenowl import KitchenOwl
from kitchenowl_python.types import (
    KitchenOwlHouseholdsResponse,
    KitchenOwlItem,
    KitchenOwlShoppingList,
    KitchenOwlShoppingListCategory,
    KitchenOwlShoppingListItem,
    KitchenOwlShoppingListItemsResponse,
    KitchenOwlShoppingListsResponse,
    KitchenOwlUser,
)

from .data.defaults import (
    DEFAULT_HEADERS,
    DEFAULT_HOUSEHOLD_ID,
    DEFAULT_HOUSEHOLDS_RESPONSE,
    DEFAULT_ITEM,
    DEFAULT_ITEM_ID_1,
    DEFAULT_SHOPPINGLIST_ID_1,
    DEFAULT_SHOPPINGLIST_ITEM_RESPONSE,
    DEFAULT_SHOPPINGLIST_RESPONSE,
    DEFAULT_SHOPPINGLIST_RESPONSE_2,
    DEFAULT_USER_RESPONSE,
    TEST_404_HOUSEHOLD_ID,
    TEST_TOKEN,
    TEST_URL,
    UPDATED_ITEM_RESPONSE,
    UPDATED_SHOPPINGLIST_ITEM_DESCRIPTION,
    UPDATED_SHOPPINGLIST_ITEM_RESPONSE,
)


@pytest.fixture
def url():
    """The base URL for testing purposes."""
    return TEST_URL


@pytest.fixture
def token():
    """A long-lived access token for testing purposes."""
    return TEST_TOKEN


@pytest.fixture
async def kitchenowl_api(
    url: Literal["https://kitchenowltest.local"], token: Literal["12345ABCD"]
) -> AsyncGenerator[KitchenOwl, None]:
    """The API client to use in the test interactions."""
    async with ClientSession() as session:
        client = KitchenOwl(session=session, url=url, token=token)
        yield client


@pytest.fixture
def responses() -> Generator[aioresponses, None, None]:
    """Mock responses from aioresponses."""
    with aioresponses() as mock_responses:
        yield mock_responses


@pytest.fixture
def default_shoppinglist() -> KitchenOwlShoppingList:
    """Default item used in update tests."""
    return KitchenOwlShoppingList(DEFAULT_SHOPPINGLIST_RESPONSE)


@pytest.fixture
def default_shoppinglist_2() -> KitchenOwlShoppingList:
    """Another item used in update tests."""
    return KitchenOwlShoppingList(DEFAULT_SHOPPINGLIST_RESPONSE_2)


@pytest.fixture
def default_shoppinglists_response(
    default_shoppinglist: KitchenOwlShoppingList, default_shoppinglist_2: KitchenOwlShoppingList
) -> KitchenOwlShoppingListItemsResponse:
    """Default items on the shopping list response."""
    return KitchenOwlShoppingListsResponse([default_shoppinglist, default_shoppinglist_2])


@pytest.fixture
def default_user_response() -> KitchenOwlUser:
    """Default items on the shopping list response."""
    return KitchenOwlUser(DEFAULT_USER_RESPONSE)


@pytest.fixture
def default_households_response() -> KitchenOwlHouseholdsResponse:
    """Default items on the shopping list response."""
    return KitchenOwlHouseholdsResponse(DEFAULT_HOUSEHOLDS_RESPONSE)


@pytest.fixture
def default_shoppinglist_item() -> KitchenOwlShoppingListItem:
    """Default item used in update tests."""
    return KitchenOwlShoppingListItem(DEFAULT_SHOPPINGLIST_ITEM_RESPONSE)


@pytest.fixture
def default_shoppinglist_item_2() -> KitchenOwlShoppingListItem:
    """Another item used in update tests."""
    return KitchenOwlShoppingListItem(DEFAULT_SHOPPINGLIST_ITEM_RESPONSE)


@pytest.fixture
def default_shoppinglist_items_response(
    default_shoppinglist_item: KitchenOwlShoppingListItem,
    default_shoppinglist_item_2: KitchenOwlShoppingListItem,
) -> KitchenOwlShoppingListItemsResponse:
    """Default items on the shopping list response."""
    return KitchenOwlShoppingListItemsResponse(
        [default_shoppinglist_item, default_shoppinglist_item_2]
    )


@pytest.fixture
def default_suggested_item() -> KitchenOwlShoppingListItem:
    """Suggested item used in update tests."""
    return KitchenOwlShoppingListItem(DEFAULT_SHOPPINGLIST_ITEM_RESPONSE)


@pytest.fixture
def default_suggested_item_2() -> KitchenOwlShoppingListItem:
    """Another suggested item used in update tests."""
    return KitchenOwlShoppingListItem(DEFAULT_SHOPPINGLIST_ITEM_RESPONSE)


@pytest.fixture
def default_suggested_items_response(
    default_suggested_item: KitchenOwlShoppingListItem,
    default_suggested_item_2: KitchenOwlShoppingListItem,
) -> KitchenOwlShoppingListItemsResponse:
    """Suggested items for the shopping list."""
    return KitchenOwlShoppingListItemsResponse([default_suggested_item, default_suggested_item_2])


@pytest.fixture
def default_item() -> KitchenOwlItem:
    """Default item used in update tests."""
    return KitchenOwlItem(DEFAULT_ITEM)


@pytest.fixture
def update_item_response() -> Dict[str, Any]:
    """Response to the updated item."""
    return UPDATED_ITEM_RESPONSE


@pytest.fixture
def update_shoppinglist_item_response() -> Dict[str, Any]:
    """Response to the updated item."""
    return UPDATED_SHOPPINGLIST_ITEM_RESPONSE


@pytest.mark.slow
async def test_timeout_exception(responses: aioresponses, kitchenowl_api: KitchenOwl):
    """Test request timeout."""

    async def response_callback(_: str, **_kwargs: Any) -> CallbackResult:
        """Response handler for this test."""
        await asyncio.sleep(4)
        return CallbackResult(body="Awake!")

    responses.head(
        url=f"{TEST_URL}/api/user",
        status=200,
        callback=response_callback,
    )
    kitchenowl_api._request_timeout = 3  # noqa: SLF001
    with pytest.raises(asyncio.TimeoutError):
        await kitchenowl_api.test_connection()

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/user",
        method=METH_HEAD,
        headers=DEFAULT_HEADERS,
        params=None,
        json=None,
    )


async def test_bad_response_exception(responses: aioresponses, kitchenowl_api: KitchenOwl):
    """Test server responding with non-json."""
    responses.get(
        url=f"{TEST_URL}/api/household/{DEFAULT_HOUSEHOLD_ID}/shoppinglist",
        status=200,
        headers={"Content-Type": "text/html"},
        body="Hello from KitchenOwl",
    )

    with pytest.raises(KitchenOwlRequestException):
        assert await kitchenowl_api.get_shoppinglists(DEFAULT_HOUSEHOLD_ID)


async def test_not_found_exception(responses: aioresponses, kitchenowl_api: KitchenOwl):
    """Test a not found response from KitchenOwl."""
    responses.get(
        url=f"{TEST_URL}/api/household/{TEST_404_HOUSEHOLD_ID}/shoppinglist",
        status=404,
        body="Requested resource not found",
    )
    with pytest.raises(KitchenOwlRequestException):
        await kitchenowl_api.get_shoppinglists(TEST_404_HOUSEHOLD_ID)


async def test_auth_exception(responses: aioresponses, kitchenowl_api: KitchenOwl):
    """Test an authentication error."""
    responses.get(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/recent-items",
        status=401,
        headers={"Content-Type": "application/json"},
        payload={"msg": "Unauthenticated"},
    )

    with pytest.raises(KitchenOwlAuthException):
        await kitchenowl_api.get_shoppinglist_recent_items(DEFAULT_SHOPPINGLIST_ID_1)


async def test_incorrect_token_exception(responses: aioresponses, kitchenowl_api: KitchenOwl):
    """Test a mock response if the token itself is incorrect."""
    responses.get(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/recent-items",
        status=422,
        headers={"Content-Type": "application/json"},
        payload={"msg": "Not enough segments"},
    )

    with pytest.raises(KitchenOwlAuthException):
        await kitchenowl_api.get_shoppinglist_recent_items(DEFAULT_SHOPPINGLIST_ID_1)


async def test_connection_test(responses: aioresponses, kitchenowl_api: KitchenOwl):
    """Test the test_connection request."""
    responses.head(
        url=f"{TEST_URL}/api/user",
        status=200,
        headers={"Content-Type": "application/json"},
    )
    actual = await kitchenowl_api.test_connection()
    assert actual is True


async def test_get_user_snapshot(
    default_user_response: KitchenOwlUser,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test get_user_info to match the snapshot."""
    responses.get(
        url=f"{TEST_URL}/api/user",
        status=200,
        headers={"Content-Type": "application/json"},
        payload=default_user_response,
    )

    actual = await kitchenowl_api.get_user_info()
    assert actual == snapshot

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/user",
        method=METH_GET,
        headers=DEFAULT_HEADERS,
        params=None,
        json=None,
    )


async def test_get_households_snapshot(
    default_households_response: KitchenOwlHouseholdsResponse,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test get_households to match the snapshot."""
    responses.get(
        url=f"{TEST_URL}/api/household",
        status=200,
        headers={"Content-Type": "application/json"},
        payload=default_households_response,
    )

    actual = await kitchenowl_api.get_households()
    assert actual == snapshot

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/household",
        method=METH_GET,
        headers=DEFAULT_HEADERS,
        params=None,
        json=None,
    )


async def test_get_shoppinglists_snapshot(
    default_shoppinglists_response: KitchenOwlShoppingListsResponse,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test get_shoppinglists to match the snapshot."""
    responses.get(
        url=f"{TEST_URL}/api/household/{DEFAULT_HOUSEHOLD_ID}/shoppinglist",
        status=200,
        headers={"Content-Type": "application/json"},
        payload=default_shoppinglists_response,
    )

    actual = await kitchenowl_api.get_shoppinglists(DEFAULT_HOUSEHOLD_ID)
    assert actual == snapshot

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/household/{DEFAULT_HOUSEHOLD_ID}/shoppinglist",
        method=METH_GET,
        headers=DEFAULT_HEADERS,
        params=None,
        json=None,
    )


async def test_get_shoppinglist_items_snapshot(
    default_shoppinglist_items_response: KitchenOwlShoppingListItemsResponse,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test get_shoppinglist_items to match the snapshot."""
    responses.get(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/items",
        status=200,
        headers={"Content-Type": "application/json"},
        payload=default_shoppinglist_items_response,
    )

    actual = await kitchenowl_api.get_shoppinglist_items(DEFAULT_SHOPPINGLIST_ID_1)
    assert actual == snapshot

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/items",
        method=METH_GET,
        headers=DEFAULT_HEADERS,
        params=None,
        json=None,
    )


async def test_get_shoppinglist_suggested_items_snapshot(
    default_suggested_items_response: KitchenOwlShoppingListItemsResponse,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test get_shoppinglist_suggested_items to match the snapshot."""
    responses.get(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/suggested-items",
        status=200,
        headers={"Content-Type": "application/json"},
        payload=default_suggested_items_response,
    )

    actual = await kitchenowl_api.get_shoppinglist_suggested_items(DEFAULT_SHOPPINGLIST_ID_1)
    assert actual == snapshot

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/suggested-items",
        method=METH_GET,
        headers=DEFAULT_HEADERS,
        params=None,
        json=None,
    )


async def test_add_shoppinglist_item(
    default_shoppinglist_item: KitchenOwlShoppingListItem,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test adding an item to a shoping list."""

    responses.post(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/add-item-by-name",
        status=200,
        payload=default_shoppinglist_item,
    )
    testitem = {
        "name": f"item_{DEFAULT_ITEM_ID_1}",
        "description": f"Description {DEFAULT_ITEM_ID_1}",
    }

    actual = await kitchenowl_api.add_shoppinglist_item(
        DEFAULT_SHOPPINGLIST_ID_1, testitem["name"], testitem["description"]
    )

    assert actual == snapshot

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/add-item-by-name",
        method=METH_POST,
        headers=DEFAULT_HEADERS,
        params=None,
        json={"name": testitem["name"], "description": testitem["description"]},
    )


async def test_update_shoppinglist_item_description(
    update_shoppinglist_item_response: Dict[str, Any],
    default_shoppinglist_item: KitchenOwlShoppingListItem,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test updating an item on a shoping list."""

    responses.post(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/item/{default_shoppinglist_item["id"]}",
        status=200,
        payload=update_shoppinglist_item_response,
    )
    default_shoppinglist_item["description"] = UPDATED_SHOPPINGLIST_ITEM_DESCRIPTION
    actual = await kitchenowl_api.update_shoppinglist_item_description(
        DEFAULT_SHOPPINGLIST_ID_1,
        default_shoppinglist_item["id"],
        default_shoppinglist_item["description"],
    )

    assert actual == snapshot

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/item/{default_shoppinglist_item["id"]}",
        method=METH_POST,
        headers=DEFAULT_HEADERS,
        params=None,
        json={"description": default_shoppinglist_item["description"]},
    )


async def test_remove_shoppinglist_item(responses: aioresponses, kitchenowl_api: KitchenOwl):
    """Test removing an item from a shoping list."""

    responses.delete(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/item",
        status=200,
    )

    actual = await kitchenowl_api.remove_shoppinglist_item(
        DEFAULT_SHOPPINGLIST_ID_1, DEFAULT_ITEM_ID_1
    )

    assert actual is True

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/shoppinglist/{DEFAULT_SHOPPINGLIST_ID_1}/item",
        method=METH_DELETE,
        headers=DEFAULT_HEADERS,
        params=None,
        json={"item_id": DEFAULT_ITEM_ID_1},
    )


async def test_update_item_snapshot(
    default_item: KitchenOwlItem,
    update_item_response: Dict[str, Any],
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
    snapshot,
):
    """Test updating an item."""

    responses.post(
        url=f"{TEST_URL}/api/item/{default_item["id"]}",
        status=200,
        payload=update_item_response,
    )
    # Update the category
    default_item["category"] = KitchenOwlShoppingListCategory(id=2)

    actual = await kitchenowl_api.update_item(default_item["id"], default_item)

    assert actual == snapshot
    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/item/{default_item["id"]}",
        method=METH_POST,
        headers=DEFAULT_HEADERS,
        params=None,
        json=default_item,
    )


async def test_delete_item(
    default_item: KitchenOwlItem,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
):
    """Test deleting an item."""

    responses.delete(
        url=f"{TEST_URL}/api/item/{default_item["id"]}",
        status=200,
        payload={"msg": "Done"},
    )

    await kitchenowl_api.delete_item(default_item["id"])

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/item/{default_item["id"]}",
        method=METH_DELETE,
        headers=DEFAULT_HEADERS,
        params=None,
        json={},
    )


async def test_delete_not_found_item(
    default_item: KitchenOwlItem,
    responses: aioresponses,
    kitchenowl_api: KitchenOwl,
):
    """Test deleting an item that is not found."""

    responses.delete(
        url=f"{TEST_URL}/api/item/{default_item["id"]}",
        status=404,
        payload="Requested resource not found",
    )
    with pytest.raises(KitchenOwlRequestException):
        await kitchenowl_api.delete_item(default_item["id"])

    responses.assert_called_once_with(
        url=f"{TEST_URL}/api/item/{default_item["id"]}",
        method=METH_DELETE,
        headers=DEFAULT_HEADERS,
        params=None,
        json={},
    )
