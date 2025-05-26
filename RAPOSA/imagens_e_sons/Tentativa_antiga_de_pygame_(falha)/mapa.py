#Legenda Bara localização
#O = linha de chegada
#V= VAZIO
#b = BlOco
#ec =  espinho Bara cima
#eB - espinho Bara baixo
#ed = espinho Bara direita


B = 0 #bloco
P = 0 #preenchimento
L = 0 #limite da tela

# os valores anteriores são iguais, para, caso queiramos colocar uma nova imagem para cada um dos elementos, não seja tão complicado
V = 1 #espaço vazio
EE = 2 #espinho virado para a esquerda
ED = 2 #espinho virado para a direita
EB = 2 #espinho virado para baixo
EC = 2 #espinho virado para cima
R = 6 #posição inicial do personagem
O = 7 #ponto de chegada
#M = 8 #moeda --> galinha
M = 8

MAPA_3 =[
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,B],
    [ED,V,V,V,M,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,M,V,V,V,V,V,V,V,V,EE,B],
    [L,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,O,L,B],
    [L,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,B,B,V,V,B,B,B,B,B,B,L,B],
    [L,V,V,B,V,V,V,V,V,V,V,M,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L,B],
    [L,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L,B],
    [L,V,V,B,V,V,B,B,B,B,B,B,B,B,B,B,B,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L,B],
    [L,V,V,B,V,V,V,V,B,V,V,V,V,V,V,B,B,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L,B],
    [L,V,V,B,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L,B],
    [L,V,V,B,V,V,V,V,B,V,V,V,V,V,V,V,V,V,M,B,V,V,B,V,V,V,B,P,P,P,P,P,L,B],
    [L,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,B,B,B,B,B,B,V,V,V,B,P,P,P,P,P,L,B],
    [L,V,V,R,V,V,V,M,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,P,L,B],
    [L,B,B,B,EC,EC,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,P,L,B],
    [P,P,P,P,P,P,P,P,B,EC,EC,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,L,B],
    [P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L,B],
    [P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L,B],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,B]]

MAPA_2= [
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,B],
    [L,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,O,L,B],
    [L,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,M,L,B],
    [L,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,B,B,L,B],
    [ED,V,V,V,V,V,V,V,V,V,V,V,V,V,M,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,P,P,L,B],
    [L,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,P,P,L,B],
    [L,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,P,P,L,B],
    [L,V,V,B,B,B,B,B,EB,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,B,P,P,L,B],
    [L,V,V,B,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,P,P,L,B],
    [L,V,V,B,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,P,P,L,B],
    [L,V,V,B,V,V,V,B,V,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,B,V,V,B,P,P,L,B],
    [L,V,V,B,B,B,B,B,V,V,V,V,B,V,V,V,V,V,V,V,V,M,B,B,B,V,B,V,V,B,P,P,L,B],
    [L,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,P,P,L,B],
    [L,V,V,V,V,V,R,V,V,B,V,M,B,V,V,V,B,B,B,B,V,V,V,B,B,B,B,V,V,B,P,P,L,B],
    [L,B,B,B,B,B,B,B,B,P,B,B,B,V,V,V,B,B,B,B,V,V,V,B,B,B,B,V,V,B,P,P,L,B],
    [L,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,L,B],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,EC,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,B]]

MAPA_1=[
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,B],
    [L,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,L,B],
    [L,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,L,B],
    [L,O,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,L,B],
    [L,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,L,B],
    [L,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,V,V,V,V,V,V,V,L,B],
    [L,B,B,B,B,B,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,M,V,V,V,V,V,V,L,B],
    [ED,V,V,V,V,M,B,V,V,V,B,B,B,B,B,B,B,B,B,B,V,V,B,B,B,B,B,B,B,B,B,B,L,B],
    [L,V,V,V,V,V,B,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,L,B],
    [L,V,V,B,B,B,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,P,P,P,P,L,B],
    [L,V,V,B,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,B,B,P,P,P,P,L,B],
    [L,V,V,B,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,P,P,P,P,P,P,L,B],
    [L,V,V,B,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,P,P,P,P,P,P,L,B],
    [L,V,V,B,B,B,B,B,B,B,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,P,P,L,B],
    [L,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L,B],
    [L,V,V,R,V,V,V,V,V,V,V,V,V,V,V,M,V,B,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L,B],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,B]]






"""
MAPA_MODELO = [
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L]]
"""