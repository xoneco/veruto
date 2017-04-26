import graphene
import helpers


class Coordinates(graphene.ObjectType):
    lat = graphene.String()
    lng = graphene.String()


class Location(graphene.ObjectType):
    address = graphene.List(graphene.String)
    coordinates = graphene.Field(Coordinates)


class Booking(graphene.ObjectType):
    contact = graphene.String()
    description = graphene.String()
    start_time = graphene.String()
    end_time = graphene.String()
    roomid = graphene.String()
    roomname = graphene.String()
    siteid = graphene.String()
    slotid = graphene.Int()
    weeknumber = graphene.Int()
    phone = graphene.String()


class Room(graphene.ObjectType):
    automated = graphene.String()
    capacity = graphene.Int()
    classification = graphene.String()
    bookings = graphene.List(Booking)
    location = graphene.Field(Location)
    roomid = graphene.String()
    roomname = graphene.String()
    siteid = graphene.String()
    sitename = graphene.String()


class Query(graphene.ObjectType):
    free_rooms = graphene.List(Room, minutes=graphene.Argument(graphene.Int))

    def resolve_free_rooms(self, args, context, info):
        if args.get("minutes"):
            rooms = helpers.fetch_free_rooms(args["minutes"])
        else:
            rooms = helpers.fetch_free_rooms()

        return [
            Room(
                automated=room["automated"],
                capacity=room["capacity"],
                classification=room["classification"],
                bookings=[
                    Booking(
                        contact=booking["contact"],
                        description=booking["description"],
                        start_time=booking["start_time"],
                        end_time=booking["end_time"],
                        roomid=booking["roomid"],
                        roomname=booking["roomname"],
                        siteid=booking["siteid"],
                        slotid=booking["slotid"],
                        weeknumber=booking["weeknumber"],
                        phone=booking["phone"]
                    ) for booking in room["bookings"]
                ],
                location=Location(
                    address=room["location"]["address"],
                    coordinates=Coordinates(
                        lat=room["location"]["coordinates"]["lat"],
                        lng=room["location"]["coordinates"]["lng"]
                    )
                ),
                roomid=room["roomid"],
                roomname=room["roomname"],
                siteid=room["siteid"],
                sitename=room["sitename"]
            ) for room in rooms
        ]
