import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader

from camera import Camera
from Ajedrez import reglas

cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False #borrar after
a_letters=[glfw.KEY_A,glfw.KEY_B,glfw.KEY_C,glfw.KEY_D,glfw.KEY_E,glfw.KEY_F,glfw.KEY_G,glfw.KEY_H]
a_numbers=[glfw.KEY_1,glfw.KEY_2,glfw.KEY_3,glfw.KEY_4,glfw.KEY_5,glfw.KEY_6,glfw.KEY_7,glfw.KEY_8]

a_moviValidos=[]
a_pieces=[["p",1,0],["p",1,1],["p",1,2],["p",1,3],["p",1,4],["p",1,5],["p",1,6],["p",1,7],
          ["t",0,0],["n",0,1],["b",0,2],["q",0,3],["k",0,4],["b",0,5],["n",0,6],["t",0,7],
          ["P",6,0],["P",6,1],["P",6,2],["P",6,3],["P",6,4],["P",6,5],["P",6,6],["P",6,7],
          ["T",7,0],["N",7,1],["B",7,2],["Q",7,3],["K",7,4],["B",7,5],["N",7,6],["T",7,7]
          ]
a_reglas=reglas(a_pieces)
a_piezSeleccionada=None
a_selection=[-1,-1]
a_newPosition=[-1,-1]
a_turno=True
a_bandCargDatos=True

# -------------------Codigos de eventos-----------------------------------
def m_selePiecEvents(key, action):

    for v_number in a_numbers:
        if key==v_number and action==glfw.PRESS:
            if a_selection[1]!=-1:
                a_selection[0]=v_number-49


    for v_letter in a_letters:
        if key==v_letter and action==glfw.PRESS:
            a_selection[1]=v_letter-65
        if key==v_letter and action==glfw.RELEASE:
            a_selection[1]=-1


    if a_selection[0]!=-1 and a_selection[1]!=-1:
        a_moviValidos.append(a_selection)


def m_seleMoviEvents(key, action):

    for v_number in a_numbers:
        if key==v_number and action==glfw.PRESS:
            if a_newPosition[1]!=-1:
                a_newPosition[0]=v_number-49


    for v_letter in a_letters:
        if key==v_letter and action==glfw.PRESS:
            a_newPosition[1]=v_letter-65
        elif key==v_letter and action==glfw.RELEASE:
            a_newPosition[1]=-1


def m_resetearJugada():
    global a_piezSeleccionada,a_bandCargDatos
    a_moviValidos.clear()
    a_selection[0] = -1
    a_selection[1] = -1
    a_newPosition[0] = -1
    a_newPosition[1] = -1
    a_piezSeleccionada = None
    a_bandCargDatos = True

def m_hacePromocion():
    global a_piezSeleccionada,a_newPosition

    if a_piezSeleccionada[0]=='p' and a_newPosition[0]==7:
        a_piezSeleccionada[0]='q'
    elif a_piezSeleccionada[0]=='P' and a_newPosition[0]==0:
        a_piezSeleccionada[0]='Q'


def m_haceMovimiento():
    global a_piezSeleccionada,a_moviValidos,a_turno,a_bandCargDatos
    v_auxiliar=None
    for v_moviValido in a_moviValidos:

        print(v_moviValido," ",a_newPosition)
        if v_moviValido[len(v_moviValido)-2]==a_newPosition[0] and v_moviValido[len(v_moviValido)-1]==a_newPosition[1]:
            v_auxiliar=v_moviValido

    if v_auxiliar is not None:
        a_piezSeleccionada[1] = a_newPosition[0]
        a_piezSeleccionada[2] = a_newPosition[1]
        m_hacePromocion()
        m_resetearJugada()
        a_turno = not a_turno




        cam.m_switCamara(a_turno)
        if len(v_auxiliar)==3:
            a_pieces.remove(v_auxiliar)


    else:
        print("no es valido")

    a_newPosition[0]=-1
    a_newPosition[1]=-1



def key_input_clb(window, key, scancode, action, mode):

    global left, right, forward, backward,a_piezSeleccionada,a_moviValidos,a_turno,a_bandCargDatos

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_BACKSPACE and action == glfw.PRESS:
        m_resetearJugada()

    #LLamando eventos de seleccion de piezas
    if  a_selection[0] == -1 or a_selection[1] < -1:
        m_selePiecEvents(key, action)
    #verificacion si hay una pieza en la casilla seleccionada
    elif a_piezSeleccionada is None:
        a_piezSeleccionada=a_reglas.obtener_pieza_en(a_selection[0], a_selection[1])

        if a_piezSeleccionada is None:
            a_piezSeleccionada=[-1]

    #Inicializando lista de movimientos posibles
    elif a_piezSeleccionada[0]!=-1 and a_bandCargDatos:


        v_moviValidos=a_reglas.movimientos_validos(a_piezSeleccionada[0], a_piezSeleccionada[1], a_piezSeleccionada[2])

        if len(v_moviValidos)!=0:

            if str(a_piezSeleccionada[0]).islower() and a_turno or str(a_piezSeleccionada[0]).isupper() and a_turno==False:
                a_moviValidos.clear()
                a_moviValidos.extend(v_moviValidos)
                a_bandCargDatos=False

    #seleccion de pieza a mover
    elif isinstance(a_piezSeleccionada[0],str):

        if a_newPosition[0]==-1 or a_newPosition[1]==-1:
            m_seleMoviEvents(key, action)
        else:
            m_haceMovimiento()
    else:
        print("No es una pieza")

"""""
    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False
"""





def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.05)
    if right:
        cam.process_keyboard("RIGHT", 0.05)
    if forward:
        cam.process_keyboard("FORWARD", 0.05)
    if backward:
        cam.process_keyboard("BACKWARD", 0.05)


# ------------the mouse position callback function-----------------



# the window resize callback function
def window_resize_clb(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

def m_getIndices(VAO,VBO,source):
    object_indices, object_buffer = ObjLoader.load_model(source)
    glBindVertexArray(VAO)
    # cube Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, object_buffer.nbytes, object_buffer, GL_STATIC_DRAW)

    # cube vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(0))
    # cube textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(12))
    # cube normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    return object_indices




vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""
#---------------------------------------------------------------------------------------------------

#************************Cargador de piezas****************************
def m_loadPieces():
    # VAO and VBO
    VAO = glGenVertexArrays(9)
    VBO = glGenBuffers(9)

    pawn_indices=m_getIndices(VAO[0],VBO[0],"finalPieces/pawn.obj")
    tower_indices=m_getIndices(VAO[1],VBO[1],"finalPieces/tower.obj")
    knight_indices=m_getIndices(VAO[2],VBO[2],"finalPieces/Knight.obj")
    bishop_indices=m_getIndices(VAO[3],VBO[3],"finalPieces/bishop.obj")
    queen_indices=m_getIndices(VAO[4],VBO[4],"finalPieces/queen.obj")
    king_indices=m_getIndices(VAO[5],VBO[5],"finalPieces/king.obj")
    floor_indices=m_getIndices(VAO[6],VBO[6],"objetos/floor.obj")
    fondo_indices=m_getIndices(VAO[7],VBO[7],"objetos/fondo.obj")
    quad_indices=m_getIndices(VAO[8],VBO[8],"objetos/quad.obj")

    textures = glGenTextures(5)
    load_texture("textures/blancas.jpg", textures[0])
    load_texture("textures/negras.jpg", textures[1])
    load_texture("textures/tableroFinal.jpg", textures[2])
    load_texture("textures/fondo.jpg",textures[3])
    load_texture("textures/quad_texture.jpg",textures[4])
    return VAO,textures,[pawn_indices, tower_indices, knight_indices,bishop_indices,
                         queen_indices,king_indices,quad_indices],[floor_indices,fondo_indices]





def m_getFigure(p_figure):
    v_respuesta=[]#piece,texture
    if p_figure == "p":
        v_respuesta=[0,0]
    elif p_figure == "P":
        v_respuesta=[0,1]
    elif p_figure == "t":
        v_respuesta=[1,0]
    elif p_figure == "T":
        v_respuesta=[1,1]
    elif p_figure == "n":
        v_respuesta=[2,0]
    elif p_figure == "N":
        v_respuesta=[2,1]
    elif p_figure == "b":
        v_respuesta=[3,0]
    elif p_figure == "B":
        v_respuesta=[3,1]
    elif p_figure=="q":
        v_respuesta=[4,0]
    elif p_figure=="Q":
        v_respuesta=[4,1]
    elif p_figure=="k":
        v_respuesta=[5,0]
    elif p_figure=="K":
        v_respuesta=[5,1]

    return v_respuesta

#Generacion de Quads para mostrar movimientos validos
def m_geneQuads(p_coorX,p_coorY,p_indices):
    v_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([[18.6 - 5.28 * p_coorX, 0, 18.6 - 5.28 * p_coorY]]))

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glBindVertexArray(VAO[8])  # 0 is piece
    glBindTexture(GL_TEXTURE_2D, textures[4])  # 1 is texture
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, v_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(p_indices))  # 0 indices of pieces
#---------------------------------------------------------------------------------------




#------------------------Cragado del juego------------------------------

# creating the window
window = glfw.create_window(WIDTH, HEIGHT, "Chess Master", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize_clb)
# set the mouse position callback
#glfw.set_cursor_pos_callback(window, mouse_look_clb)
# set the keyboard input callback
glfw.set_key_callback(window, key_input_clb)
# capture the mouse cursor
#******************************Cursor********************************************************************
#glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
#*************************************************************************************************

# make the context current
glfw.make_context_current(window)




shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

glUseProgram(shader)
glClearColor(1, 1, 1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)


model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


floor_pos=pyrr.matrix44.create_from_translation(pyrr.Vector3([[0,0,0]]))
VAO,textures,size,area_indices=m_loadPieces()






# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    view = cam.get_view_matrix()

    # draw the fondo
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glBindVertexArray(VAO[7])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(area_indices[1]))

    #print(a_newPosition)
    # draw the floor
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glBindVertexArray(VAO[6])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(area_indices[0]))

    #print(a_selection)

    for data in a_pieces:
        piece_data=m_getFigure(data[0])

        v_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([[18.5-5.28*data[1], 0, 18.5-5.28*data[2]]]))

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glBindVertexArray(VAO[piece_data[0]]) #0 is piece
        glBindTexture(GL_TEXTURE_2D, textures[piece_data[1]]) #1 is texture
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, v_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(size[piece_data[0]])) #0 indices of pieces

    #movimientos validos
    for v_mov in a_moviValidos:
        m_geneQuads(v_mov[len(v_mov)-2],v_mov[len(v_mov)-1],size[6])




    glfw.swap_buffers(window)




# terminate glfw, free up allocated resources
glfw.terminate()