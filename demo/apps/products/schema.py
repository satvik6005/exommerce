import graphene
from graphene_django import DjangoObjectType
from products.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields=['id','name','desc','available_units','price_per_unit','supplier']


class Query(graphene.ObjectType):
    products=graphene.List(ProductType)
    products_by_name=graphene.List(ProductType,name=graphene.String(required=True))
    products_by_desc=graphene.List(ProductType,desc=graphene.String(required=True))

    def resolve_products(self,info,**kwargs):
        print(Product.objects.all())
        return Product.objects.all()
    def resolve_products_by_name(self,info,name):
        return Product.objects.filter(name=name)
    def resolve_products_by_desc(self,info,desc):
        return Product.objects.filter(desc=desc)

schema = graphene.Schema(query=Query)
