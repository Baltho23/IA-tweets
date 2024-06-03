import pandas as pd

def remove_urls(text):
    # Dividir el texto por espacios en blanco
    words = text.split()
    # Filtrar las palabras que no son enlaces URL
    words = [word for word in words if not ('http://' in word or 'https://' in word)]
    # Unir las palabras de nuevo en una cadena de texto
    return ' '.join(words)

def remove_accents(text):
    # Lista de caracteres acentuados
    accented_chars = 'áéíóúüÁÉÍÓÚÜ'
    # Lista de caracteres sin acento correspondientes
    unaccented_chars = 'aeiouuAEIOUU'
    # Reemplazar caracteres acentuados por sus equivalentes sin acento
    text = ''.join(unaccented_chars[accented_chars.index(char)] if char in accented_chars else char for char in text)
    return text

def clean_text(text):
    # Eliminar enlaces URL
    text = remove_urls(text)
    # Eliminar caracteres especiales y tildes
    cleaned_text = ''.join(char for char in remove_accents(text) if char.isalnum() or char.isspace())
    # Divide el texto por los espacios en blanco
    words = cleaned_text.split()
    # Filtra las palabras que no tienen longitud mayor a 2 y contienen caracteres alfabéticos
    filtered_words = [word for word in words if len(word) > 2 and any(c.isalpha() for c in word)]
    # Une las palabras filtradas de nuevo en una cadena de texto
    return ' '.join(filtered_words)

# Ruta al archivo de texto
file_tuistBases = 'tuitsBases.txt'

# Cargar el archivo en un DataFrame
df = pd.read_csv(file_tuistBases, delimiter=',', header=None)

# Eliminar la primera columna (índice)
df = df.drop(columns=[0])

# Calcular cuántas veces aparece cada nombre de usuario en la columna 3
name_counts = df[2].value_counts()

# Filtrar el DataFrame original para mantener solo las filas donde el nombre de usuario aparezca al menos 6 veces
df_filtered = df[df[2].isin(name_counts.index[name_counts >= 6])]

# Aplicar primero la función remove_urls y luego clean_text a todas las columnas de texto en el DataFrame a partir de la tercera columna
df_filtered.iloc[:, 2:] = df_filtered.iloc[:, 2:].map(lambda x: clean_text(x) if isinstance(x, str) else x)

# Mostrar las primeras filas del DataFrame filtrado
print(df_filtered.head())

# Ruta para el nuevo archivo
file_tuitsLimpios = 'tuitsLimpios.txt'

# Guardar el DataFrame filtrado en un nuevo archivo de texto
df_filtered.to_csv(file_tuitsLimpios, index=False, header=False, sep=',')

# Cargar el archivo en un DataFrame
df = pd.read_csv(file_tuitsLimpios, delimiter=',', header=None)

# Crear una lista para almacenar las filas tokenizadas
tokenized_rows = []

for index, row in df.iterrows():
    # Obtener el id del tweet y el nombre de usuario de la fila
    tweet_id, username = row[0], row[1]
    # Obtener el contenido del tweet y tokenizarlo
    tweet_content = row[2].split()
    # Iterar sobre cada palabra del contenido del tweet y agregarla como una nueva fila
    for word in tweet_content:
        tokenized_rows.append([tweet_id, username, word])

# Crear un nuevo DataFrame con las filas tokenizadas
df_tokenized = pd.DataFrame(tokenized_rows, columns=['Tweet ID', 'Username', 'Word'])

# Ruta para el nuevo archivo
file_tuistTokenizados = 'tuitsTokenizados.txt'

# Guardar el DataFrame tokenizado en un nuevo archivo de texto
df_tokenized.to_csv(file_tuistTokenizados, index=False, header=False, sep=',')

print(f"Archivo guardado en: {file_tuistTokenizados}")

print(f"Archivo guardado en: {file_tuitsLimpios}")