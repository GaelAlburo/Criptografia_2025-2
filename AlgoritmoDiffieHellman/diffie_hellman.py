# Autor: Rodrigo Gael Guzmán Alburo

from sympy import isprime


def solicitar_valores(type):
    """
    Solicita al usuario un valor entero positivo y lo verifica.

    Args:
        tpe(str): Tipo de valor a solicitar ('P', 'G', 'a' o 'b').

    Returns:
        int: Valor ingresado por el usuario.
    """

    print(f"Ingrese el valor de '{type}' (entero positivo): ")
    n = input()
    while not n.isnumeric():
        print(f"¡Error! Ingrese un número entero positivo para '{type}': ")
        n = input()
    return int(n)


def deffie_hellman(p, g):
    """
    Implementación del algoritmo de Diffie-Hellman para el intercambio de claves.

    Args:
        p (int): Número primo.
        g (int): Generador.
    """

    a = solicitar_valores("a")

    b = solicitar_valores("b")

    A = (g**a) % p
    print(f"(Alice) Valor calculado de A: {A}")

    B = (g**b) % p
    print(f"(Bob) Valor calculado de B: {B}")

    print("\n---CALCULO DE LLAVES---")

    k_a = (B**a) % p
    print(f"(Alice) Valor obtenido de la llave k: {k_a}")

    k_b = (A**b) % p
    print(f"(Bob) Valor obtenido de la llave k: {k_b}")


def main():
    """Programa principal"""
    print("\n\t----Algoritmo de Diffie-Hellman----\n")
    p = solicitar_valores("P")
    g = solicitar_valores("G")

    while g >= p:
        print("El valor G debe ser menor a P. Intente nuevamente.")
        g = solicitar_valores("G")

    deffie_hellman(p, g)


if __name__ == "__main__":
    main()
