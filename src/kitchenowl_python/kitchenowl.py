"""KitchnOwl API wrapper."""

import asyncio
import logging
from http import HTTPStatus
from typing import Any

import aiohttp
from aiohttp.hdrs import METH_DELETE, METH_GET, METH_HEAD, METH_POST

from .exceptions import KitchenOwlAuthException, KitchenOwlRequestException
from .types import (
    KitchenOwlHouseholdsResponse,
    KitchenOwlItem,
    KitchenOwlShoppingListItem,
    KitchenOwlShoppingListItemsResponse,
    KitchenOwlShoppingListsResponse,
    KitchenOwlUser,
)

_LOGGER = logging.getLogger(__name__)


class KitchenOwl:
    """Unnoficial KitchenOwl API interface.

    Handles communication with the KitchenOwl REST API.

    Attributes:
        session: An ClientSession that handles the communication with the KitchenOwl REST API.
        url: A string representing the URL of the KitchenOwl instance.
        token: A string representing the Long-Lived Access Token for accessing the KitchenOwl API.

    """

    def __init__(self, session: aiohttp.ClientSession, url: str, token: str) -> None:
        """Init function for KitchenOwl API.

        Args:
            session: An ClientSession that handles the communication with the KitchenOwl REST API.
            url: A string representing the URL of the KitchenOwl instance.
            token: A string representing the Long-Lived Access Token for accessing the KitchenOwl API.

        """

        self._session = session

        self._base_url = url
        self._token = token
        self._request_timeout = 25

        self._headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        return_json=False,
    ) -> Any:
        """Perform a HTTP request to the KitchenOwl instance."""

        url = f"{self._base_url}/{path}"

        try:
            async with asyncio.timeout(self._request_timeout):
                r = await self._session.request(
                    method, url, headers=self._headers, params=params, json=json_data
                )
            if r.status == HTTPStatus.UNAUTHORIZED:
                raise KitchenOwlAuthException("Login not possible: not authorized")
            if r.status == HTTPStatus.UNPROCESSABLE_ENTITY:
                raise KitchenOwlAuthException(
                    "Login not possible: authorization incorrect, please check your authorization token."
                )
            r.raise_for_status()

        except aiohttp.ClientError as e:
            raise KitchenOwlRequestException("Error during request") from e

        if return_json:
            content_type = r.headers.get("Content-type", "")
            text = await r.text()
            if "application/json" not in content_type:
                raise KitchenOwlRequestException(
                    "Expected JSON response from server",
                    {"content_type": content_type, "response": text},
                )

            return await r.json()

        return r.status == HTTPStatus.OK

    async def _post(self, path: str, json_data: dict, return_json=False) -> Any:
        """Perform a POST request to the KitchenOwl instance."""

        return await self._request(
            METH_POST, path=path, json_data=json_data, return_json=return_json
        )

    async def _get(self, path: str) -> dict:
        """Perform a GET request to the KitchenOwl instance."""

        return await self._request(METH_GET, path=path, return_json=True)

    async def _head(self, path: str) -> bool:
        """Perform a HEAD request to the KitchenOwl instance."""

        return await self._request(METH_HEAD, path=path, return_json=False)

    async def _delete(self, path: str, json_data: dict) -> bool:
        """Perform a DELETE request to the KitchenOwl instance."""

        return await self._request(METH_DELETE, path=path, json_data=json_data, return_json=False)

    async def test_connection(self) -> bool:
        """Test the kitchenowl token by performing HEAD on the user endpoint.

        Returns:
            A True bool value if a connection to the API endpoint can be established.
            Note: False is never returned as Errors are raised in this case.

        Raises:
            KitchenOwlTimeoutException: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect

        """
        return await self._head("api/user")

    async def get_user_info(self) -> KitchenOwlUser:
        """Return the user informaiton.

        Returns:
            A KitchenOwlUser object containing the information about the user.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect

        """

        return KitchenOwlUser(await self._get("api/user"))

    async def get_households(self) -> KitchenOwlHouseholdsResponse:
        """Return all households for the user.

        Returns:
            A KitchenOwlHouseholdsResponse object containing the information about all households the user is registered for.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect

        """

        return KitchenOwlHouseholdsResponse(await self._get("api/household"))

    async def get_shoppinglists(self, household_id) -> KitchenOwlShoppingListsResponse:
        """Get all shopping lists for the household.

        Args:
            household_id: A positive integer value of the household id.

        Returns:
            A KitchenOwlShoppingListsResponse object containing the information about all shopping lists for the household.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect

        """

        return KitchenOwlShoppingListsResponse(
            await self._get(f"api/household/{household_id}/shoppinglist")
        )

    async def get_shoppinglist_items(self, list_id: int) -> KitchenOwlShoppingListItemsResponse:
        """Get all shopping list items on the list.

        Args:
            list_id: A positive integer value of the shopping list id.

        Returns:
            A KitchenOwlShoppingListsResponse object containing the information about all shopping lists for the household.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect

        """

        return KitchenOwlShoppingListItemsResponse(
            await self._get(f"api/shoppinglist/{list_id}/items")
        )

    async def get_shoppinglist_recent_items(
        self, list_id: int
    ) -> KitchenOwlShoppingListItemsResponse:
        """Get the recent shopping list items for the shopping list.

        Args:
            list_id: A positive integer value of the shopping list id.

        Returns:
            A KitchenOwlShoppingListItemsResponse object containing all items recently used on the shopping list

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect

        """

        return KitchenOwlShoppingListItemsResponse(
            await self._get(f"api/shoppinglist/{list_id}/recent-items")
        )

    async def get_shoppinglist_suggested_items(
        self, list_id: int
    ) -> KitchenOwlShoppingListItemsResponse:
        """Get the suggested shopping list items for the shopping list.

        Args:
            list_id: A positive integer value of the shopping list id.

        Returns:
            A KitchenOwlShoppingListItemsResponse object containing all items that are suggestedfor the shopping list

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect


        """

        return KitchenOwlShoppingListItemsResponse(
            await self._get(f"api/shoppinglist/{list_id}/suggested-items")
        )

    async def add_shoppinglist_item(
        self, list_id: int, item_name: str, item_description: str = ""
    ) -> KitchenOwlShoppingListItem:
        """Add an item to the shopping list by name.

        Args:
            list_id: A positive integer value of the shopping list id.
            item_name: A string representing the name of the item to add to the list.
            item_description: An optional string to add to the description of the item.

        Returns:
            A KitchenOwlShoppingListItem object containing the added item on success.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect


        """

        item = {"name": item_name, "description": item_description}
        return KitchenOwlShoppingListItem(
            await self._post(f"api/shoppinglist/{list_id}/add-item-by-name", item, True)
        )

    async def update_shoppinglist_item_description(
        self, list_id: int, item_id: int, item_description: str
    ) -> KitchenOwlShoppingListItem:
        """Update the description of an item on the shopping list.

        Args:
            list_id: A positive integer value of the shopping list id.
            item_id: An integer as the id of the item to update.
            item_description: The description string to add to the item.

        Returns:
            A KitchenOwlShoppingListItem object containing the updated item on success.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect


        """

        json_data = {"description": item_description}

        return KitchenOwlShoppingListItem(
            await self._post(f"api/shoppinglist/{list_id}/item/{item_id}", json_data, True)
        )

    async def remove_shoppinglist_item(self, list_id: int, item_id: int) -> bool:
        """Remove the item from the shopping list.

        Args:
            list_id: A positive integer value of the shopping list id.
            item_id: An integer as the id of the item to update.

        Returns:
            A bool (True) in case of success.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect


        """

        json_data = {"item_id": item_id}

        return await self._delete(f"api/shoppinglist/{list_id}/item", json_data)

    async def update_item(self, item_id: int, item: KitchenOwlItem) -> KitchenOwlItem:
        """Update an item.

        Args:
            item_id: An integer as the id of the item to update.
            item: A dict containing the item data to update.


        Returns:
             A KitchenOwlShoppingListItem object containing the updated item on success.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect


        """

        return KitchenOwlItem(await self._post(f"api/item/{item_id}", item, True))

    async def delete_item(self, item_id: int) -> KitchenOwlItem:
        """Delete an item.

        Args:
            item_id: An integer as the id of the item to delete.


        Returns:
            A bool (True) in case of success.

        Raises:
            TimeoutError: If the request times out
            KitchenOwlRequestException: If there is an error during the request
            KitchenOwlAuthException: If the token is not provided or incorrect


        """

        return await self._delete(path=f"api/item/{item_id}", json_data={})
