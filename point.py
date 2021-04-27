class Boundary_Point:
    coord_tl = None #top left point
    coord_br = None #bottom right point
    def __init__(self, coord_top_left, coord_bottop_right) -> None:
        self.coord_tl = coord_top_left
        self.coord_br = coord_bottop_right
    
    def get_mid_point(self):
        if isinstance(self.coord_tl, tuple) and isinstance(self.coord_br, tuple):
            return (int((self.coord_br[0] + self.coord_tl[0])/2), 
                int((self.coord_br[1] + self.coord_tl[1])/2))
            
        else:
            raise "type error"