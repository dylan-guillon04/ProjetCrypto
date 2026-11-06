from math import gcd
from itertools import combinations
from random import sample, seed
from Crypto.Util.number import getPrime


def generer_modulos():
    seed(1)
    pool = [getPrime(512) for _ in range(10)]
    modulo = []
    for _ in range(20):
        p, q = sample(pool, 2)
        modulo.append((p, q, p * q))
    return modulo


def afficher_collisions(modulo):
    print("=== Attaque RSA par collision ===")
    print("Recherche de collisions entre les modules RSA...")
    found = False
    for (i, a), (j, b) in combinations(enumerate(modulo), 2):
        pgdc = gcd(a[2], b[2])
        if 1 < pgdc < a[2]:
            found = True
            print(f"N{i:02d} et N{j:02d} partagent le premier {str(pgdc)[:10]}...")
    if not found:
        print("Aucune collision trouvée.")
    print()


def retrouver_facteur_partage(modulo):
    e = 65537
    p_original, q_original, n = modulo[0]
    p = None
    for j, (_, _, other_N) in enumerate(modulo[1:], start=1):
        pgdc = gcd(n, other_N)
        if 1 < pgdc < n:
            p = pgdc
            print(f"Facteur partagé détecté entre N{0:02d} et N{j:02d} : {str(p)[:10]}...")
            break

    if p is None:
        raise ValueError(f"Aucun facteur partagé trouvé pour N{0:02d}")

    q = n // p
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    print(f"p = {str(p)[:10]}...")
    print(f"q = {str(q)[:10]}...")
    print(f"phi(N) = {str(phi)[:10]}...")
    print(f"d = {str(d)[:10]}...")
    print()
    return p_original, q_original, n, p, q, e, d


def valider_cle_privee(modulo, p, q, n, e, d):
    p_original, q_original, _ = modulo[0]
    m = 42
    c = pow(m, e, n)
    m_dechiffre = pow(c, d, n)
    assert m_dechiffre == m
    assert sorted((p, q)) == sorted((p_original, q_original))
    print(f"Validation réussie : message déchiffré = {m_dechiffre}")
    print("Les facteurs retrouvés correspondent aux facteurs générés.")



if __name__ == "__main__":
    modulo = generer_modulos()
    afficher_collisions(modulo)
    p_original, q_original, n, p, q, e, d = retrouver_facteur_partage(modulo)
    valider_cle_privee(modulo, p, q, n, e, d)
