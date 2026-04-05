# Detector de Balões com OpenCV para Raspberry Pi

Programa em Python para detecção de balões usando uma câmera USB conectada a um Raspberry Pi.

## Requisitos

- Raspberry Pi (qualquer modelo com portas USB)
- Câmera USB compatível
- Python 3.x
- OpenCV
- NumPy

## Instalação no Raspberry Pi

```bash
# Atualizar o sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependências do sistema
sudo apt-get install -y python3-pip python3-dev libatlas-base-dev libjasper-dev \
    libqtgui4 libqt4-test python3-tk

# Instalar pacotes Python
pip3 install opencv-python numpy

# Alternativamente, para melhor performance no Raspberry Pi:
# pip3 install opencv-contrib-python-headless numpy
```

## Como Usar

### Execução Básica

```bash
python3 detector_baloes.py
```

### Controles Durante a Execução

- **q**: Sair do programa
- **s**: Salvar foto do frame atual
- **p**: Pausar/retomar a detecção

## Funcionalidades

1. **Detecção de Círculos**: Usa a Transformada de Hough para identificar formas circulares
2. **Visualização em Tempo Real**: Mostra os balões detectados com contornos verdes
3. **Contador de Balões**: Exibe quantos balões foram detectados
4. **Salvar Fotos**: Permite capturar frames com as detecções
5. **Parâmetros Ajustáveis**: Fácil ajuste dos parâmetros de detecção

## Ajuste de Parâmetros

Para melhorar a detecção, você pode ajustar os parâmetros no código:

```python
detector = BalaoDetector(camera_id=0)
detector.ajustar_parametros(
    min_dist=30,      # Distância mínima entre círculos
    param1=100,       # Limiar superior para Canny
    param2=25,        # Limiar para identificação de círculos
    min_radius=15,    # Raio mínimo do balão
    max_radius=150    # Raio máximo do balão
)
```

### Descrição dos Parâmetros

- **min_dist**: Distância mínima entre os centros dos círculos detectados
- **param1**: Limiar superior para o detector de bordas Canny
- **param2**: Limiar acumulativo para o centro do círculo (quanto menor, mais círculos falsos)
- **min_radius**: Menor raio de círculo a ser detectado
- **max_radius**: Maior raio de círculo a ser detectado

## Dicas para Melhor Detecção

1. **Iluminação**: Use boa iluminação para melhor contraste
2. **Fundo**: Prefira fundos uniformes e contrastantes
3. **Distância**: Ajuste `min_radius` e `max_radius` conforme a distância da câmera
4. **Calibração**: Teste diferentes valores de `param2` para reduzir falsos positivos

## Uso como Módulo

Você também pode importar e usar em seu próprio código:

```python
from detector_baloes import BalaoDetector

detector = BalaoDetector(camera_id=0)
detector.executar(mostrar_janela=True, salvar_video=False)
```

## Solução de Problemas

### Câmera não é detectada
- Verifique se a câmera está conectada: `lsusb`
- Tente mudar o `camera_id` para 1, 2, etc.
- Teste a câmera com: `fswebcam test.jpg`

### Detecção ruim
- Ajuste os parâmetros de detecção
- Melhore a iluminação do ambiente
- Use balões com cores contrastantes ao fundo

### Performance lenta no Raspberry Pi
- Reduza a resolução do frame
- Use `opencv-python-headless` sem interface gráfica
- Considere usar a câmera oficial do Raspberry Pi (CSI)

## Licença

Este código é fornecido como exemplo educacional. Sinta-se livre para modificar e distribuir.
