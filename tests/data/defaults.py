"""Constants for KitchenOwl tests."""

TEST_URL = "https://kitchenowltest.local"
TEST_TOKEN = "12345ABCD"

DEFAULT_SHOPPINGLIST_ID_1 = 1
DEFAULT_SHOPPINGLIST_ID_2 = 2

DEFAULT_HOUSEHOLD_ID = 1
TEST_404_HOUSEHOLD_ID = 404

DEFAULT_ITEM_ID_1 = 1
DEFAULT_ITEM_ID_2 = 2

DEFAULT_USER_ID = 1

DEFAULT_HEADERS = {"accept": "application/json", "Authorization": f"Bearer {TEST_TOKEN}"}

DEFAULT_SHOPPINGLIST_RESPONSE = {
    "created_at": 0,
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "id": DEFAULT_SHOPPINGLIST_ID_1,
    "name": f"list_{DEFAULT_SHOPPINGLIST_ID_1}",
    "updated_at": 0
}

DEFAULT_SHOPPINGLIST_RESPONSE_2 = {
    "created_at": 0,
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "id": DEFAULT_SHOPPINGLIST_ID_2,
    "name": f"list_{DEFAULT_SHOPPINGLIST_ID_2}",
    "updated_at": 0
}

DEFAULT_USER_RESPONSE = {
    "admin": True,
    "created_at": 0,
    "expense_balance": 0,
    "id": DEFAULT_USER_ID,
    "name": f"user {DEFAULT_USER_ID}",
    "owner": True,
    "photo": None,
    "updated_at": 0,
    "username": f"user {DEFAULT_USER_ID}"
}

DEFAULT_HOUSEHOLDS_RESPONSE = [
    {
        "created_at": 0,
        "default_shopping_list": DEFAULT_SHOPPINGLIST_RESPONSE,
        "expenses_feature": True,
        "id": DEFAULT_HOUSEHOLD_ID,
        "language": "en",
        "member": [DEFAULT_USER_RESPONSE],
        "name": f"household {DEFAULT_HOUSEHOLD_ID}",
        "photo": None,
        "planner_feature": True,
        "updated_at": 0,
        "view_ordering": ["items","recipes"]
    }
]



DEFAULT_SHOPPINGLIST_ITEM_RESPONSE = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 1,
        "name": "Category 1",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 1,
    "created_at": 0,
    "default": False,
    "default_key": f"item_{DEFAULT_ITEM_ID_1}",
    "description": f"Description {DEFAULT_ITEM_ID_1}",
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_1}",
    "id": DEFAULT_ITEM_ID_1,
    "name": f"item_{DEFAULT_ITEM_ID_1}",
    "ordering": 1,
    "support": 0,
    "updated_at": 0,
}

DEFAULT_SHOPPINGLIST_ITEM_RESPONSE_2 = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 1,
        "name": "Category 1",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 1,
    "created_at": 0,
    "default": False,
    "default_key": f"item_{DEFAULT_ITEM_ID_2}",
    "description": f"Description {DEFAULT_ITEM_ID_2}",
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_2}",
    "id": DEFAULT_ITEM_ID_2,
    "name": f"item_{DEFAULT_ITEM_ID_2}",
    "ordering": 2,
    "support": 0,
    "updated_at": 0,
}

DEFAULT_SUGGESTED_ITEM_RESPONSE = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 1,
        "name": "Category 1",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 1,
    "created_at": 0,
    "default": False,
    "default_key": f"suggested_item_{DEFAULT_ITEM_ID_1}",
    "description": f"Description {DEFAULT_ITEM_ID_1}",
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_1}",
    "id": DEFAULT_ITEM_ID_1,
    "name": f"suggested_item_{DEFAULT_ITEM_ID_1}",
    "ordering": 1,
    "support": 0,
    "updated_at": 0,
}

DEFAULT_SUGGESTED_ITEM_RESPONSE_2 = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 1,
        "name": "Category 1",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 1,
    "created_at": 0,
    "default": False,
    "default_key": f"suggested_item_{DEFAULT_ITEM_ID_2}",
    "description": f"Description {DEFAULT_ITEM_ID_2}",
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_2}",
    "id": DEFAULT_ITEM_ID_2,
    "name": f"suggested_item_{DEFAULT_ITEM_ID_2}",
    "ordering": 2,
    "support": 0,
    "updated_at": 0,
}

UPDATED_SHOPPINGLIST_ITEM_DESCRIPTION = "Description 2"

UPDATED_SHOPPINGLIST_ITEM_RESPONSE = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 1,
        "name": "Category 1",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 1,
    "created_at": 0,
    "default": False,
    "default_key": f"item_{DEFAULT_ITEM_ID_1}",
    "description": UPDATED_SHOPPINGLIST_ITEM_DESCRIPTION,
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_1}",
    "id": DEFAULT_ITEM_ID_1,
    "name": f"item_{DEFAULT_ITEM_ID_1}",
    "ordering": 1,
    "support": 0,
    "updated_at": 0,
}

DEFAULT_ITEM_RESPONSE = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 1,
        "name": "Category 1",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 1,
    "created_at": 0,
    "default": False,
    "default_key": f"item_{DEFAULT_ITEM_ID_1}",
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_1}",
    "id": DEFAULT_ITEM_ID_1,
    "name": f"item_{DEFAULT_ITEM_ID_1}",
    "ordering": 1,
    "support": 0,
    "updated_at": 0,
}

UPDATED_ITEM_RESPONSE = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 2,
        "name": "Category 2",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 2,
    "created_at": 0,
    "default": False,
    "default_key": f"item_{DEFAULT_ITEM_ID_1}",
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_1}",
    "id": DEFAULT_ITEM_ID_1,
    "name": f"item_{DEFAULT_ITEM_ID_1}",
    "ordering": 1,
    "support": 0,
    "updated_at": 0,
}

DEFAULT_ITEM = {
    "category": {
        "created_at": 0,
        "default": False,
        "default_key": "category_1",
        "household_id": DEFAULT_HOUSEHOLD_ID,
        "id": 1,
        "name": "Category 1",
        "ordering": 1,
        "updated_at": 0,
    },
    "category_id": 1,
    "created_at": 0,
    "default": False,
    "default_key": f"item_{DEFAULT_ITEM_ID_1}",
    "household_id": DEFAULT_HOUSEHOLD_ID,
    "icon": f"icon_{DEFAULT_ITEM_ID_1}",
    "id": DEFAULT_ITEM_ID_1,
    "name": f"item_{DEFAULT_ITEM_ID_1}",
    "ordering": 1,
    "support": 0,
    "updated_at": 0,
}
