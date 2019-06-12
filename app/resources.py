from falcon_autocrud.resource import CollectionResource, SingleResource
from models import Customer


# /customers
class CustomerCollectionResource(CollectionResource):
    model = Customer
    methods = ['GET', 'POST']


# /customers/{id}
class CustomerResource(SingleResource):
    model = Customer
