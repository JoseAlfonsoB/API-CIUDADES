import math
from operator import itemgetter

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def en_ruta(rutas, c):
    for r in rutas:
        if c in r:
            return r
    return None

def peso_ruta(ruta, pedidos):
    return sum(pedidos[c] for c in ruta)

def distancia_ruta(ruta, coord, almacen):
    total = distancia(almacen, coord[ruta[0]])
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], almacen)
    return total

def consumo_gasolina(distancia):
    return distancia / 10  # 10 km por litro

def vrp_voraz(coord, pedidos, almacen, max_carga, max_distancia, max_gasolina):
    s = {}
    for c1 in coord:
        for c2 in coord:
            if c1 != c2 and (c2, c1) not in s:
                d_c1_c2 = distancia(coord[c1], coord[c2])
                d_c1_almacen = distancia(coord[c1], almacen)
                d_c2_almacen = distancia(coord[c2], almacen)
                s[c1, c2] = d_c1_almacen + d_c2_almacen - d_c1_c2

    s = sorted(s.items(), key=itemgetter(1), reverse=True)
    rutas = []

    for (c1, c2), _ in s:
        rc1 = en_ruta(rutas, c1)
        rc2 = en_ruta(rutas, c2)

        def validar_y_agregar(nueva_ruta):
            peso = peso_ruta(nueva_ruta, pedidos)
            dist = distancia_ruta(nueva_ruta, coord, almacen)
            gas = consumo_gasolina(dist)
            if peso <= max_carga and dist <= max_distancia and gas <= max_gasolina:
                return peso, dist, gas, nueva_ruta
            return None

        if rc1 is None and rc2 is None:
            result = validar_y_agregar([c1, c2])
            if result:
                rutas.append(result[3])
        elif rc1 and rc2 is None:
            if rc1[0] == c1:
                nueva = [c2] + rc1
            elif rc1[-1] == c1:
                nueva = rc1 + [c2]
            else:
                continue
            result = validar_y_agregar(nueva)
            if result:
                rutas[rutas.index(rc1)] = result[3]
        elif rc1 is None and rc2:
            if rc2[0] == c2:
                nueva = [c1] + rc2
            elif rc2[-1] == c2:
                nueva = rc2 + [c1]
            else:
                continue
            result = validar_y_agregar(nueva)
            if result:
                rutas[rutas.index(rc2)] = result[3]
        elif rc1 != rc2:
            if rc1[0] == c1 and rc2[-1] == c2:
                nueva = rc2 + rc1
            elif rc1[-1] == c1 and rc2[0] == c2:
                nueva = rc1 + rc2
            else:
                continue
            result = validar_y_agregar(nueva)
            if result:
                rutas.remove(rc1)
                rutas.remove(rc2)
                rutas.append(result[3])
    return rutas
