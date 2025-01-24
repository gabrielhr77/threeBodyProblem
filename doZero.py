import pygame, math
pygame.init()

comprimentoTela=1024
larguraTela=700
G=0.1
fonte=pygame.font.Font(None,36)
fps=pygame.time.Clock()
vetorBase=[10,10]
dt = fps.tick(60)

class Planeta:
    def __init__(self,nome,corOriginal,corDinamica,posicaoX,posicaoY,massa,raio,anguloVel,moduloVel):
        self.nome = nome
        self.corOriginal = corOriginal
        self.corDinamica = corDinamica
        self.posicaoX = posicaoX
        self.posicaoY = posicaoY
        self.massa = massa
        self.raio = raio
        self.anguloVel = anguloVel
        self.moduloVel = moduloVel
        self.velocidadeX = self.moduloVel*math.cos(math.radians(anguloVel))
        self.velocidadeY = self.moduloVel*math.sin(math.radians(anguloVel))
        self.trajetoria = [[posicaoX,posicaoY]]

    def movimentoPlaneta(self, acelX, acelY, dt):
        self.velocidadeX += acelX*(dt/1000)
        self.velocidadeY += acelY*(dt/1000)
        self.posicaoX += self.velocidadeX*(dt/1000)
        self.posicaoY += self.velocidadeY*(dt/1000)
        self.trajetoria.append([self.posicaoX, self.posicaoY])

    def desenhaCorpo(self,tela):
        pygame.draw.circle(tela,self.corDinamica,((int(math.floor(self.posicaoX))),int(math.floor(self.posicaoY))),self.raio)

class SistemaEstelar:
    def __init__(self,corposNaoErrantes):
        self.win=pygame.display.set_mode([comprimentoTela,larguraTela])
        self.corposNaoErrantes=corposNaoErrantes
        self.colisao=False
        self.tempoDoAlerta=0

    def distanciaEntreCorpos(self,corpo1,corpo2):
        return ((corpo1.posicaoX-corpo2.posicaoX)**2+(corpo1.posicaoY-corpo2.posicaoY)**2)**(0.5)

    def verificaColisao(self,corpo1,corpo2):
        if self.distanciaEntreCorpos(corpo1,corpo2)<=(corpo1.raio+corpo2.raio):
            return True
        else: return False

    def calculaVetor(self,planeta):
        fGravX=0
        fGravY=0
        for outroPlaneta in self.corposNaoErrantes:
            distancia=self.distanciaEntreCorpos(planeta,outroPlaneta)
            if planeta.nome!=outroPlaneta.nome:# and distancia>10:
                fGravitacional=(G*planeta.massa*outroPlaneta.massa)/(self.distanciaEntreCorpos(planeta,outroPlaneta)**2)
                angulo=math.atan2(planeta.posicaoY-outroPlaneta.posicaoY,planeta.posicaoX-outroPlaneta.posicaoX)
                fGravX-=fGravitacional*math.cos(angulo)#aqui é menos por causa do cálculo do ângulo
                fGravY-=fGravitacional*math.sin(angulo)
        aceleracaoX=1000*fGravX/planeta.massa
        aceleracaoY=1000*fGravY/planeta.massa
        xPonta=(planeta.posicaoX+aceleracaoX*100)
        yPonta=(planeta.posicaoY+aceleracaoY*100)
        if (math.sqrt((planeta.posicaoX-xPonta)**2+(planeta.posicaoY-yPonta)**2))<100:
            anguloAux = math.atan2(aceleracaoY, aceleracaoX)
            largura_base = 6
            altura_triangulo = 10
            xFront = xPonta + altura_triangulo * math.cos(anguloAux)
            yFront = yPonta + altura_triangulo * math.sin(anguloAux)
            estibordo = (xPonta + largura_base * math.cos(anguloAux + math.pi / 2), yPonta + largura_base * math.sin(anguloAux + math.pi / 2))
            bombordo = (xPonta + largura_base * math.cos(anguloAux - math.pi / 2), yPonta + largura_base * math.sin(anguloAux - math.pi / 2))
            pygame.draw.line(self.win, (255,255,255), (planeta.posicaoX, planeta.posicaoY), (xPonta, yPonta), 2)
            pygame.draw.polygon(self.win, (255, 255, 255), [estibordo, bombordo, (xFront, yFront)])
        return [aceleracaoX,aceleracaoY]

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
            alert_text=fonte.render("COLISÃO DETECTADA!!!",True,(255,255,255))  # Renderizar o texto
            self.win.blit(alert_text,(350,50))
        elif self.tempoDoAlerta<1:
            self.corposNaoErrantes[0].corDinamica = self.corposNaoErrantes[0].corOriginal
            self.corposNaoErrantes[1].corDinamica = self.corposNaoErrantes[1].corOriginal
        pygame.display.update()
        pygame.display.flip()

    def baleEstelar(self):
        for planeta in self.corposNaoErrantes:
            vetor=self.calculaVetor(planeta)
            planeta.movimentoPlaneta(vetor[0],vetor[1],dt)
            planeta.desenhaCorpo(self.win)
            for posicao in planeta.trajetoria:
                #self.win.fill((255,0,0),((posicao[0],posicao[1],1,1)))
                self.win.fill(planeta.corOriginal,((posicao[0],posicao[1],1,1)))

def main():
    #teste=Planeta("nome",corOriginal,corDinamica,posX,posY,massa,raio,anguloVel,moduloVel)
    lua = Planeta('Lua', (128, 128, 128), (128, 128, 128), 624, 350, 100, 5, 140, 5)
    terra = Planeta('Terra', (0, 0, 255), (0, 0, 255), 412, 350, 100, 15, 0, 0)
    rodando = True
    solar = SistemaEstelar([lua, terra])
    while rodando:
        solar.geraQuadro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

main()