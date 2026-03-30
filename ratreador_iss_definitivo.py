import requests
import folium
import math

# Coordenadas aproximadas de São Gonçalo
SGR_LAT, SGR_LON = -22.8269, -43.0539

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0  # Raio da Terra
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def obter_posicao_iss():
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    headers = {'User-Agent': 'Mozilla/5.0'} # "Disfarce" para a API aceitar melhor
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        dados = response.json()
        return float(dados['latitude']), float(dados['longitude'])
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return None, None

def criar_rastreador():
    lat_iss, lon_iss = obter_posicao_iss()
    
    if lat_iss is not None:
        distancia = calcular_distancia(SGR_LAT, SGR_LON, lat_iss, lon_iss)
        print(f"ISS encontrada! Distância de São Gonçalo: {distancia:.2f} km")
        
        # Cria o mapa
        mapa = folium.Map(location=[lat_iss, lon_iss], zoom_start=3)
        
        # Marcador da ISS
        folium.Marker([lat_iss, lon_iss], popup="ISS", icon=folium.Icon(color='red')).add_to(mapa)
        
        # Marcador da sua casa (São Gonçalo)
        folium.Marker([SGR_LAT, SGR_LON], popup="Minha Casa", icon=folium.Icon(color='blue')).add_to(mapa)
        
        mapa.save("rastreador_iss.html")
        print("Arquivo 'rastreador_iss.html' gerado!")
    else:
        print("Falha na missão. Tente novamente em alguns minutos.")

if __name__ == "__main__":
    criar_rastreador()