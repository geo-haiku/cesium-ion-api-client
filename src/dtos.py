from __future__ import annotations

from typing import Optional

from pydantic.main import BaseModel

from exceptions import MalformedResponseError


class PaginationLinks(BaseModel):
    next: Optional[str]
    prev: Optional[str]

    @staticmethod
    def from_header(link_header: str) -> PaginationLinks:
        pagination_links = PaginationLinks(next=None, prev=None)
        header_els = link_header.split("; ")
        try:
            url1 = header_els[0][1:-1]
            rel1 = header_els[1][5:-1]
        except IndexError:
            raise MalformedResponseError(
                f"`Link` header value is invalid: {link_header=}."
            )
        else:
            try:
                setattr(pagination_links, rel1, url1)
            except ValueError:
                raise MalformedResponseError(
                    f"`Link` header value is invalid: {link_header=}."
                )

        try:
            url2 = header_els[2][1:-1]
            rel2 = header_els[3][5:-1]
        except IndexError:
            pass
        else:
            try:
                setattr(pagination_links, rel2, url2)
            except ValueError:
                raise MalformedResponseError(
                    f"`Link` header value is invalid: {link_header=}."
                )

        return pagination_links
