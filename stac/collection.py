#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""STAC Collection module."""
import json

from pkg_resources import resource_string

from .catalog import Catalog
from .item import Item, ItemCollection
from .utils import Utils


class Extent(dict):
    """The Extent object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Extent metadata.
        """
        super(Extent, self).__init__(data or {})

    @property
    def spatial(self):
        """:return: the spatial extent."""
        return self['spatial']

    @property
    def temporal(self):
        """:return: the temporal extent."""
        return self['temporal']


class Provider(dict):
    """The Provider Object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Provider metadata.
        """
        super(Provider, self).__init__(data or {})

    @property
    def name(self):
        """:return: the Provider name."""
        return self['name']

    @property
    def description(self):
        """:return: the Provider description."""
        return self['description']

    @property
    def roles(self):
        """:return: the Provider roles."""
        return self['roles']

    @property
    def url(self):
        """:return: the Provider url."""
        return self['url']


class Collection(Catalog):
    """The STAC Collection."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with collection metadata.
        :param validate: true if the Collection should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(Collection, self).__init__(data or {}, validate)
        if self._validate:
            Utils.validate(self)

    @property
    def keywords(self):
        """:return: the Collection list of keywords."""
        return self['keywords']

    @property
    def version(self):
        """:return: the Collection version."""
        return self['version']

    @property
    def license(self):
        """:return: the Collection license."""
        return self['license']

    @property
    def providers(self):
        """:return: the Collection list of providers."""
        return [Provider(provider) for provider in self['providers']]

    @property
    def extent(self):
        """:return: the Collection extent."""
        return Extent(self['extent'])

    @property
    def properties(self):
        """:return: the Collection properties."""
        return self['properties']

    @property
    def _schema(self):
        """:return: the Collection jsonschema."""
        schema = resource_string(__name__, f'jsonschemas/{self.stac_version}/collection.json')
        _schema = json.loads(schema)
        return _schema

    def get_items(self, item_id=None, filter=None):
        """:return: A GeoJSON FeatureCollection of STAC Items from the collection."""
        for link in self['links']:
            if link['rel'] == 'items':
                if item_id is not None:
                    data = Utils._get(f'{link["href"]}/{item_id}')
                    return Item(data, self._validate)
                data = Utils._get(link['href'], params=filter)
                return ItemCollection(data)
        return ItemCollection({})
