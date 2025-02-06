import pygame, math, numpy as np, panda as pd
pygame.init()


comprimentoTela=1024
alturaTela=700
G=0.1#6.6743e-11
fonte=pygame.font.Font(None,36)
fps=pygame.time.Clock()
dt=fps.tick(6)/1000

df=pd.DataFrame(dados,columns=["x","y","vx","vy","ax","ay"])
df.to_csv("dadosDoTreinamento.csv",index=False)


class Planeta:
    def __init__(self,nome,corOriginal,posicao,massa,raio,velocidade):
        self.nome=nome
        self.corOriginal=corOriginal
        self.corDinamica=corOriginal
        self.posicao=np.array(posicao,dtype=np.float64) #[x y]
        self.massa=massa
        self.raio=raio
        self.velocidade=np.array(velocidade,dtype=np.float64) #[vx vy]
        self.aceleracao=np.zeros(2,dtype=np.float64) #[ax ay] começa com zero em cada uma das posições
        self.trajetoria=[(posicao[0],posicao[1])]


    def desenhaCorpo(self,tela):
        pygame.draw.circle(tela,self.corDinamica,((int(math.floor(self.posicao[0]))),int(math.floor(self.posicao[1]))),self.raio)





class SistemaEstelar:
    def __init__(self,corposNaoErrantes):
        self.win=pygame.display.set_mode([comprimentoTela,alturaTela])
        self.corposNaoErrantes=corposNaoErrantes
        self.colisao=False
        self.tempoDoAlerta=0

    def distanciaEntreCorpos(self,corpo1,corpo2):
        return ((corpo1.posicao[0]-corpo2.posicao[0])**2+(corpo1.posicao[1]-corpo2.posicao[1])**2)**(0.5)

    def verificaColisao(self,corpo1,corpo2):
        if self.distanciaEntreCorpos(corpo1,corpo2)<=(corpo1.raio+corpo2.raio):
            return True
        else: return False

    def geraQuadro(self):
        self.win.fill((0,0,0))
        self.baleEstelar()
        for planeta in self.corposNaoErrantes:
            for outroPlaneta in self.corposNaoErrantes:
                if planeta!=outroPlaneta:
                    if self.verificaColisao(planeta,outroPlaneta)==True:
                        self.tempoDoAlerta=100
        if self.tempoDoAlerta>0:
            self.tempoDoAlerta-=1
            self.corposNaoErrantes[0].corDinamica=(255,255,255)  # Alterar cor para indicar colisão
            self.corposNaoErrantes[1].corDinamica=(255,255,255)
            self.corposNaoErrantes[2].corDinamica=(255,255,255)
            alert_text=fonte.render("COLISÃO DETECTADA!!!",True,(255,255,255))  # Renderizar o texto
            self.win.blit(alert_text,(350,50))
        elif self.tempoDoAlerta<1:
            self.corposNaoErrantes[0].corDinamica = self.corposNaoErrantes[0].corOriginal
            self.corposNaoErrantes[1].corDinamica = self.corposNaoErrantes[1].corOriginal
            self.corposNaoErrantes[2].corDinamica = self.corposNaoErrantes[2].corOriginal
        pygame.display.update()
        pygame.display.flip()

    def calculaVetor(self,corpos):
        n = len(corpos)
        aceleracoes = [np.zeros(2, dtype=np.float64) for _ in range(n)]
        for corpo in range(n):
            for outroCorpo in range(n):
                if corpo != outroCorpo:
                    distancia = math.sqrt((corpos[outroCorpo].posicao[0] - corpos[corpo].posicao[0]) ** 2 + (corpos[outroCorpo].posicao[1] - corpos[corpo].posicao[1]) ** 2) + (1e-10)  # isso vai evitar divisão por zero
                    forca = (G * corpos[corpo].massa * corpos[outroCorpo].massa) / (distancia ** 2)
                    #direcao = ((corpos[outroCorpo].posicao[0] - corpos[corpo].posicao[0]) - (corpos[outroCorpo].posicao[1] - corpos[corpo].posicao[1])) / distancia  # Vetor unitário
                    direcao = (corpos[outroCorpo].posicao - corpos[corpo].posicao) / distancia
                    aceleracoes[corpo] += (forca / corpos[corpo].massa) * direcao
        return aceleracoes

    def metodoVerlet(self,corpos):
        for corpo in corpos:
            #corpo.posicao[0] += corpo.velocidade[0] * dt + 0.5 * corpo.aceleracao[0] * (dt ** 2)
            #corpo.posicao[1] += corpo.velocidade[1] * dt + 0.5 * corpo.aceleracao[1] * (dt ** 2)
            corpo.posicao += corpo.velocidade * dt + 0.5 * corpo.aceleracao * (dt ** 2)
            corpo.trajetoria.append([corpo.posicao[0],corpo.posicao[1]])
        novaAceleracao = self.calculaVetor(corpos)
        for i, corpo in enumerate(corpos):
            corpo.velocidade += 0.5 * (corpo.aceleracao + novaAceleracao[i]) * dt
            corpo.aceleracao = novaAceleracao[i]



    def baleEstelar(self):
        for planeta in self.corposNaoErrantes:
            self.metodoVerlet(self.corposNaoErrantes)
            planeta.desenhaCorpo(self.win)
            for posicao in planeta.trajetoria:
                #self.win.fill((255,0,0),((posicao[0],posicao[1],1,1)))
                self.win.fill(planeta.corOriginal,((posicao[0],posicao[1],1,1)))


def main():
    #teste=Planeta('nome',cirOri,x,y,massa,raio,velocidade)
    lua = Planeta('Lua', (128, 128, 128), [624, 350], 7.35e2, 15, [-9,2])
    terra = Planeta('Terra', (0, 0, 255), [412, 350], 5.97e4, 15, [-7,7])
    sol = Planeta('Sol', (255, 255, 0), [250, 250], 1.989e5, 30, [2,-1])


    rodando = True
    solar = SistemaEstelar([lua, terra, sol])
    #satelite = Planeta('sputnik',(128,128,128),(128,128,128),712,350,130,5,120,15)
    #solar = SistemaEstelar([terra,satelite])
    while rodando:

        solar.geraQuadro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

main()