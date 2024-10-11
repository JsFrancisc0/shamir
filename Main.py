import random


# generar el polinomio aleatorio
def generar_polinomio_modular(secreto, n, prime_mod):
    coeficientes = [secreto] + [random.randint(1, prime_mod - 1) for _ in range(n - 1)]
    return coeficientes


# funcion para evaluar el polinomio en un punto dado
def evaluar_polinomio(coeficientes, x, prime_mod):
    resultado = 0
    for i, coef in enumerate(coeficientes):
        resultado = (resultado + coef * (x ** i)) % prime_mod
    return resultado


# dividir el secreto en partes
def dividir_secreto_modular(secreto, n, prime_mod):
    coeficientes = generar_polinomio_modular(secreto, n, prime_mod)
    partes = []
    for i in range(1, n + 1):
        x_value = i
        y_value = evaluar_polinomio(coeficientes, x_value, prime_mod)
        partes.append((x_value, y_value))
    return partes


# interpolacion de Lagrange
def lagrange_interpolacion_modular(partes, prime_mod):
    def inverso_modular(a, p):
        return pow(a, p - 2, p)

    secreto = 0
    for i, (xi, yi) in enumerate(partes):
        numerador = 1
        denominador = 1
        for j, (xj, _) in enumerate(partes):
            if i != j:
                numerador = (numerador * -xj) % prime_mod
                denominador = (denominador * (xi - xj)) % prime_mod
        termino = (yi * numerador * inverso_modular(denominador, prime_mod)) % prime_mod
        secreto = (secreto + termino) % prime_mod

    return secreto


# menu
def menu():
    prime_mod = 2087  # este numero primo es el modulo en que se realizan las operaciones
    while True:
        print("\n/// Secreto de Shamir ///")
        print("[1] Generar y dividir un secreto")
        print("[2] Reconstruir un secreto a partir de partes")
        print("[3] Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            secreto = int(input(f"Introduce el valor del secreto (menor que {prime_mod}): "))
            if secreto >= prime_mod:
                print(f"ERROR: El secreto debe ser menor que {prime_mod}!!!")
                continue
            n = int(input("Introduce el número de partes en que deseas dividir el secreto: "))
            k = int(input("Introduce el número mínimo de partes requeridas para reconstruir el secreto: "))

            if k > n:
                print("Error: El valor de k no puede ser mayor que el valor de n.")
                continue

            # Dividir el secreto en partes
            partes = dividir_secreto_modular(secreto, n, prime_mod)

            print("\nLas partes generadas son:")
            for idx, parte in enumerate(partes):
                print(f"Parte {idx + 1}: {parte}")

        elif opcion == '2':
            k = int(input("Introduce el número de partes que vas a ingresar: "))
            partes = []
            print(f"Introduce los valores de las partes en formato (x, y), donde y < {prime_mod}:")
            for i in range(k):
                x = int(input(f"Introduce x{i + 1}: "))
                y = int(input(f"Introduce y{i + 1}: "))
                partes.append((x, y))

            secreto_reconstruido = lagrange_interpolacion_modular(partes, prime_mod)
            print(f"\nEl secreto reconstruido es: {secreto_reconstruido}")

        elif opcion == '3':
            print("Saliendo...")
            break

        else:
            print("Opción no válida !!!.")


# Ejecutar el menú trutrsh
menu()
