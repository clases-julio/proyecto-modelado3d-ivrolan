import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto].select = True # ...excepto el buscado

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.scene.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

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
    
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    
    
    borrarObjetos()
    
    # creacin escenario para hacer luego el render
    Objeto.crearCamara('Cam')
    Especifico.posicionar('Cam', (5, -4,2))
    
    Objeto.crearPuntoLuz('Punto')
    Especifico.posicionar('Punto', (2,-3,1))
    bpy.context.object.data.energy = 140

    ## Creacion del objeto Rueda
    crearRueda("1")
    
    Especifico.posicionar('Rueda1', (0, -1.5, 0))
    
    crearRueda("2")
    
    Especifico.rotar('Rueda2', (-1.57,0,0))
    Especifico.posicionar('Rueda2', (0, 1.5, 0))
    
    
    
    
    
    
