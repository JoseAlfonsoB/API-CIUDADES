from flask import Flask, request, jsonify
from rutas import vrp_voraz, distancia_ruta, peso_ruta, consumo_gasolina
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Datos globales
coord = {
    'EDO.MEX': (19.2938258568844, -99.65366252023884),
    'QRO': (20.593537489366717, -100.39004057702225),
    'CDMX': (19.432854452264177, -99.13330004822943),
    'SLP': (22.151725492903953, -100.97657666103268),
    'MTY': (25.673156272083876, -100.2974200019319),
    'PUE': (19.063532268065185, -98.30729139446866),
    'GDL': (20.67714565083998, -103.34696388920293),
    'MICH': (19.702614895389996, -101.19228631929688),
    'SON': (29.075273188617818, -110.95962477655333)
}
pedidos = {
    'EDO.MEX': 10,
    'QRO': 13,
    'CDMX': 7,
    'SLP': 11,
    'MTY': 15,
    'PUE': 8,
    'GDL': 6,
    'MICH': 7,
    'SON': 8
}

@app.route('/ruta-optima', methods=['POST'])
def calcular_ruta():
    data = request.json
    origen = data.get('origen')
    destino = data.get('destino')
    max_carga = data.get('max_carga')
    max_distancia = data.get('max_distancia')
    max_gasolina = data.get('max_gasolina')

    if origen not in coord or destino not in coord:
        return jsonify({'error': 'Ciudad no válida'}), 400

    almacen = coord[origen]

    rutas = vrp_voraz(coord, pedidos, almacen, max_carga, max_distancia, max_gasolina)

    resultado = []
    for ruta in rutas:
        if destino in ruta:
            dist = distancia_ruta(ruta, coord, almacen)
            gas = consumo_gasolina(dist)
            resultado.append({
                'ruta': ruta,
                'peso_total': peso_ruta(ruta, pedidos),
                'distancia_total': round(dist, 2),
                'consumo_gasolina': round(gas, 2)
            })

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
