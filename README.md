
# Restaurante App 🍴

Este proyecto es una aplicación web para gestionar reservas, usuarios, compras y pedidos en un restaurante. Facilita el manejo de clientes, camareros, chefs y administradores mediante un sistema de roles bien definido.

## Funcionalidades

### Registro e inicio de sesión de usuarios:
- **Asignación automática de roles:** 
  - Los usuarios nuevos son asignados automáticamente como "Cliente".
- **Gestión de roles específicos:** 
  - Roles soportados: **Administrador**, **Camarero**, **Chef** y **Cliente**.
- **Autenticación segura:** 
  - Los usuarios solo pueden acceder a funcionalidades de acuerdo a su rol asignado.

---

### Gestión de reservas:
- **Clientes:**
  - Crear y visualizar sus propias reservas.
- **Camareros:**
  - Ver y gestionar todas las reservas, incluyendo el cliente asociado.
  - Editar y eliminar reservas disponibles.
- **Restricciones:**
  - No se permiten reservas en fechas pasadas.

---

### Gestión de menús y pedidos:
- **Administrador:**
  - Añadir, editar y eliminar platillos del menú.
  - Marcar platillos como "disponibles" o "no disponibles".
- **Clientes:**
  - Visualizar el menú actualizado.
  - Realizar compras seleccionando uno o varios platillos.
  - Visualizar un desglose detallado de cada compra, incluyendo:
    - **Platillos seleccionados.**
    - **Cantidad.**
    - **Precio por platillo.**
    - **Precio total.**
- **Chef:**
  - Acceso a todas las compras realizadas por los clientes.
  - Actualizar el estado de una compra a:
    - **En preparación.**
    - **Terminado.**
    - **Compra cancelada.**
  - Visualización detallada de cada compra, incluyendo platillos, cantidades y precios.
- **Camareros:**
  - Gestionar pedidos asignados y dar seguimiento a las compras.

---

### Gestión de compras:
- **Estados de compra:**
  - Cada compra tiene un estado que puede ser modificado por el Chef:
    - **En preparación.**
    - **Terminado.**
    - **Compra cancelada.**
- **Desglose detallado:**
  - Clientes y chefs pueden ver los platillos y cantidades asociadas a cada compra.

---

### Diseño e interfaz:
- **Bootstrap 5 integrado:**
  - Interfaz responsiva y amigable para facilitar la navegación en distintos dispositivos.
- **Estilos personalizados:**
  - Colores específicos para cada estado de compra:
    - **En preparación:** Amarillo.
    - **Terminado:** Verde.
    - **Compra cancelada:** Rojo.

---

## Tecnologías utilizadas:
- **Backend:**
  - Django 5.1.3
- **Frontend:**
  - Bootstrap 5
- **Base de datos:**
  - MySQL
- **Control de versiones:**
  - Git y GitHub

---

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/vnoram/restaurante.git
   cd restaurante