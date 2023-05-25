import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')

BUFFER_SIZE = 10
buffer = []
condition = threading.Condition()


def consumer(cond):
    """wait for the condition and use the resource"""
    logging.debug('Iniciando hilo consumidor')
    with cond:
        while len(buffer) == 0:
            logging.debug('El buffer está vacío, esperando recursos...')
            cond.wait()
        resource = buffer.pop(0)
        logging.debug('Consumiendo recurso: %s', resource)
        cond.notifyAll()


def producer(cond):
    """set up the resource to be used by the consumer"""
    logging.debug('Iniciando el hilo productor')
    with cond:
        while len(buffer) == BUFFER_SIZE:
            logging.debug('El buffer está lleno, esperando consumo...')
            cond.wait()
        resource = time.time()  # Ejemplo: generar recurso de tiempo actual
        buffer.append(resource)
        logging.debug('Producido recurso: %s', resource)
        cond.notifyAll()


c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
p = threading.Thread(name='p', target=producer, args=(condition,))

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()
