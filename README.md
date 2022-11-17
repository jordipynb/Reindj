# Reindj
Este proyecto tiene el objetivo de crear un Motor de Búsqueda con un Sistema de Recuperación de Información.  
Se deben crear 3 modelos de recuperación de información en función de 3 colecciones de documentos y establecer las métricas pertinentes para evaluar cada modelo.  
  
| Modelos | Colecciones | Finalizado |
|---------|-------------|------------|
| Vectorial | Cranfield |  Listo     |
| Booleano | TREC-Covid | Pendiente  |
| Vectorial Generalizado | Vaswani | Pendiente|  

Para ejecutar el código debe tener instalado python, uvicorn, nltk y numpy
```
> uvicorn main:app --reload
```
