import tkinter as tk

def is_clockwise(polygon):
    """Checks if the polygon vertices are ordered clockwise."""
    s = 0.0
    n = len(polygon)
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        s += (p2[0] - p1[0]) * (p2[1] + p1[1])
    return s > 0

def is_point_inside_triangle(p, a, b, c):
    """Returns True if point p is inside the triangle formed by a, b, c."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def triangulate_ear_clipping(vertices):
    """
    Triangulates a simple polygon using the Ear Clipping algorithm.
    Takes an ordered list of points [(x1, y1), (x2, y2), ...]
    Returns a list of triangles, where each triangle is a tuple of 3 points.
    """
    # Create a local copy. Ensure counter-clockwise order for standard math
    poly = list(vertices)
    if is_clockwise(poly):
        poly.reverse()
        
    triangles = []
    
    while len(poly) > 3:
        n = len(poly)
        ear_found = False
        
        for i in range(n):
            prev_pt = poly[(i - 1) % n]
            prev_pt_index = i - 1
            curr_pt = poly[i]
            curr_pt_index = i
            next_pt = poly[(i + 1) % n]
            next_pt_index = i+1
            
            # Check if the vertex forms a convex angle (turns left)
            # Vector 1: curr - prev, Vector 2: next - curr
            cross_product = (curr_pt[0] - prev_pt[0]) * (next_pt[1] - curr_pt[1]) - (curr_pt[1] - prev_pt[1]) * (next_pt[0] - curr_pt[0])
            
            if cross_product <= 0:
                continue  # Reflex angle, cannot be an ear
                
            # Check if any other point of the polygon is inside this test triangle
            is_ear = True
            for j in range(n):
                if j in [(i - 1) % n, i, (i + 1) % n]:
                    continue
                if is_point_inside_triangle(poly[j], prev_pt, curr_pt, next_pt):
                    is_ear = False
                    break
                    
            if is_ear:
                # 'Clip' the ear
                triangles.append((prev_pt, curr_pt, next_pt))
                poly.pop(i)
                ear_found = True
                break
                
        if not ear_found:
            # Fallback for complex/self-intersecting shapes where no valid ear is found
            raise ValueError("Polygon tracking failed. Ensure the polygon is simple and non-self-intersecting.")
            
    # The remaining 3 vertices form the final triangle
    if len(poly) == 3:
        triangles.append((poly[0], poly[1], poly[2]))
        
    return triangles

class GeometryViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry Renderer")
        self.root.geometry("600x500")
        
        # 1. Hard-coded geometry data (A simple house shape)
        self.points = [
            (100, 100), # 1
            (100, 500), # 2
            (500, 500), # 3
            (500, 100), # 4
            (400, 100), # 5
            (400, 400), # 6
            (200, 400), # 7
            (200, 100)  # 8
        ]

        print(triangulate_ear_clipping(self.points))
        
        # Explicit edges connecting the point indices
        self.edges = [
            (0, 1), 
            (1, 2), 
            (2, 3), 
            (3, 4), 
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 0)
        ]
        
        # Explicit face defining the ordering of vertices for shading
        self.faces = [[0, 1, 2],
                      [0, 1, 2],
                      [1, 2, 3]]



        # 2. Setup Tkinter Variables for Checkboxes
        self.show_faces = tk.BooleanVar(value=True)
        self.show_edges = tk.BooleanVar(value=True)
        self.show_points = tk.BooleanVar(value=True)

        # 3. Create the Main UI Layout
        self.create_widgets()
        
        # Initial Render
        self.render_geometry()

    def create_widgets(self):
        # Control Panel Frame (Checkboxes)
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Checkboxes bound to variables and linked to the render function
        cb_faces = tk.Checkbutton(control_frame, text="Render Faces", variable=self.show_faces, command=self.render_geometry)
        cb_faces.pack(side=tk.LEFT, padx=20)

        cb_edges = tk.Checkbutton(control_frame, text="Render Edges", variable=self.show_edges, command=self.render_geometry)
        cb_edges.pack(side=tk.LEFT, padx=20)

        cb_points = tk.Checkbutton(control_frame, text="Render Points", variable=self.show_points, command=self.render_geometry)
        cb_points.pack(side=tk.LEFT, padx=20)

        # Canvas for Drawing
        self.canvas = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def render_geometry(self):
        # Clear the canvas before rebuilding the layers
        self.canvas.delete("all")

        # Layer 1: Render Faces (Draw first so it sits in the background)
        if self.show_faces.get():
            # Flatten the point tuples into a single list [x1, y1, x2, y2...] for create_polygon
            face_coords = []
            for face in self.faces:
                for index in face:
                    face_coords.extend(self.points[index])
                self.canvas.create_polygon(face_coords, fill="#3b5998", outline="")

        # Layer 2: Render Edges
        if self.show_edges.get():
            for edge in self.edges:
                p1 = self.points[edge[0]]
                p2 = self.points[edge[1]]
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="#ffffff", width=2)

        # Layer 3: Render Points (Draw last so dots stay on top)
        if self.show_points.get():
            radius = 5
            for x, y in self.points:
                self.canvas.create_oval(
                    x - radius, y - radius, 
                    x + radius, y + radius, 
                    fill="#ff4d4d", outline="#ffffff"
                )

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryViewer(root)
    root.mainloop()
