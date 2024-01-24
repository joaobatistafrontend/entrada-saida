from django.views.generic import View,TemplateView
from typing import Any
from django.shortcuts import render, redirect
from .models import Pessoa,Verificacao,Empresa
import face_recognition
import numpy as np
from django.views.generic import TemplateView,CreateView,View,ListView,UpdateView,DeleteView
import io
from django.http import JsonResponse
from datetime import datetime
import cv2
import os
from django.utils import timezone  


class Index(TemplateView):
    template_name = 'index.html'


    @staticmethod
    def recognize_face(uploaded_image):
        pessoas = Pessoa.objects.all()

        # Salvar temporariamente a imagem usando OpenCV
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, 'wb') as temp_image_file:
            temp_image_file.write(uploaded_image)

        # Carregar a imagem temporária usando OpenCV
        imagem_enviada = cv2.imread(temp_image_path)
        # Converta a imagem para RGB (face_recognition usa RGB)
        imagem_enviada_rgb = cv2.cvtColor(imagem_enviada, cv2.COLOR_BGR2RGB)
        # Detectar rosto na imagem
        face_locations = face_recognition.face_locations(imagem_enviada_rgb)

        if not face_locations:
            # Remover a imagem temporária após o uso
            os.remove(temp_image_path)
            return None

        # Codificar os rostos encontrados
        imagem_enviada_encodings = face_recognition.face_encodings(imagem_enviada_rgb, face_locations)

        for person in pessoas:
            # Carregar encodings da pessoa do banco de dados
            pessoa_encodings = face_recognition.face_encodings(face_recognition.load_image_file(person.imagem.path))

            for i, encoding in enumerate(imagem_enviada_encodings):
                # Comparar o encoding do rosto encontrado com o encoding da pessoa
                result = face_recognition.compare_faces(pessoa_encodings, encoding)

                if any(result):
                    horario_atual = timezone.now()

                    # Verificar a última verificação para esta pessoa
                    ultima_verificacao = Verificacao.objects.filter(
                        pessoa=person
                    ).order_by('-horario').first()

                    if ultima_verificacao:
                        # Se a última verificação foi uma entrada, registrar uma saída
                        if ultima_verificacao.entrada_correta:
                            Verificacao.objects.create(
                                pessoa=person,
                                horario=horario_atual,
                                entrada_correta=False,
                                saida_correta=True
                            )
                        else:
                            # Se a última verificação foi uma saída, registrar uma entrada
                            Verificacao.objects.create(
                                pessoa=person,
                                horario=horario_atual,
                                entrada_correta=True,
                                saida_correta=False
                            )
                    else:
                        # Se não há verificações anteriores, registrar uma entrada
                        Verificacao.objects.create(
                            pessoa=person,
                            horario=horario_atual,
                            entrada_correta=True,
                            saida_correta=False
                        )

                    # Remover a imagem temporária após o uso
                    os.remove(temp_image_path)

                    # Aqui você pode adicionar lógica adicional ou retornar o resultado desejado
                    return person.nome, horario_atual.strftime("Horario %H:%M:%S"), horario_atual.strftime("Data %Y-%m-%d")


        # Remover a imagem temporária após o uso
        os.remove(temp_image_path)
        return None
    

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):        
        try:
            uploaded_image = request.FILES['image'].read()
            
            nome_pessoa = self.recognize_face(uploaded_image)
            if nome_pessoa:
                return render(request, self.template_name, {'nome_pessoa': nome_pessoa, 'error': None})

            else:
                return render(request, self.template_name, {'nao reco': nome_pessoa, 'error': 'Pessoa não reconhecida.'})

        except Exception as e:
            return render(request, self.template_name, {'error': f"Erro no reconhecimento facial: {str(e)}", 'nome_pessoa': None})
                    
