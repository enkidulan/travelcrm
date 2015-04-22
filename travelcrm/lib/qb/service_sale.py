# -*coding: utf-8-*-
from collections import Iterable

from sqlalchemy import func, literal
from sqlalchemy.orm import aliased
from sqlalchemy.dialects.postgresql import Any

from . import ResourcesQueryBuilder

from ...models import DBSession
from ...models.resource import Resource
from ...models.service_sale import ServiceSale
from ...models.service_item import ServiceItem
from ...models.person import Person
from ...models.invoice import Invoice
from ...models.calculation import Calculation

from ...lib.utils.common_utils import get_base_currency


class ServiceSaleQueryBuilder(ResourcesQueryBuilder):

    def __init__(self, context):
        super(ServiceSaleQueryBuilder, self).__init__(context)
        self._subq_services_price = (
            DBSession.query(
                ServiceSale.id,
                func.sum(ServiceItem.base_price).label('base_price'),
                func.array_agg(ServiceItem.service_id).label('service_arr'),
                func.array_agg(ServiceItem.person_id).label('person_arr'),
            )
            .join(ServiceItem, ServiceSale.services_items)
            .group_by(ServiceSale.id)
            .subquery()
        )
        _ServiceSale = aliased(ServiceSale)
        self._subq_calculations = (
            DBSession.query(Calculation)
            .join(ServiceItem, Calculation.service_item)
            .join(_ServiceSale, ServiceItem.service_sale)
            .filter(_ServiceSale.id == ServiceSale.id)
            .exists()
        )
        self._fields = {
            'id': ServiceSale.id,
            '_id': ServiceSale.id,
            'deal_date': ServiceSale.deal_date,
            'customer': Person.name,
            'base_price': self._subq_services_price.c.base_price,
            'base_currency': literal(get_base_currency()),
            'invoice_id': Invoice.id,
            'calculation': self._subq_calculations
        }
        self._simple_search_fields = [
            Person.name,
        ]
        self.build_query()

    def build_query(self):
        self.build_base_query()
        self.query = (
            self.query
            .join(ServiceSale, Resource.service_sale)
            .join(Person, ServiceSale.customer)
            .join(
                self._subq_services_price,
                self._subq_services_price.c.id == ServiceSale.id
            )
            .outerjoin(Invoice, ServiceSale.invoice)
        )
        super(ServiceSaleQueryBuilder, self).build_query()

    def filter_id(self, id):
        assert isinstance(id, Iterable), u"Must be iterable object"
        if id:
            self.query = self.query.filter(ServiceSale.id.in_(id))

    def advanced_search(self, **kwargs):
        super(ServiceSaleQueryBuilder, self).advanced_search(**kwargs)
        if 'person_id' in kwargs:
            self._filter_person(kwargs.get('person_id'))
        if 'service_id' in kwargs:
            self._filter_service(kwargs.get('service_id'))
        if 'price_from' in kwargs or 'price_to' in kwargs:
            self._filter_price(
                kwargs.get('price_from'), kwargs.get('price_to')
            )
        if 'sale_from' in kwargs or 'sale_to' in kwargs:
            self._filter_sale_date(
                kwargs.get('sale_from'), kwargs.get('sale_to')
            )

    def _filter_person(self, person_id):
        if person_id:
            self.query = self.query.filter(
                Any(int(person_id), self._subq_services_price.c.person_arr),
            )

    def _filter_service(self, service_id):
        if service_id:
            self.query = self.query.filter(
                Any(int(service_id), self._subq_services_price.c.service_arr),
            )

    def _filter_price(self, price_from, price_to):
        if price_from:
            self.query = self.query.filter(
                self._subq_services_price.c.base_price >= price_from
            )
        if price_to:
            self.query = self.query.filter(
                self._subq_services_price.c.base_price <= price_to
            )

    def _filter_sale_date(self, date_from, date_to):
        if date_from:
            self.query = self.query.filter(
                ServiceSale.deal_date >= date_from
            )
        if date_to:
            self.query = self.query.filter(
                ServiceSale.deal_date <= date_to
            )