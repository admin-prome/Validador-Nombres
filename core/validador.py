import pandas as pd
import numpy as np
import unicodedata
from .singleton_meta import SingletonMeta

class Validador(metaclass=SingletonMeta):
    def normalizar_cadena(self, cadena):  
        s1 = cadena.replace("ñ", "#").replace("Ñ", "%")
        s2 = unicodedata.normalize("NFKD", s1)\
         .encode("ascii","ignore").decode("ascii")\
         .replace("#", "ñ").replace("%", "Ñ")
        return s2
    
    def compararCadena(self, cadena1,cadena2):
        """
        Recibo dos cadenas
        i -> es un contador, para usar de indice
        Se obtienen las longitudes de cadena, si la diferencia entre ellas es mayor a 2 se devuelve 0
        total -> lonfitud menor (int)
        pivot -> cadena con mas longitud(str)
        recorredor -> cadena con menos longitud(str)
        uso recorredor para buscar el caracter en la cadena larga. Si la encuentro, reemplazo en la cadena larga el caracter por una ","
        se realiza hasta fin de la cadena mas corta
        cuento las "," que hay en las cadena larga, luego se divide por la longitud de la misma, lo que devuelve un porcentaje de coincidencia.
        """
        i=0
        longitud1=len(cadena1)
        longitud2=len(cadena2)
        if abs(longitud1-longitud2)>=3 and (cadena1 not in cadena2) and (cadena2 not in cadena1):
            return 0
        if longitud1 > longitud2:
            total=longitud2
            pivot=cadena1
            recorredor=cadena2
        else:
            total=longitud1
            pivot=cadena2
            recorredor=cadena1
        while(i<total):
            if recorredor[i] in pivot:
                pivot = pivot.replace(recorredor[i],",", 1)
            i+=1        
        casos_correctos=pivot.count(",")
        total=len(pivot)
        return (casos_correctos/total)*100
    
    def comparar_NyA_V2(self, nombre, apellido, nombre_completo_nosis):
        """
        las columnas se pasan a minusculas
        aquellas que eran vacias (s/d) devuelven un 0
        separo el nombre en una lista y el apellido tambien. 
        Se compara apellido con el nombre completo de nosis y eso da un resultado
        Se compara nombre con el nombre completo de nosis y eso da un resultado
        Se le da un peso al resultado de nombre y apellido; para devolverlo
        """
        cadena_nombre=nombre
        cadena_apellido=apellido
        cadena_nosis=nombre_completo_nosis
        cadena_nombre=cadena_nombre.lower()
        cadena_apellido=cadena_apellido.lower()
        cadena_nosis=cadena_nosis.lower()
        cadena_nombre=self.normalizar_cadena(cadena_nombre)
        cadena_nosis=self.normalizar_cadena(cadena_nosis)
        cadena_apellido=self.normalizar_cadena(cadena_apellido)
        lista_nombre=cadena_nombre.split()
        lista_apellido=cadena_apellido.split()
        lista_nosis=cadena_nosis.split()
        if "s/d" in lista_apellido:
            resultado_apellido=0
        else:
            resultado_apellido=self.comparador_lista(lista_apellido,lista_nosis)
        if "s/d" in lista_nombre:
            resultado_nombre=0
        else:
            resultado_nombre=self.comparador_lista(lista_nombre,lista_nosis)
        return ((resultado_apellido*0.75) + (resultado_nombre*0.25))
    
    def comparador_lista(self,cad1,cad2):
        """
        Se reciben dos listas. 
        elegida -> es la que tiene menos elementos
        aux -> la que tiene mas elementos
        Por cada elemento de "elegida" lo comparo con cada elemento de "aux". Eso da un resultado. Me quedo con el maximo y saco de "aux" el elemento con mas coincidencia para evitar una futura redudancia.
        Luego me quedo con el maximo de coincidencia y lo devuelvo.
        """
        final=[]
        if len(cad1) > len (cad2):
            elegida=cad2
            aux=cad1
        else:
            elegida=cad1
            aux=cad2
        for eleg in elegida:
            max=0
            i=0
            sacar=0
            for opc in aux:
                resultado=self.compararCadena(eleg,opc)
                if resultado > max:
                    max=resultado
                    sacar=i
                i+=1
            final.append(max)
            aux.pop(sacar)
        if final != []:
            maximo=np.max(final)
        else:
            maximo=0
        return float(maximo)
        
    def comparar_NyA(self,cadena1,cadena2):
        """
        La función comparar_NyA compara el nombre con su razón comercial(nombre en nosis)
        y devuelve un valor entre 0 y 100 que indica cuán similares son.
        Cuanto mayor sea el número, más similares son.
        
        :param fila: Obtiene los valores de las columnas que se van a comparar
        :return: El promedio de la similitud entre dos cadenas
        """
    
        cadena1=cadena1.lower()
        cadena2=cadena2.lower()
        cadena1=self.normalizar_cadena(cadena1)
        cadena2=self.normalizar_cadena(cadena2)
        cad1=cadena1.split()
        cad2=cadena2.split()
        final=[]
        if len(cad1) > len (cad2):
            elegida=cad2
            aux=cad1
        else:
            elegida=cad1
            aux=cad2
        for eleg in elegida:
            max=0
            i=0
            sacar=0
            for opc in aux:
                resultado=self.compararCadena(eleg,opc)
                if resultado > max:
                    max=resultado
                    sacar=i
                i+=1
            final.append(max)
            aux.pop(sacar)
        cantidad=len(final)
        suma=sum(final)
        return (suma/cantidad)
    
    
    def comparador_final(self, nombre, apellido, nombre_completo_nosis):
        nombre_completo = nombre + " " + apellido
        valor_comp_1 = self.comparar_NyA(nombre_completo, nombre_completo_nosis)
        valor_comp_2 = self.comparar_NyA_V2(nombre, apellido,nombre_completo_nosis)
        if valor_comp_1 > valor_comp_2:
            return valor_comp_1
        else:
            return valor_comp_2