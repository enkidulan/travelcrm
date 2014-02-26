# -*-coding: utf-8 -*-

import colander

from . import ResourceSchema


class RegionSchema(ResourceSchema):
    country_id = colander.SchemaNode(
        colander.Integer(),
    )
    name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=128)
    )
