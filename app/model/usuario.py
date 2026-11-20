class Usuario:

    def __init__(self, id, nombre, apellidos, dni, telefono,
                 correo, contrasena_hash, estado, rol):

        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.telefono = telefono
        self.correo = correo
        self.contrasena_hash = contrasena_hash
        self.estado = estado
        self.rol = rol