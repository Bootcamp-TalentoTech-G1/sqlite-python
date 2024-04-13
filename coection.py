import sqlite3

# Ruta al archivo de la base de datos SQLite existente
database_path = 'D:/db/datos2.db'

# Conectarse a la base de datos
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Crear una tabla
conn.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY, nombre TEXT, edad INTEGER)''')

# Insertar datos en la tabla
conn.execute("INSERT INTO usuarios (nombre, edad) VALUES ('Juan', 30)")
conn.execute("INSERT INTO usuarios (nombre, edad) VALUES ('María', 25)")

# Crear tabla mensajes
cursor.execute('''CREATE TABLE IF NOT EXISTS mensajes
             (id INTEGER PRIMARY KEY, contenido TEXT, id_usuario INTEGER,
              FOREIGN KEY(id_usuario) REFERENCES usuarios(id))''')

# Insertar datos en la tabla usuarios
cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES ('Juan', 30)")
cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES ('María', 25)")

# Insertar datos en la tabla mensajes
cursor.execute("INSERT INTO mensajes (contenido, id_usuario) VALUES ('Hola Mundo', 1)")
cursor.execute("INSERT INTO mensajes (contenido, id_usuario) VALUES ('Saludos', 2)")

# Consulta SELECT para obtener todos los usuarios
cursor.execute("SELECT usuarios.nombre,usuarios.edad FROM usuarios")
print("Usuarios:")
for row in cursor.fetchall():
    print(row)

# Consulta SELECT para obtener todos los mensajes con los nombres de los usuarios
cursor.execute("SELECT mensajes.id, mensajes.contenido, usuarios.nombre FROM mensajes JOIN usuarios ON mensajes.id_usuario = usuarios.id")
print("\nMensajes:")
for row in cursor.fetchall():
    print(row)

# Crear un trigger para eliminar mensajes de un usuario cuando se elimina ese usuario
cursor.execute('''CREATE TRIGGER IF NOT EXISTS eliminar_mensajes_usuario
                AFTER DELETE ON usuarios
                FOR EACH ROW
                BEGIN
                    DELETE FROM mensajes WHERE id_usuario = OLD.id;
                END''')
id=2

# Eliminar un usuario y ver cómo se eliminan automáticamente sus mensajes
cursor.execute("DELETE FROM usuarios WHERE id ="+id)

# Consultar nuevamente los mensajes para verificar que los mensajes del usuario eliminado ya no existen
cursor.execute("SELECT * FROM mensajes")
print("\nMensajes después de eliminar usuario 1:")
for row in cursor.fetchall():
    print(row)
    
# Consulta SELECT para obtener los mensajes de un usuario específico (por ejemplo, usuario con id = 2)
cursor.execute("SELECT * FROM mensajes WHERE id_usuario = 2")
print("\nMensajes del usuario con id = 2:")
for row in cursor.fetchall():
    print(row)
    
# Actualizar el nombre del usuario con id = 2
cursor.execute("UPDATE usuarios SET nombre = 'Pedro' WHERE id = 2")

# Guardar los cambios
conn.commit()

# Cerrar la conexión cuando hayas terminado
conn.close()