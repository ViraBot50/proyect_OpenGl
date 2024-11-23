from django.contrib.auth.hashers import must_update_salt
from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians
from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians





class Camera:
    def __init__(self):
        self.camera_pos = Vector3([43.098, 33.957, -0.33214283])
        self.camera_up = Vector3([-0.629, 0.777, -0.008])
        self.camera_right = Vector3([0.013, 0.0, -0.999])
        self.camera_front = ([-0.771, -0.636, -0.006])
        self.jaw = -180  # jaw y
        self.pitch = -39.25  # pitch definen el angulo de vista

        self.mouse_sensitivity = 0.25
        self.jaw = -120
        self.pitch = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)



    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    # Camera method for the WASD movement



    def m_switCamara(self,p_turno):
        if p_turno:
            self.m_whitVision()
        else:
            self.m_blacVision()




    def m_blacVision(self):
        self.camera_pos = Vector3([-43.098, 33.957, -0.33214283])
        self.camera_up = Vector3([0.629, 0.777, -0.008])
        self.camera_right = Vector3([-0.013, 0.0, -0.999])
        self.camera_front = ([-0.771, -0.636, -0.006])
        self.jaw = 359.75  # jaw y
        self.pitch = -39.25  # pitch definen el angulo de vista


        self.update_camera_vectors()


    def m_whitVision(self):
        self.camera_pos = Vector3([43.098, 33.957, -0.33214283])
        self.camera_up = Vector3([-0.629,  0.777, -0.008])
        self.camera_right = Vector3([0.013,0.0,-0.999])
        self.camera_front=([-0.771,-0.636,-0.006])
        self.jaw=-180      # jaw y
        self.pitch=-39.25  # pitch definen el angulo de vista

        self.update_camera_vectors()
