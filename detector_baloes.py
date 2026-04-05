#!/usr/bin/env python3
"""
Programa para detecção de balões usando OpenCV em Raspberry Pi com câmera USB
Autor: Assistente de Código
"""

import cv2
import numpy as np
import time

class BalaoDetector:
    def __init__(self, camera_id=0):
        """
        Inicializa o detector de balões
        
        Args:
            camera_id: ID da câmera USB (geralmente 0 para a primeira câmera)
        """
        self.camera_id = camera_id
        self.cap = None
        self.baloes_detectados = []
        
        # Parâmetros para detecção de círculos (ajustáveis para balões)
        self.min_dist = 50  # Distância mínima entre círculos
        self.param1 = 50    # Limiar superior para detecção de bordas Canny
        self.param2 = 30    # Limiar para identificação de círculos
        self.min_radius = 20  # Raio mínimo do balão
        self.max_radius = 200  # Raio máximo do balão
        
    def iniciar_camera(self):
        """Inicia a captura da câmera USB"""
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            print(f"Erro: Não foi possível abrir a câmera {self.camera_id}")
            return False
            
        # Configurações opcionais para melhorar a qualidade
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"Câmera {self.camera_id} iniciada com sucesso!")
        return True
    
    def detectar_baloes(self, frame):
        """
        Detecta balões no frame usando transformação de Hough para círculos
        
        Args:
            frame: Imagem BGR do frame da câmera
            
        Returns:
            Lista de círculos detectados (x, y, raio)
        """
        # Converter para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aplicar blur para reduzir ruído
        gray_blur = cv2.medianBlur(gray, 5)
        
        # Detectar círculos usando Hough Circle Transform
        circulos = cv2.HoughCircles(
            gray_blur,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=self.min_dist,
            param1=self.param1,
            param2=self.param2,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )
        
        self.baloes_detectados = []
        
        if circulos is not None:
            # Arredondar os valores para inteiros
            circulos = np.round(circulos[0, :]).astype("int")
            
            for (x, y, raio) in circulos:
                self.baloes_detectados.append((x, y, raio))
                
        return self.baloes_detectados
    
    def desenhar_detecoes(self, frame, baloes):
        """
        Desenha os balões detectados no frame
        
        Args:
            frame: Imagem original
            baloes: Lista de balões detectados (x, y, raio)
            
        Returns:
            Frame com as detecções desenhadas
        """
        frame_saida = frame.copy()
        
        for (x, y, raio) in baloes:
            # Desenhar o círculo externo
            cv2.circle(frame_saida, (x, y), raio, (0, 255, 0), 2)
            
            # Desenhar o centro do círculo
            cv2.circle(frame_saida, (x, y), 2, (0, 0, 255), 3)
            
            # Adicionar texto com coordenadas
            cv2.putText(frame_saida, f"Balao: ({x}, {y})", 
                       (x - 50, y - raio - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Adicionar contador de balões
        texto_contador = f"Baloes detectados: {len(baloes)}"
        cv2.putText(frame_saida, texto_contador, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame_saida
    
    def processar_frame(self, frame):
        """
        Processa um frame completo: detecta e desenha balões
        
        Args:
            frame: Frame da câmera
            
        Returns:
            Frame processado com detecções
        """
        baloes = self.detectar_baloes(frame)
        frame_processado = self.desenhar_detecoes(frame, baloes)
        return frame_processado
    
    def executar(self, mostrar_janela=True, salvar_video=False):
        """
        Executa o loop principal de detecção
        
        Args:
            mostrar_janela: Se True, mostra a janela com o vídeo
            salvar_video: Se True, salva o vídeo com detecções
        """
        if not self.iniciar_camera():
            return
        
        # Configurar salvamento de vídeo se necessário
        out = None
        if salvar_video:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('baloes_detectados.avi', fourcc, 20.0, (640, 480))
        
        print("\nPressione 'q' para sair, 's' para salvar foto, 'p' para pausar")
        print("Iniciando detecção de balões...\n")
        
        pausado = False
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Erro ao capturar frame")
                    break
                
                if not pausado:
                    frame_processado = self.processar_frame(frame)
                else:
                    frame_processado = frame
                    cv2.putText(frame_processado, "PAUSADO", (10, 450),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Salvar vídeo se configurado
                if salvar_video and out is not None:
                    out.write(frame_processado)
                
                # Mostrar frame se configurado
                if mostrar_janela:
                    cv2.imshow('Detecao de Baloes', frame_processado)
                    
                    # Teclas de controle
                    tecla = cv2.waitKey(1) & 0xFF
                    
                    if tecla == ord('q'):
                        print("\nEncerrando...")
                        break
                    elif tecla == ord('s'):
                        nome_arquivo = f"foto_balao_{int(time.time())}.jpg"
                        cv2.imwrite(nome_arquivo, frame_processado)
                        print(f"Foto salva: {nome_arquivo}")
                    elif tecla == ord('p'):
                        pausado = not pausado
                        estado = "pausado" if pausado else "ativo"
                        print(f"Processo {estado}")
        
        except KeyboardInterrupt:
            print("\nInterrupto pelo usuário")
        
        finally:
            # Liberar recursos
            if out is not None:
                out.release()
            self.parar()
    
    def parar(self):
        """Libera os recursos da câmera"""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Recursos liberados.")
    
    def ajustar_parametros(self, min_dist=None, param1=None, param2=None, 
                          min_radius=None, max_radius=None):
        """
        Ajusta os parâmetros de detecção
        
        Args:
            min_dist: Distância mínima entre círculos
            param1: Limiar superior para Canny
            param2: Limiar para identificação de círculos
            min_radius: Raio mínimo
            max_radius: Raio máximo
        """
        if min_dist is not None:
            self.min_dist = min_dist
        if param1 is not None:
            self.param1 = param1
        if param2 is not None:
            self.param2 = param2
        if min_radius is not None:
            self.min_radius = min_radius
        if max_radius is not None:
            self.max_radius = max_radius
        
        print("Parâmetros atualizados:")
        print(f"  min_dist: {self.min_dist}")
        print(f"  param1: {self.param1}")
        print(f"  param2: {self.param2}")
        print(f"  min_radius: {self.min_radius}")
        print(f"  max_radius: {self.max_radius}")


def main():
    """Função principal"""
    print("=" * 50)
    print("DETECTOR DE BALOES - Raspberry Pi + Camera USB")
    print("=" * 50)
    
    # Criar instância do detector
    detector = BalaoDetector(camera_id=0)
    
    # Ajuste opcional dos parâmetros (descomente para ajustar)
    # detector.ajustar_parametros(min_dist=30, param1=100, param2=25, 
    #                             min_radius=15, max_radius=150)
    
    # Executar detecção
    detector.executar(mostrar_janela=True, salvar_video=False)


if __name__ == "__main__":
    main()
