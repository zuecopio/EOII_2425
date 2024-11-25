# EOII_2425_P8
*Práctica 8 - OPC-UA: Aplicaciones cliente/servidor*

## Cuestiones ejercicio 1

### Print 1

#### ```print("los hijos a parir de la raiz son: ", espacio_obj)```

**Resultado:**
```console
The children from the root are:  [SyncNode(NodeId(Identifier=85, NamespaceIndex=0, NodeIdType=<NodeIdType.Numeric: 2>)), SyncNode(NodeId(Identifier=86, NamespaceIndex=0, NodeIdType=<NodeIdType.Numeric: 2>)), SyncNode(NodeId(Identifier=87, NamespaceIndex=0, NodeIdType=<NodeIdType.Numeric: 2>))]
```
**Significado:** <br>
Se muestran todos los nodos hijos que se encuentran directamente bajo la raíz.  Cada ```SyncNode``` representa un nodo con un identificador único.

---

### Print 2

#### ```print("el valor del dato es: ", result1)```

**Resultado:**
```console
The value of the data is:  DataValue(Value=Variant(Value=295.9999999999988, VariantType=<VariantType.Double: 11>, Dimensions=None, is_array=False), StatusCode_=StatusCode(value=0), SourceTimestamp=datetime.datetime(2024, 11, 24, 23, 34, 19, 373458, tzinfo=datetime.timezone.utc), ServerTimestamp=datetime.datetime(2024, 11, 24, 23, 34, 19, 373512, tzinfo=datetime.timezone.utc), SourcePicoseconds=None, ServerPicoseconds=None)
```
**Significado:** <br>
Con este print se muestra el valor de la variable ```MyVariable``` que se encuentra en el servidor OPC-UA. Incluye su valor (295.99), el tipo de dato (doble), el estado del código (que indica si el dato es válido) y las marcas de tiempo que indican cuándo se obtuvo el dato, tanto del origen como del servidor.

---

### Print 3

#### ```print("el valor antes de escribir es: ", result2)```

**Resultado:**
```console
 The value before writing is:  295.9999999999988
```
**Significado:** <br>
Muestra el valor de ```MyVariable``` antes de ser modificada por el cliente.

---

### Print 4

#### ```print("el valor después de escribir: ", result3)```

**Resultado:**
```console
The value after writing is:  1000.9
```
**Significado:** <br>
Muestra el valor de ```MyVariable``` después de haber sido modificada por el cliente.

---

### Print 5

#### ```print("myobj is: ", obj)```

**Resultado:**
```console
myobj is:  ns=2;i=1
```

**Significado:** <br>
Indica la representación del objeto ```myobj``` con la que se puede identificar el nodo de forma única. Esta incluye su espacio de nombres (ns=2) y su identificador (i=1).