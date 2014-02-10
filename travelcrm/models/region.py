# -*-coding: utf-8 -*-

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    )

from sqlalchemy.orm import (
    relationship,
    backref
)

from ..models import (
    DBSession,
    Base
)


class Region(Base):
    __tablename__ = 'region'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    resource_id = Column(
        Integer,
        ForeignKey(
            'resource.id',
            name="fk_resource_id_region",
            ondelete='cascade',
            onupdate='cascade',
            use_alter=True,
        ),
        nullable=False,
    )
    parent_id = Column(
        Integer(),
        ForeignKey(
            'region.id',
            name='fk_region_parent_id',
            onupdate='cascade',
            ondelete='cascade',
            use_alter=True,
        )
    )
    name = Column(
        String(length=32),
        nullable=False,
    )

    resource = relationship(
        'Resource',
        backref=backref('region', uselist=False),
        uselist=False
    )

    children = relationship(
        'Region',
        backref=backref(
            'parent',
            remote_side=[id]
        ),
        uselist=True,
        order_by='Region.name',
        lazy='dynamic'
    )

    @classmethod
    def get(cls, id):
        if id is None:
            return None
        return DBSession.query(cls).get(id)