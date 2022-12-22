# Reindj
Este proyecto tiene el objetivo de crear un Motor de Búsqueda con un Sistema de Recuperación de Información.  
Se deben crear 3 modelos de recuperación de información en función de 3 colecciones de documentos y establecer las métricas pertinentes para evaluar cada modelo.  
  
|        Modelos         | Finalizado | Colecciones | Finalizado |
|------------------------|------------|-------------|------------|
| Vectorial              | Listo      | Cranfield   | Listo      |
| Booleano               | Listo  | TREC-Covid  | Listo  |
| Indexación de Semántica Latente| Listo      | Vaswani     | Listo      |  
                                      

Para ejecutar el código debe tener instalado python, uvicorn, nltk y numpy
```
> uvicorn main:app --reload
```
Con respecto a los requerimientos se puede encontrar un ```requirements.txt``` dentro del directorio principal del proyecto. Cualquier editor de código o IDE ofrece las facilidades para satisfacer dichos requerimientos.
