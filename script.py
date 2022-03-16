import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto].select_set(True)# ...excepto el buscado

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.view_layer.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False, confirm=False)


def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

def seleccionarVariosObjetos(nombresObj):
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    for obj in nombresObj:
        bpy.data.objects[obj].select_set(True)

def unirObjetos(listObj, nombreUnion):
    seleccionarVariosObjetos(listObj)
    bpy.ops.object.join()
    #print("funcionooo")
    Activo.renombrar(nombreUnion)
    #print("fin unirObjetos")
'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')

'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto
    def diferencia(nombreObjeto, nombreResta, borrarObjetoResta):
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[nombreResta]
        #bpy.context.object.modifiers["Boolean"].use_hole_tolerant = True
        bpy.ops.object.modifier_apply(modifier="Boolean")
        
        if borrarObjetoResta:
            borrarObjeto(nombreResta)


'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
        
    def crearCilindro(objName):
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        Activo.renombrar(objName)
        
    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearPuntoLuz(objName):
        bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        Activo.renombrar(objName)
        
    def crearCamara(objName):
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(1.29722, 0.0141782, 1.14368), scale=(1, 1, 1))
        Activo.renombrar(objName)

def crearRueda(id):
    Objeto.crearCilindro('Cilindro' + id)
    Especifico.rotar('Cilindro'  + id, (1.57, 0, 0))
    Especifico.escalar('Cilindro' + id, (0.75, 0.75, 0.2))
    Especifico.posicionar('Cilindro' + id, (0, -0.5, 0))
    
    Objeto.crearCilindro('Cilindro2' + id)
    Especifico.rotar('Cilindro2' + id, (1.57, 0, 0))
    Especifico.escalar('Cilindro2' + id, (0.25, 0.25, 0.4))
    Especifico.posicionar('Cilindro2' + id, (0, 0, 0))
    
    #seleccionarVariosObjetos(['Cilindro', 'Cilindro2'])
    unirObjetos(['Cilindro' + id, 'Cilindro2' + id], 'Rueda' + id)

def crearLink(id):
    Objeto.crearCubo('Link'+id)
    Especifico.escalar('Link'+id, (1.3, 1, 4))
    
    Objeto.crearCubo("RestaSuperior")
    Especifico.escalar("RestaSuperior", (1.4, 0.6, 1.8))
    Especifico.posicionar("RestaSuperior", (0,0, 0.8))
    
    activarObjeto('Link'+id)
    Activo.diferencia('Link'+id, "RestaSuperior", True)
    
    Objeto.crearCubo("RestaInferior")
    Especifico.escalar("RestaInferior", (1.4, 2, 1.2))
    #Especifico.posicionar("RestaSuperior", (0,0, 0.8))
    Objeto.crearCilindro("CilindroResta")
    Especifico.escalar("CilindroResta", (0.3, 0.3, 0.6))
    Especifico.rotar("CilindroResta", (1.57, 0,0))
    Especifico.posicionar("CilindroResta", (0,0,0.24))
    
    activarObjeto("RestaInferior")
    Activo.diferencia("RestaInferior", "CilindroResta", True)
    
    Especifico.posicionar("RestaInferior", (0, 0, -0.9))
    
    activarObjeto('Link'+id)
    Activo.diferencia('Link'+id, "RestaInferior", True)
    
    Objeto.crearCubo("RestaLateral")
    Especifico.escalar("RestaLateral", (1.4, 0.6, 1.5))
    Especifico.posicionar("RestaLateral", (0, -0.27, -0.6))
    
    activarObjeto('Link'+id)
    Activo.diferencia('Link'+id, "RestaLateral", False)
    
    Especifico.posicionar("RestaLateral", (0, 0.27, -0.6))
    
    activarObjeto('Link'+id)
    Activo.diferencia('Link'+id, "RestaLateral", True)

def crearCabeza(id):
    
    Objeto.crearCubo("HeadCube"+id)
    
    width_head = 6.5
    
    Especifico.escalar("HeadCube"+id, (4,width_head, 3))
    
    Objeto.crearCilindro("HeadCylinder"+id)
    Especifico.escalar("HeadCylinder"+id, (0.75, 0.75, width_head/4))
    Especifico.rotar("HeadCylinder"+id, (1.57, 0, 0)) 
    Especifico.posicionar("HeadCylinder"+id, (0.9, 0, 0))
    
    unirObjetos(["HeadCube"+id,"HeadCylinder"+id ], "Head"+id)
    
    Objeto.crearCubo("HeadCubeSuma"+id)
    Especifico.escalar("HeadCubeSuma"+id, (5, 1.1, 1))
    
    Especifico.posicionar("HeadCubeSuma"+id, (0.5, -1, 0.1))
    
    Objeto.crearCubo("HeadCubeSuma2"+id)
    Especifico.escalar("HeadCubeSuma2"+id, (5, 1.1, 1))
    
    Especifico.posicionar("HeadCubeSuma2"+id, (0.5, 1, 0.1))
    
    
    
    seleccionarObjeto("Head"+id)
    activarObjeto("Head"+id)
    unirObjetos([ "HeadCubeSuma"+id,"HeadCubeSuma2"+id , "Head"+id], "Head"+id)
    #Especifico.posicionar("HeadCubeResta"+id, (-0.4, 1, -0.7))
    
    #activarObjeto("Head"+id)
    #Activo.diferencia("Head"+id, "HeadCubeResta"+id, True)
    
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    
    
    borrarObjetos()
    
    # creacin escenario para hacer luego el render
    Objeto.crearCamara('Cam')
    Especifico.posicionar('Cam', (9.5, -5,3.5))
    
    Objeto.crearPuntoLuz('Punto')
    Especifico.posicionar('Punto', (2,-3,1))
    bpy.context.object.data.energy = 140

    ## Creacion del objeto Rueda
    crearRueda("1")
    
    Especifico.posicionar('Rueda1', (0, -1.5, 0))
    
    ## Creamos otra y la desplazamos y giramos
    crearRueda("2")
    
    Especifico.rotar('Rueda2', (-1.57,0,0))
    Especifico.posicionar('Rueda2', (0, 1.5, 0))
    
    crearLink("11") # bottom left (11)link
    
    Especifico.rotar('Link11', (0,-1.57/2,0))
    Especifico.posicionar('Link11', (-0.5, -1,0.5))
    
    
    crearLink("12") # bottom left (11)link
    
    Especifico.rotar('Link12', (0,-1.57/2,0))
    Especifico.posicionar('Link12', (-0.5, 1,0.5))
    
    crearLink("21")
    Especifico.rotar('Link21', (0,1.57/2,0))
    Especifico.posicionar('Link21', (-0.5, -1,1.5))
    
    crearLink("22")
    Especifico.rotar('Link22', (0,1.57/2,0))
    Especifico.posicionar('Link22', (-0.5, 1,1.5))
    
    crearCabeza("1")
    
    Especifico.posicionar("Head1", (0.6,0,2.5))
    
    
