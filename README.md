# APLICAÇÃO DA RECEPÇÃO DE CÂMARAS DA CEFP
## OBJETIVO DA APLICAÇÃO
A Congregação Espírita Francisco de Paula oferece tratamentos espirituais de passe nas reuniões públicas. Após comparecer por doze semanas, os frequentadores podem marcar os serviços de vidência e prece. Na vidência, o médium fala sobre o frequentador. Na prece, o frequentador escolhe dois desencarnados e recebe informações deles através do médium. Cada atividade é feita em uma pequena câmara. Na sexta-feira, existem quatro câmaras funcionando: duas de vidência e duas de prece. O frequentador se apresenta à recepção e entra na fila. Existe uma fila única para as duas câmaras de vidência e outra fila única par as duas câmaras de prece. Quando começam os trabalhos, o recepcionista começa a chamar os nomes pela ordem de chegada. A câmara toca uma campaínha avisando que está disponível para chamar o próximo frequentador. O problema é que o recepcionista não consegue identificar qual câmara tocou a campaínha e o som é muito alto atrapalhando a concentração dos trabalhos, por vezes até assustando as pessoas. Esta aplicação tem o objetivo de melhorar a eficiência e a tranquilidade da recepção mostrando em um monitor na sala de espera o nome da pessoa e a câmara que está chamando. A aplicação substituirá o som da campaínha por um som de uma voz em volume adequado dizendo qual câmara está chamando. Estamos trabalhando para que em breve haja um botão físico em cada câmara que se conectará ao programa e chamará o próximo a ser atendido diretamente no monitor da sala de espera. Para mais informações sobre a CEFP acesse cefp.org.br.


## SUMÁRIO
- [`INSTALAÇÃO`](#INSTALAÇÃO)
- [`LINKS DO PROJETO`](#LINKS-DO-PROJETO)

## INSTALAÇÃO
### PRÉ-REQUISITOS
- Instalar Pyhton3: https://www.python.org/downloads/
- Instalar Pip3: https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3/
- Instalar Node: https://nodejs.org/en/download/package-manager

### PARA INICIAR O REACT
Digite os seguintes comandos no terminal:
```
cd front_recepcao
npm i
npm run dev
```
Para acessar no navegador:
http://localhost:5173/

### PARA INICIAR A API
Digite os seguintes comandos no terminal:
```
pip install -r requirements.txt
python app.py
```
Para acessar no navegador:
http://localhost:5001/


## LINKS DO PROJETO
VÍDEO
https://www.youtube.com/watch?v=d2XidcDOZGQ

FRONT GITHUB
https://github.com/luscianaderose/prjrecepcaocefp/tree/main

FIGMA
https://www.figma.com/proto/4WaxuFjrOhR8aIHIlHXuIP/prj-recepcao-cefp-01?node-id=0-1&t=XGYyK7bsqyAa5qK2-1


# DOCKER
## pra entrar na pasta do projeto
cd "/mnt/f/_dev pos puc/prjrecepcaocefp"

## para fazer build da imagem api_recepcao
docker build -t api_recepcao:1.0 api_recepcao
docker build -t api_calendario:1.0 api_calendario
docker build -t front_recepcao:1.0 front_recepcao

## para fazer deploy (serve p rodar os 3 juntos)
docker-compose -f deploy_recepcao/docker-compose.yml up

sempre que alterar o codigo tem que refazer o build. então precisa parar com o 'down' depois o 'up'.

## para parar os containers enquanto estão no background
docker-compose -f deploy_recepcao/docker-compose.yml down

## para fazer deploy rodando em background
d = detatch = rodando em background
docker-compose -f deploy_recepcao/docker-compose.yml up -d

## para ver os logs enquanto estão no background
docker-compose -f deploy_recepcao/docker-compose.yml logs

## para ver quais serviços estão rodando
docker ps

!! proxima aula configura pra nao precisar rodar o build manualmente
ele mesmo faz o build por vc
ajudtar configuração pra nao ficar reinstalando tudo

## para executar teste do botão
curl http://localhost:5001/camara -d '{"numero":"2"}' -H'Content-type: application/json'

## shut down

