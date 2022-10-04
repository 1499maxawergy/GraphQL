import graphene

from graphene_django.types import DjangoObjectType, ObjectType
from cars.models import Car

class CarType(DjangoObjectType):
    class Meta:
        model = Car


class Query(ObjectType):
    car = graphene.Field(CarType, id=graphene.Int())
    cars = graphene.List(CarType)

    def resolve_car(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Car.objects.get(pk=id)

        return None

    def resolve_cars(self, info, **kwargs):
        return Car.objects.all()


class CarInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    brand = graphene.String()
    price = graphene.Int()
    age = graphene.Int()


class CreateCar(graphene.Mutation):
    class Arguments:
        input = CarInput(required=True)
    ok = graphene.Boolean()
    car = graphene.Field(CarType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        car_instance = Car(
            title=input.title,
            brand=input.brand,
            price=input.price,
            age=input.age
            )
        car_instance.save()
        return CreateCar(ok=ok, car=car_instance)


class UpdateCar(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CarInput(required=True)
    ok = graphene.Boolean()
    car = graphene.Field(CarType)


    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        car_instance = Car.objects.get(pk=id)
        if car_instance:
            ok = True
            car_instance = Car(
            title=input.title,
            brand=input.brand,
            price=input.price,
            age=input.age
            )
            car_instance.save()
            return UpdateCar(ok=ok, actor=car_instance)
        return UpdateCar(ok=ok, actor=None)


class Mutation(graphene.ObjectType):
    create_car = CreateCar.Field()
    update_car = UpdateCar.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)