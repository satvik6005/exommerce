import graphene
from graphene_django import DjangoObjectType
from cart.models import cart
from users.models import User

class cart(DjangoObjectType):
    class Meta:
        model=cart
        fields=['product','user','quantity']

class Query(graphene.ObjectType):
    carts=graphene.List(cart,users=graphene.Int(required=True))

    def resolve_carts(self,info,users):
        print("i am runnning")
        return cart.objects.filter(user=User.objects.get(id=users))


schema = graphene.Schema(query=Query)
