import socket
import sys
import os 

sys.path.append(os.path.abspath('./log'))
from logger_config import setup_logger
logger = setup_logger("calc_logger")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

calc_port_str = os.environ.get('CALC_PORT')

if calc_port_str is None:
  logger.error("ERROR Aucun port spécifié : spécifiez un port (nombre entier de 1 à 65535).")
  sys.exit(1)

try:
    calc_port = int(calc_port_str)
    if (calc_port < 0 or calc_port> 65535):
      logger.error("ERROR Le port spécifié n'est pas un port possible (de 1 à 65535).")
      sys.exit(1)
    elif (calc_port >= 0 and calc_port<= 1024):
      logger.error("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
      sys.exit(1)
    else:
      logger.info("calc_serv available at localhost:%s",calc_port)
      s.bind(('localhost',calc_port))
except ValueError:
    logger.error("ERROR Argument non valide: spécifiez un port (nombre entier de 1 à 65535).")
    sys.exit(1)

s.listen(1)
conn, addr = s.accept()

while True:

  try:
    # On lit les 4 premiers octets qui arrivent du client
    # Car dans le client, on a fixé la taille du header à 4 octets
    isEnded = 0
    isAddition = 0
    isMultiply = 0
    isSubstract = 0
    isDivide = 0
    isModulo = 0
    isPower = 0
    # Une liste qui va contenir les données reçues
    chunks = []
    numbers = []
    result = 0
    while isEnded == 0 :
      header = conn.recv(4)
      if not header:
        break

      # On lit la valeur
      msg_len = int.from_bytes(header[0:4], byteorder='big')

      print(f"Lecture des {msg_len} prochains octets")

      bytes_received = 0
      numbersAdded = 0
      
      while bytes_received < msg_len:
          # Si on reçoit + que la taille annoncée, on lit 1024 par 1024 octets
          chunk = conn.recv(min(msg_len - bytes_received,
                                  1024))
          if not chunk:
            raise RuntimeError('Invalid chunk received bro')

          try:
            if chunk.decode('utf-8') == "hehe":
              isEnded = 1
            elif chunk.decode('utf-8') == "+":
              isAddition = 1
            elif chunk.decode('utf-8') == "-":
              isSubstract = 1
            elif chunk.decode('utf-8') == "*":
              isMultiply = 1
            elif chunk.decode('utf-8') == "/":
              isDivide = 1
            elif chunk.decode('utf-8') == "%":
              isModulo = 1
            else :
              # on ajoute le morceau de 1024 ou moins à notre liste
              numbers.append(chunk)
          except:
            # on ajoute le morceau de 1024 ou moins à notre liste
            numbers.append(chunk)
          
          # on ajoute la quantité d'octets reçus au compteur
          bytes_received += len(chunk)

    if isAddition == 1 :
      result =  int.from_bytes(numbers[0], byteorder='big') + int.from_bytes(numbers[1], byteorder='big')
    elif isSubstract == 1 :
      result = int.from_bytes(numbers[0], byteorder='big') - int.from_bytes(numbers[1], byteorder='big')
    elif isMultiply == 1 :
      result = int.from_bytes(numbers[0], byteorder='big') * int.from_bytes(numbers[1], byteorder='big')
    elif isDivide == 1 :
      result = int.from_bytes(numbers[0], byteorder='big') // int.from_bytes(numbers[1], byteorder='big')
    elif isModulo == 1 :
      result = int.from_bytes(numbers[0], byteorder='big') % int.from_bytes(numbers[1], byteorder='big')
    elif isPower == 1 :
      result = int.from_bytes(numbers[0], byteorder='big') ** int.from_bytes(numbers[1], byteorder='big')

    try:
      print(f" le résultat est {result}")
      conn.send(result.to_bytes(8, byteorder='big'))
    except Exception as e:
      print(f" error sending {e}")
    
    conn.close()
    s.close()
    sys.exit(0)
  except socket.error:
    print("Error Occured.")
    break


