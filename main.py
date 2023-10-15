import threading
import time
import queue
import os

# Codigo correcto

def barbero(barbero_disponible, cola_clientes):
    while True:
        if not cola_clientes.empty(): #si la cola_clientes no esta vacia: 
            cliente = cola_clientes.get()
            print(f'El barbero está atendiendo al cliente {cliente}')
            time.sleep(5)  # El barbero atiende al cliente durante 2 segundos
            print(f'El cliente {cliente} ha sido atendido')
            cola_clientes.task_done()
        else: # Si esta vacia (pasa esto primero)
            print('El barbero está durmiendo...')
            time.sleep(3)
            barbero_disponible.set()
            barbero_disponible.wait()

def cliente(cliente_id, cola_clientes, barbero_disponible):
    print(f'Cliente {cliente_id} llega a la barbería')
    if cola_clientes.qsize() < 3:
        cola_clientes.put(cliente_id)
        if barbero_disponible.is_set():
            print(f'El barbero está despierto.')
            barbero_disponible.clear()
    else:
        print(f'La barbería está llena. Cliente {cliente_id} se va.')

if __name__ == '__main__':
    cola_clientes = queue.Queue() # Cola (FIFO)
    barbero_disponible = threading.Event() #Creamos un semaforo(False), Set = True, Clear = False, wait = empezera a ser true o false

    clientes = []  # Número de clientes que llegan
    total_c = input("Cuantos clientes deseas agregar? \n")
    for i in range(int(total_c)):
        clientes.append(i + 1)
    os.system("cls")

    barbero_thread = threading.Thread(target=barbero,daemon=True, args=(barbero_disponible, cola_clientes)) #empieza la funcion como un hilo
    # Empeazamos un sub-proceso (hilo)
    barbero_thread.start()

    for cliente_id in clientes:
        time.sleep(2)  # Intervalo de llegada de clientes
        cliente_thread = threading.Thread(target=cliente,daemon=True, args=(cliente_id, cola_clientes, barbero_disponible))
        #empezamos un sub-proceso
        cliente_thread.start()
    
    input("")
