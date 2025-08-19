import datetime
from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paged_response_repo_log_item import PagedResponseRepoLogItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    repo_id: UUID,
    *,
    created_after: Union[None, Unset, datetime.datetime] = UNSET,
    created_before: Union[None, Unset, datetime.datetime] = UNSET,
    page_start: Union[Unset, int] = 0,
    page_size: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_after: Union[None, Unset, str]
    if isinstance(created_after, Unset):
        json_created_after = UNSET
    elif isinstance(created_after, datetime.datetime):
        json_created_after = created_after.isoformat()
    else:
        json_created_after = created_after
    params["created_after"] = json_created_after

    json_created_before: Union[None, Unset, str]
    if isinstance(created_before, Unset):
        json_created_before = UNSET
    elif isinstance(created_before, datetime.datetime):
        json_created_before = created_before.isoformat()
    else:
        json_created_before = created_before
    params["created_before"] = json_created_before

    params["page_start"] = page_start

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/repo/{repo_id}/chat",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PagedResponseRepoLogItem]]:
    if response.status_code == 200:
        response_200 = PagedResponseRepoLogItem.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, PagedResponseRepoLogItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    repo_id: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[None, Unset, datetime.datetime] = UNSET,
    created_before: Union[None, Unset, datetime.datetime] = UNSET,
    page_start: Union[Unset, int] = 0,
    page_size: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, PagedResponseRepoLogItem]]:
    """Get Chat Log

     Retrieve the event log for a repository, including user prompts.

    Args:
        repo_id (UUID):
        created_after (Union[None, Unset, datetime.datetime]):
        created_before (Union[None, Unset, datetime.datetime]):
        page_start (Union[Unset, int]): Page start index Default: 0.
        page_size (Union[Unset, int]): Maximum results per page Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PagedResponseRepoLogItem]]
    """

    kwargs = _get_kwargs(
        repo_id=repo_id,
        created_after=created_after,
        created_before=created_before,
        page_start=page_start,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    repo_id: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[None, Unset, datetime.datetime] = UNSET,
    created_before: Union[None, Unset, datetime.datetime] = UNSET,
    page_start: Union[Unset, int] = 0,
    page_size: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, PagedResponseRepoLogItem]]:
    """Get Chat Log

     Retrieve the event log for a repository, including user prompts.

    Args:
        repo_id (UUID):
        created_after (Union[None, Unset, datetime.datetime]):
        created_before (Union[None, Unset, datetime.datetime]):
        page_start (Union[Unset, int]): Page start index Default: 0.
        page_size (Union[Unset, int]): Maximum results per page Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PagedResponseRepoLogItem]
    """

    return sync_detailed(
        repo_id=repo_id,
        client=client,
        created_after=created_after,
        created_before=created_before,
        page_start=page_start,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    repo_id: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[None, Unset, datetime.datetime] = UNSET,
    created_before: Union[None, Unset, datetime.datetime] = UNSET,
    page_start: Union[Unset, int] = 0,
    page_size: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, PagedResponseRepoLogItem]]:
    """Get Chat Log

     Retrieve the event log for a repository, including user prompts.

    Args:
        repo_id (UUID):
        created_after (Union[None, Unset, datetime.datetime]):
        created_before (Union[None, Unset, datetime.datetime]):
        page_start (Union[Unset, int]): Page start index Default: 0.
        page_size (Union[Unset, int]): Maximum results per page Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PagedResponseRepoLogItem]]
    """

    kwargs = _get_kwargs(
        repo_id=repo_id,
        created_after=created_after,
        created_before=created_before,
        page_start=page_start,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    repo_id: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[None, Unset, datetime.datetime] = UNSET,
    created_before: Union[None, Unset, datetime.datetime] = UNSET,
    page_start: Union[Unset, int] = 0,
    page_size: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, PagedResponseRepoLogItem]]:
    """Get Chat Log

     Retrieve the event log for a repository, including user prompts.

    Args:
        repo_id (UUID):
        created_after (Union[None, Unset, datetime.datetime]):
        created_before (Union[None, Unset, datetime.datetime]):
        page_start (Union[Unset, int]): Page start index Default: 0.
        page_size (Union[Unset, int]): Maximum results per page Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PagedResponseRepoLogItem]
    """

    return (
        await asyncio_detailed(
            repo_id=repo_id,
            client=client,
            created_after=created_after,
            created_before=created_before,
            page_start=page_start,
            page_size=page_size,
        )
    ).parsed
