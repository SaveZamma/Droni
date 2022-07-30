import sys
import importlib.util
import subprocess
import os

reqModules = ['socket', 'threading', 'curses', 'npyscreen', 'time', 'datetime', 'pyperclip'] # Array con i moduli richiesti
missingModules = [] # Array da riempire con i moduli mancanti

if sys.version_info < (3, 3): # Verifica la versione di Python
    print("E' richiesta la versione Python 3.3 per poter eseguire la chat-p2p. La tua versione {0}.".format(sys.version))
    exit(1)
else:
    for module in reqModules: # Verifica che ciascun modulo sia installato
        if not module in sys.modules and importlib.util.find_spec(module) == None:
            missingModules.append(module)
            print("Il modulo richiesto non è presente: {0}".format(module))
        else:
            print("{0} è installato".format(module))

    if missingModules: # Se c'è un modulo mancante, installalo | L'installazione richiede pip
        print("Almeno uno dei moduli necesari manca. Exiting...")
        if "pip3" in sys.modules or importlib.util.find_spec("pip3") is not None:
            answ = input("Proviamo ad installare i moduli mancanti with pip3? [y/n] >> ")
            if answ == "y" or answ == "Y":
                for module in missingModules:
                    if module == "curses" and os.name == "nt":
                        print("Curses richiede di essere installato manualmente.")
                        continue
                    try:
                        pip = subprocess.Popen([sys.executable, "-m", "pip3", "install", module])
                        pip.wait()
                    except Exception:
                        pass
                    if not module in sys.modules and importlib.util.find_spec(module) == None:
                        print("Impossibile installare {0}.".format(module))
                    else:
                        print("Installato {0}.".format(module))
                        missingModules.remove(module)
    
if missingModules:
    print("Provate ad installare questi moduli manualmente:")
    for module in missingModules:
        print("-",module)
        i = input("Premere Enter per Uscire >>")
        exit(1)
else:
    import chat # Importa la Chat da chat.py
    chatApp = chat.ChatApp().run() # esegue la Chat



