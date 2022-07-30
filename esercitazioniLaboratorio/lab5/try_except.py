while True:
    try:
        n = input("Inserisci un numero intero: ")
        n = int(n)
        break
    except Exception as e:
        print("L'errore commesso e': ",e)
print("Grande, il numero che hai inserito è un intero!")
