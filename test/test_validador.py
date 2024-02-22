import sys
sys.path.append("..")
from core.validador import Validador

class Test:
    validador = Validador()
    def test_normalizar(self):
        json = {"nombre": "Matías D'Onofio", "apellido": "Caños"}
        nombre_normalizado = self.validador.normalizar_cadena(json["nombre"])
        apellido_normalizado = self.validador.normalizar_cadena(json["apellido"])
        assert nombre_normalizado == "Matias D'Onofio"
        assert apellido_normalizado == "Caños"

    def test_comparar_correcto(self):
        json = {"nombre": "Matías D'Onofio", "apellido": "Caños", "nombre_completo_nosis": "Matias D'Onofio Caños"}
        resultado = self.validador.comparador_final(json["nombre"], json["apellido"], json["nombre_completo_nosis"])
        assert resultado == 100.0

    def test_comparar_incorrecto(self):
        json = {"nombre": "Nahuel ", "apellido": "Caños", "nombre_completo_nosis": "Matias D'Onofio"}
        resultado = self.validador.comparador_final(json["nombre"], json["apellido"], json["nombre_completo_nosis"])
        assert resultado != 100.0
    
    def test_comparar_incorrecto_2(self):
        json = {"nombre": "Nahuel ", "apellido": "Jeremias", "nombre_completo_nosis": "Matias D'Onofio"}
        resultado = self.validador.comparador_final(json["nombre"], json["apellido"], json["nombre_completo_nosis"])
        assert resultado != 100.0
