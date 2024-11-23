class reglas:
    a_pieces = []


    def __init__(self, p_pieces):
        self.a_pieces = p_pieces


    def obtener_pieza_en(self, fila, columna):
        for v_pieza in self.a_pieces:
            if v_pieza[1] == fila and v_pieza[2] == columna:
                return v_pieza
        return None

    def movimientos_validos(self, tipo, fila, columna):
        if tipo.lower() == 'p':
            return self.movimientos_peon(tipo, fila, columna)
        elif tipo.lower() == 't':
            return self.movimientos_torre(tipo,fila, columna)
        elif tipo.lower() == 'n':
            return self.movimientos_caballo(tipo,fila, columna)
        elif tipo.lower() == 'b':
            return self.movimientos_alfil(tipo,fila, columna)
        elif tipo.lower() == 'q':
            return self.movimientos_reina(tipo,fila, columna)
        elif tipo.lower() == 'k':
            return self.movimientos_rey(tipo,fila, columna)
        return []


    def m_isEnemy(self,p_piece,p_objetive):
        v_resultado=False

        if p_piece.islower() and p_objetive.isupper():
            v_resultado=True
        elif p_piece.isupper() and p_objetive.islower():
            v_resultado=True

        return v_resultado


    def movimientos_peon(self, tipo, p_fila, p_columna):
        v_respuesta=[]
        v_direccion=-1
        v_direFila=0
        v_direColumna=p_columna
        v_pieza=None

        if tipo.islower():
            v_direccion=1

        v_direFila=p_fila+v_direccion


        v_pieza=self.obtener_pieza_en(v_direFila, v_direColumna)


        #avance derecho
        if v_pieza is None:
                v_respuesta.append([v_direFila,v_direColumna])
                v_pieza = self.obtener_pieza_en(v_direFila + v_direccion, v_direColumna)

                if v_pieza is None:
                    if tipo.islower() and p_fila == 1:
                        v_respuesta.append([v_direFila + v_direccion, v_direColumna])
                    elif tipo.isupper() and p_fila == 6:
                        v_respuesta.append([v_direFila + v_direccion, v_direColumna])

        v_pieza=self.obtener_pieza_en(v_direFila, v_direColumna-1)
        #lateral izquierdo
        if v_pieza is not None:

            if self.m_isEnemy(tipo,v_pieza[0]):
                v_respuesta.append(v_pieza)

        v_pieza=self.obtener_pieza_en(v_direFila, v_direColumna+1)
        #lateral derecho
        if v_pieza is not None:

            if self.m_isEnemy(tipo,v_pieza[0]):
                v_respuesta.append(v_pieza)

        return v_respuesta


    def movimientos_alfil(self,p_tipo,p_fila,p_columna):
        v_respuesta=[]

        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[1,1])) #Derecha hacia arriba
        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[-1,1]))#izquierda hacia abajo
        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[1,-1]))#derecha hacia abajo
        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[-1,-1]))#izquierda hacia abajo

        return v_respuesta


    def movimientos_torre(self,p_tipo,p_fila,p_columna):
        v_respuesta=[]
        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[1,0]))#arriba
        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[-1,0]))#abajo
        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[0,1]))#derecha
        v_respuesta.extend(self.m_moviDireccionado(p_tipo,p_fila,p_columna,[0,-1]))#izquierda

        return v_respuesta


    def movimientos_reina(self,p_tipo,p_fila,p_columna):
        v_respuesta=[]
        v_respuesta.extend(self.movimientos_torre(p_tipo,p_fila,p_columna))
        v_respuesta.extend(self.movimientos_alfil(p_tipo,p_fila,p_columna))

        return v_respuesta

    def movimientos_rey(self,p_tipo,p_fila,p_columna):
        v_respuesta=[]
        v_movimientos=[[1,-1],[1,0],[1,1],
                      [0,-1],[0,1],
                      [-1,-1],[-1,0],[-1,1],
                      ]

        for v_movimiento in v_movimientos:
            v_respuesta.extend(self.m_moveUnaPosicion(p_tipo,p_fila,p_columna,v_movimiento))




        return v_respuesta



    def m_moveUnaPosicion(self,p_tipo,p_fila,p_columna,p_direccion):
        v_respuesta=[]

        p_columna+=p_direccion[0]
        p_fila+=p_direccion[1]

        if (p_fila>=0 and p_columna>=0) and (p_fila<8 and p_columna<8):

            v_pieza=self.obtener_pieza_en(p_fila,p_columna)

            if v_pieza is not None:

                if self.m_isEnemy(p_tipo,v_pieza[0]):
                    v_respuesta.append(v_pieza)


            else:
                v_respuesta.append([p_fila,p_columna])

        return v_respuesta



    def movimientos_caballo(self,p_tipo,p_fila,p_columna):
        v_respuesta=[]
        v_movimientos=[[1,-2],[2,-1],[1,2],[2,1],
                       [-1,-2],[-2,-1],[-1,2],[-2,1]]

        for v_movimiento in v_movimientos:
            v_respuesta.extend(self.m_moveUnaPosicion(p_tipo,p_fila,p_columna,v_movimiento))


        return v_respuesta



    def m_moviDireccionado(self,p_tipo,p_fila,p_columna,p_direccion):
        v_respuesta=[]
        p_fila+=p_direccion[0]
        p_columna+=p_direccion[1]
        v_pieza=None
        v_bandera=True
        while (p_fila>=0 and p_columna>=0) and (p_fila<8 and p_columna<8) and v_bandera:
            v_pieza=self.obtener_pieza_en(p_fila, p_columna)

            if v_pieza is not None:
                v_bandera=False

                if self.m_isEnemy(p_tipo,v_pieza[0]):
                    v_respuesta.append(v_pieza)

            else:
                v_respuesta.append([p_fila,p_columna])

            p_fila+=p_direccion[0]
            p_columna+=p_direccion[1]


        return v_respuesta







