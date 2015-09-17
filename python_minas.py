# -*- coding: utf-8 -*-

import random
import pygame
from pygame.locals import *

import os
import sys
import ctypes

import random

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
    ctypes.windll.user32.SetProcessDPIAware()

##CLASES

class casilla:
	def __init__(self,num,pos,seleccionada,pulsada,marcada,aberta,mina,numero_minas):
		self.num = num
		self.pos = pos
		self.seleccionada = seleccionada
		self.pulsada = pulsada
		self.marcada = marcada
		self.aberta = aberta
		self.mina = mina
		self.numero_minas = numero_minas

##CONSTANTES

MARCO = 5

GROSOR_LINHA = 3

LADO_CADRO = 25

NUM_CADRADOS_FILA = 20
NUM_FILAS = 20

NUM_MINAS = 50

ANCHO_VENTANA = NUM_CADRADOS_FILA * LADO_CADRO + MARCO * 2
ALTO_VENTANA = NUM_FILAS * LADO_CADRO + MARCO * 2

NUM_CASILLAS = NUM_CADRADOS_FILA * NUM_FILAS

FPS = 60

COLOR_FONDO = [210,210,210]
COLOR_CADRO = [120,120,120]
COLOR_SELECCIONADA = [130,130,130]
COLOR_PULSADA = [140,140,140]
COLOR_MARCA = [255,50,50]
COLOR_MINA = [255,0,0]
COLOR_CADRICULA = [200,200,200]

COLOR_TEXTO = [120,120,240]

MAX_ACTUALIZAR = 1

##VARIABLES

actualizar = 1

pos_casilla_mouse = False

lista_casillas = []

actualizacion_completa = True

fora_pantalla = False

#INICIAR PYGAME

pygame.init()

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

Surface_casillas = pygame.Surface((ANCHO_VENTANA-MARCO*2,ALTO_VENTANA-MARCO*2)).convert()

pygame.display.set_caption("Python Buscaminas")

font = pygame.font.SysFont("System", int(LADO_CADRO*1.2))

ON = True

inicio = True

#FUNCIONS

def num(pos):
	return pos[0]+pos[1]*NUM_CADRADOS_FILA
	
def pos(num):
	return [num % NUM_CADRADOS_FILA, num / NUM_CADRADOS_FILA]

def debuxar_casilla(n):

	posicion = pos(n)
		
	rect_cadro = pygame.Rect(posicion[0]*LADO_CADRO,posicion[1]*LADO_CADRO,LADO_CADRO,LADO_CADRO)
	
	casilla = lista_casillas[n]
		
	if casilla.aberta and casilla.mina:
		color_cadro = COLOR_MINA
	elif casilla.aberta:
		color_cadro = COLOR_FONDO
	else:
		color_cadro = COLOR_CADRO
		
	pygame.draw.rect(Surface_casillas,color_cadro,rect_cadro)
		
	if casilla.aberta and casilla.numero_minas and not casilla.mina:
		color = [COLOR_TEXTO[0]+20*casilla.numero_minas,COLOR_TEXTO[1]-20*casilla.numero_minas,COLOR_TEXTO[2]-20*casilla.numero_minas]
		text_numero = font.render(str(casilla.numero_minas),True,color)
		Surface_casillas.blit(text_numero,[
							casilla.pos[0]*LADO_CADRO+text_numero.get_width()/1.6,
							casilla.pos[1]*LADO_CADRO+text_numero.get_height()/5.1
							])
		
	if not casilla.aberta and casilla.marcada:
		text_numero = font.render("?",True,COLOR_MARCA)
		Surface_casillas.blit(text_numero,[
							casilla.pos[0]*LADO_CADRO+text_numero.get_width()/2.,
							casilla.pos[1]*LADO_CADRO+text_numero.get_height()/5.1
							])

def num_minas_colindates(num):

	lista_pos_mirar = [num-(NUM_CADRADOS_FILA+1),num-NUM_CADRADOS_FILA,num-(NUM_CADRADOS_FILA-1),num-1,num+1,
						num+(NUM_CADRADOS_FILA-1),num+NUM_CADRADOS_FILA,num+(NUM_CADRADOS_FILA+1)]
						
	lista_num_eliminar =[]
	
	numero_minas_colindantes = 0
	
	if pos(num)[0] == 0:
		lista_num_eliminar.append(num-(NUM_CADRADOS_FILA+1))
		lista_num_eliminar.append(num-1)
		lista_num_eliminar.append(num+(NUM_CADRADOS_FILA-1))
	if pos(num)[0] == NUM_CADRADOS_FILA-1:
		lista_num_eliminar.append(num-(NUM_CADRADOS_FILA-1))
		lista_num_eliminar.append(num+1)
		lista_num_eliminar.append(num+(NUM_CADRADOS_FILA+1))
	if pos(num)[1] == 0:
		lista_num_eliminar.append(num-(NUM_CADRADOS_FILA+1))
		lista_num_eliminar.append(num-NUM_CADRADOS_FILA)
		lista_num_eliminar.append(num-(NUM_CADRADOS_FILA-1))
	if pos(num)[1] == NUM_FILAS-1:
		lista_num_eliminar.append(num+(NUM_CADRADOS_FILA+1))
		lista_num_eliminar.append(num+NUM_CADRADOS_FILA)
		lista_num_eliminar.append(num+(NUM_CADRADOS_FILA-1))
	lista_num_eliminar = list(set(lista_num_eliminar))
	
	for i in lista_num_eliminar:
		lista_pos_mirar.remove(i)
		
	for i in lista_pos_mirar:
		if lista_casillas[i].mina:
			numero_minas_colindantes += 1
			
	return numero_minas_colindantes
		
	
Surface_casillas.fill(COLOR_CADRO)		

for i in range(NUM_CADRADOS_FILA+1):
	pygame.draw.line(Surface_casillas, COLOR_FONDO, [i*LADO_CADRO, 0], [i*LADO_CADRO,ALTO_VENTANA], GROSOR_LINHA)
		
for i in range(NUM_FILAS+1):
	pygame.draw.line(Surface_casillas, COLOR_FONDO, [0, i*LADO_CADRO], [ANCHO_VENTANA,i*LADO_CADRO], GROSOR_LINHA)

#GENERAR LISTA_CASILLAS

for i in range(NUM_CASILLAS):
								#pos										marcada aberta mina numero
	lista_casillas.append(casilla(i,pos(i),0,0,0,0,0,0))

cont_num_minas = NUM_MINAS
	
while cont_num_minas:
	num_casilla = random.randint(0, NUM_CASILLAS-1)
	if not lista_casillas[num_casilla].mina:
		lista_casillas[num_casilla].mina = True
		cont_num_minas -= 1
		
for i in range(len(lista_casillas)):
	lista_casillas[i].numero_minas = num_minas_colindates(i)

###################################################################
####BUCLE XOGO
###################################################################

while ON:
	
	reloj = pygame.time.Clock()
	
	##DEBUXAR VENTANA
	#--------------------------------------------------
	
	if actualizar:
		ventana.fill(COLOR_FONDO)		
	
		#PEGAR SURFACE_CASILAS
	
	if actualizar:
		ventana.blit(Surface_casillas,(MARCO,MARCO))
	
		#DEBUXAR CADRO_MOUSE
		
	if pos_casilla_mouse:
		
		if not lista_casillas[num_casilla].aberta:
		
			if lista_casillas[num_casilla].pulsada:
				if lista_casillas[num_casilla].marcada:
					color_cadro = COLOR_SELECCIONADA
				else:
					color_cadro = COLOR_PULSADA
			elif lista_casillas[num_casilla].seleccionada:
				color_cadro = COLOR_SELECCIONADA
				
			rect_cadro = pygame.Rect(lista_casillas[num_casilla].pos[0]*LADO_CADRO+MARCO,
												lista_casillas[num_casilla].pos[1]*LADO_CADRO+MARCO,
												LADO_CADRO,LADO_CADRO)	
			pygame.draw.rect(ventana,color_cadro,rect_cadro)
			
			if lista_casillas[num_casilla].marcada:
				text_numero = font.render("?",True,COLOR_MARCA)
				ventana.blit(text_numero,[
							lista_casillas[num_casilla].pos[0]*LADO_CADRO+MARCO+text_numero.get_width()/2.,
							lista_casillas[num_casilla].pos[1]*LADO_CADRO+MARCO+text_numero.get_height()/5.1
							])
		
		#DEBUXAR CADRICULA

	if actualizar:
	
		if actualizacion_completa:

			for i in range(NUM_CADRADOS_FILA+1):
				pygame.draw.line(ventana, COLOR_CADRICULA, [MARCO+i*LADO_CADRO, MARCO], [MARCO+i*LADO_CADRO,ALTO_VENTANA-MARCO], GROSOR_LINHA)
			for i in range(NUM_FILAS+1):
				pygame.draw.line(ventana, COLOR_CADRICULA, [MARCO, MARCO+i*LADO_CADRO], [ANCHO_VENTANA-MARCO,MARCO+i*LADO_CADRO], GROSOR_LINHA)
				
		else:
	
			if pos_casilla_mouse:
		
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO,ALTO_VENTANA-MARCO],
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO+LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO+LADO_CADRO,ALTO_VENTANA-MARCO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO], 
					[ANCHO_VENTANA-MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO+LADO_CADRO], 
					[ANCHO_VENTANA-MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO+LADO_CADRO], 
					GROSOR_LINHA)
			
			if pos_casilla_mouse_anterior:
				
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO,ALTO_VENTANA-MARCO],
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO+LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO+LADO_CADRO,ALTO_VENTANA-MARCO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO, MARCO+pos_casilla_mouse_anterior[1]*LADO_CADRO], 
					[ANCHO_VENTANA-MARCO, MARCO+pos_casilla_mouse_anterior[1]*LADO_CADRO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_CADRICULA, 
					[MARCO, MARCO+pos_casilla_mouse_anterior[1]*LADO_CADRO+LADO_CADRO], 
					[ANCHO_VENTANA-MARCO, MARCO+pos_casilla_mouse_anterior[1]*LADO_CADRO+LADO_CADRO], 
					GROSOR_LINHA)
			

	#ACTUALIZAR VENTANA
	#--------------------------------------------------
	
	if actualizar:
		
		if actualizacion_completa:
			rectangulos_sucios = [pygame.Rect(0,0,ANCHO_VENTANA,ALTO_VENTANA)]
		else:
			rectangulos_sucios = []
			if pos_casilla_mouse:
				rectangulos_sucios.append(pygame.Rect(
						pos_casilla_mouse[0]*LADO_CADRO+MARCO,pos_casilla_mouse[1]*LADO_CADRO+MARCO,LADO_CADRO,LADO_CADRO))
			if pos_casilla_mouse_anterior:
				rectangulos_sucios.append(pygame.Rect(
						pos_casilla_mouse_anterior[0]*LADO_CADRO+MARCO,pos_casilla_mouse_anterior[1]*LADO_CADRO+MARCO,LADO_CADRO,LADO_CADRO))
				
			
		pygame.display.update(rectangulos_sucios)
		
	actualizar = max(actualizar-1,0)
	
	if actualizacion_completa:
		actualizacion_completa = False
		
	##MOUSE
	#--------------------------------------------------
	
	pos_mouse = pygame.mouse.get_pos()
	
	pos_casilla_mouse_anterior = pos_casilla_mouse
	
	#POS CASILLA MOUSE
	
	if pos_mouse[0] > MARCO and pos_mouse[1] > MARCO and pos_mouse[0] < ANCHO_VENTANA-MARCO and pos_mouse[1] < ALTO_VENTANA-MARCO and not fora_pantalla:
		pos_casilla_mouse = [(pos_mouse[0]-MARCO)/LADO_CADRO,(pos_mouse[1]-MARCO)/LADO_CADRO]
	else:
		pos_casilla_mouse = False
		
	if pos_casilla_mouse:
		num_casilla = num(pos_casilla_mouse)
		
	if pos_casilla_mouse and pygame.mouse.get_pressed()[0]:
		lista_casillas[num_casilla].pulsada = 1
		if not (lista_casillas[num_casilla].aberta or lista_casillas[num_casilla].marcada):
			actualizar = MAX_ACTUALIZAR
	elif pos_casilla_mouse:
		lista_casillas[num_casilla].seleccionada = 1
		
	if not pos_casilla_mouse == pos_casilla_mouse_anterior:
		actualizar = MAX_ACTUALIZAR
		
		
	##EVENTOS
	#--------------------------------------------------
	
	for evento in pygame.event.get():
	
		if evento.type == 1 and not inicio:
		
			if evento.state == 1 and evento.gain == 0:
				fora_pantalla = True
			else:
				fora_pantalla = False
		
		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_SPACE:
				for i in lista_casillas:
					i.aberta = 1
					debuxar_casilla(i.num)
				actualizar = 1
				actualizacion_completa = True
			
		if evento.type == pygame.MOUSEBUTTONUP:
			if pos_mouse[0] > MARCO and pos_mouse[1] > MARCO and pos_mouse[0] < ANCHO_VENTANA-MARCO and pos_mouse[1] < ALTO_VENTANA-MARCO:
				
				if evento.button == 1:
					if not lista_casillas[num_casilla].marcada:
						lista_casillas[num_casilla].aberta = 1
						actualizar = MAX_ACTUALIZAR
						debuxar_casilla(num_casilla)
						
				if evento.button == 3:
					if not lista_casillas[num_casilla].marcada:
						lista_casillas[num_casilla].marcada = 1
						actualizar = MAX_ACTUALIZAR
						debuxar_casilla(num_casilla)
					else:
						lista_casillas[num_casilla].marcada = 0
						actualizar = MAX_ACTUALIZAR
						debuxar_casilla(num_casilla)
		
		if evento.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
		
	if inicio:
		inicio = False
			
			
	if not ON:
		break
	
	reloj.tick(FPS)
