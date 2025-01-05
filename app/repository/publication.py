from typing import Annotated
from fastapi import Depends, Query
from model.publication import Publication
from repository.base import BaseRepository

class PublicationRepository(BaseRepository[Publication]):

    def get_posts(
        self, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
    ) -> list[Publication]:
        return self.get_all(Publication, offset, limit)

    def get_post_by_id(self, post_id: int) -> Publication:
        return self.get_by_id(Publication, post_id)

    def create_post(self, post: Publication) -> Publication:
        return self.create(post)

    def delete_post(self, post_id: int) -> dict:
        return self.delete(Publication, post_id)