class OBU:

    def __init__(self,name,id,address,height,width,route):
        self.name = name
        self.id = id
        self.address=address
        self.route = route
        self.height = height
        self.width = width
        self.coords = route.get_position()
        self.state = "Gathering Info"
        self.speed = 100

    def set_coords(self,coords):
        self.coords = coords

    def set_state(self,state):
        self.state = state

    def set_speed(self,speed):
        self.speed = speed
    
    def set_route(self,route):
        self.route = route

    def accelerate(self):
        pass

    def decelerate(self):
        pass
    
    def send_message(self,message):
        pass

    def __repr__(self) -> str:
        return "Name: " + self.name + " OBU ID[" + str(self.id) + "] | Address: " + self.address + " | State: " + self.state + "\n"