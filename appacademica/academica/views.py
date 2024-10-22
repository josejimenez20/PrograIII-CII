from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import alumno, docente, materia
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def hola_mundo(request):
    return HttpResponse("Hola Mundo")

def saludo(request, nombre):
    return HttpResponse(f"Hola {nombre}, bienvenido a Programacion Computacional III")

def edad(request, edad):
    return HttpResponse("Tu edad es %s años" %edad)

def index(request):
    return render(request, 'index.html')

def vista(request, form):
    return render(request, f"{form}.html")

def consultar_alumnos(request):
    datos = alumno.objects.values('id', 'codigo', 'nombre', 'direccion', 'telefono')
    return JsonResponse(list(datos), safe=False)

def consultar_docentes(request):
    datos = docente.objects.values('id', 'codigo', 'nombre', 'direccion', 'telefono', 'email')
    return JsonResponse(list(datos), safe=False)

def consultar_materias(request):
    datos = materia.objects.values('id', 'codigo', 'nombre', 'uv')
    return JsonResponse(list(datos), safe=False)

@csrf_exempt
def guardar_alumno(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if( data.get("accion")=="nuevo" ):
            editAlumno = alumno.objects.create(
                codigo = data.get("codigo"),
                nombre = data.get("nombre"),
                direccion = data.get("direccion"),
                telefono = data.get("telefono"),
            )
        elif( data.get("accion")=="modificar" ):
            editAlumno = alumno.objects.get(id=data.get("idAlumno"))
            editAlumno.codigo = data.get("codigo")
            editAlumno.nombre = data.get("nombre")
            editAlumno.direccion = data.get("direccion")
            editAlumno.telefono = data.get("telefono")
            editAlumno.save()
        elif( data.get("accion")=="eliminar" ):
            editAlumno = alumno.objects.get(id=data.get("idAlumno"))
            editAlumno.delete()
        return JsonResponse({'msg':'ok', 'idAlumno': editAlumno.id})
    
@csrf_exempt
def guardar_docente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if( data.get("accion")=="nuevo" ):
            editDocente = docente.objects.create(
                codigo = data.get("codigo"),
                nombre = data.get("nombre"),
                direccion = data.get("direccion"),
                telefono = data.get("telefono"),
                email = data.get("email"),
            )
        elif( data.get("accion")=="modificar" ):
            editDocente = docente.objects.get(id=data.get("idDocente"))
            editDocente.codigo = data.get("codigo")
            editDocente.nombre = data.get("nombre")
            editDocente.direccion = data.get("direccion")
            editDocente.telefono = data.get("telefono")
            editDocente.email = data.get("email")
            editDocente.save()

        elif( data.get("accion")=="eliminar" ):
            editDocente = docente.objects.get(id=data.get("idDocente"))
            editDocente.delete()
        return JsonResponse({'msg':'ok', 'idDocente': editDocente.id})

@csrf_exempt
def guardar_materia(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if( data.get("accion")=="nuevo" ):
            editMateria = materia.objects.create(
                codigo = data.get("codigo"),
                nombre = data.get("nombre"),
                uv = data.get("uv"),
            )
        elif( data.get("accion")=="modificar" ):
            editMateria = materia.objects.get(id=data.get("idMateria"))
            editMateria.codigo = data.get("codigo")
            editMateria.nombre = data.get("nombre")
            editMateria.uv = data.get("uv")
            editMateria.save()

        elif( data.get("accion")=="eliminar" ):
            editMateria = materia.objects.get(id=data.get("idMateria"))
            editMateria.delete()
        return JsonResponse({'msg':'ok', 'idMateria': editMateria.id})
