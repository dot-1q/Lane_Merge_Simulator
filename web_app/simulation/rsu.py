class RSU:

    def __init__(self,id,address,width,height,coords):
        self.id = id
        self.address = address
        self.width = width
        self.height = height
        self.coords = None

    def set_coords(self,coords):
        self.coords = coords

    def send_message(self,message):
        pass