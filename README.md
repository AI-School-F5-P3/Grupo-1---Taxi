# Proyecto Python: Taxi

 ## Planteamiento
 El objetivo de este proyecto es desarrollar un prototipo de taxímetro digital en Python que
 pueda ser implementado en la red de taxis para modernizar el sistema actual de facturación
 y calcular las tarifas en función de si el taxi está en movimiento o no.
 
 ## Requisitos
1. Inicio del programa:
    * Elprograma debe iniciar con un mensaje de bienvenida y una explicación de
    su funcionamiento.
    * Debequedar a la espera de instrucciones para comenzar la carrera.
    
2. Inicio de carrera:
    * Al iniciar la carrera, el taxi siempre comenzará parado.
    * Debecalcular la tarifa en función del estado del taxi:
        * 2céntimos por segundo mientras el taxi esté parado.
        * 5céntimos por segundo mientras el taxi esté en movimiento.

3. Cambio de estado:
    * Elprograma debe permitir indicar cuando el taxi arranca y se pone en
    movimiento.
    * También debe permitir indicar cuando el taxi se detiene, sin acabar la carrera.

4. Fin de carrera:
    * Al finalizar la carrera, debe calcular y mostrar el precio total en euros.
    * Elprograma debe quedar a la espera de iniciar una nueva carrera sin
    necesidad de reiniciarlo.

##  Niveles de Entrega
 1. Nivel Esencial:
    * Programa CLI con las funcionalidades básicas.
    * Manejo de estado de taxi (parado/en movimiento).
    * Cálculo y visualización del total de la carrera.

 2. Nivel Medio:
    * Sistema de logs para trazabilidad.
    * Tests unitarios.
    * Registro histórico de carreras en texto plano.
    * Configuración dinámica de precios.

 3. Nivel Avanzado:
    * Enfoque orientado a objetos (OOP).
    * Seguridad mediante contraseñas.
    * Frontend o interfaz amigable.

 4. Nivel Experto:
    * Basededatos para registros de carreras.
    * Dockerización de la aplicación.
    * Despliegue web accesible.

## Tecnologías a Utilizar
    ● GityGitHub para control de versiones y repositorio.
    ● Python para el desarrollo del programa.
    ● Trello/Jira para la gestión del proyecto.

##  Implementación del Nivel Esencial
 Vamos a comenzar con la implementación del nivel esencial del proyecto. Aquí está el plan
 paso a paso para lograrlo.

 ## Plan de Implementación
 1. Estructura del Programa:
    * Crear un programa CLI que interactúe con el usuario a través de la terminal.
    * Utilizar input para recibir comandos del usuario y controlar el estado del
 taxi.

 2. Cálculo de Tarifas:
    * Implementar un temporizador que calcule el tiempo que el taxi pasa en cada
    estado.
    * Calcular el costo acumulado en función del tiempo y el estado del taxi.

 3. Gestión de Estados:
    * Crear funciones para manejar el cambio de estado (parado/en movimiento)
    del taxi.
    * Asegurarse de que el estado y el tiempo transcurrido se actualicen
    correctamente.

 4. Finalización de la Carrera:
    * Calcular el costo total y mostrarlo al usuario.
    * Preparar el programa para una nueva carrera sin necesidad de reiniciarlo.
