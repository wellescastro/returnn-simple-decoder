# returnn-simple-decoder
Repositório destinado a publicação de decodificadores de imagens para o framework RETURNN.


#### Decodificando uma única imagem

Para realizar a decodificação de uma imagem qualquer, são necessários dois passos:

1. Executar o RETURNN no modo "daemon", no qual é levantado um servidor local que pode receber requisições de decodificação.
  
  Nessa primeira etapa, é necessário definir um arquivo de configuração especificando o modelo a ser executado, através do comando:
  > path/to/returnn/rnn.py filename.config
	
	Modelo do arquivo de configuração: IAM-exemplo.config

2. Executar um script (single-image-decoder.py) para se conectar ao servidor e realizar a transcrição do texto.
	
	Obs.: É necessário editar a variável img_path com o caminho completo da imagem a ser reconhecida
