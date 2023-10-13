import threading
import time
import queue

def barbero(barbero_disponible, cola_clientes):
    while True:
        if not cola_clientes.empty():
            cliente = cola_clientes.get()
            print(f'El barbero está atendiendo al cliente {cliente}')
            time.sleep(2)  # El barbero atiende al cliente durante 2 segundos
            print(f'El cliente {cliente} ha sido atendido')
            cola_clientes.task_done()
        else:
            print('El barbero está durmiendo...')
            barbero_disponible.set()
            barbero_disponible.wait()

def cliente(cliente_id, cola_clientes, barbero_disponible):
    print(f'Cliente {cliente_id} llega a la barbería')
    if cola_clientes.qsize() < 3:
        cola_clientes.put(cliente_id)
        if barbero_disponible.is_set():
            print(f'El barbero está despierto. Cliente {cliente_id} despierta al barbero')
            barbero_disponible.clear()
    else:
        print(f'La barbería está llena. Cliente {cliente_id} se va.')

if __name__ == '__main__':
    cola_clientes = queue.Queue()
    barbero_disponible = threading.Event()

    barbero_thread = threading.Thread(target=barbero, args=(barbero_disponible, cola_clientes))
    barbero_thread.start()

    clientes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Número de clientes que llegan
    for cliente_id in clientes:
        time.sleep(1)  # Intervalo de llegada de clientes
        cliente_thread = threading.Thread(target=cliente, args=(cliente_id, cola_clientes, barbero_disponible))
        cliente_thread.start()
