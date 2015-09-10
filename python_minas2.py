# -*- coding: utf-8 -*-

import random
import pygame
from pygame.locals import *

import os
import sys
import ctypes

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
    ctypes.windll.user32.SetProcessDPIAware()

##CLASES

class casilla:
	def __init__(self,pos,seleccionada,pulsada,marcada,aberta,mina,numero):
		self.seleccionada = seleccionada
		self.pulsada = pulsada
		self.pos = pos
		self.marcada = marcada
		self.aberta = aberta
		self.mina = mina
		self.numero = numero

##CONSTANTES

MARCO = 5

GROSOR_LINHA = 3

LADO_CADRO = 20

NUM_CADRADOS_FILA = 25
NUM_FILAS = 25

ANCHO_VENTANA = NUM_CADRADOS_FILA * LADO_CADRO + MARCO * 2
ALTO_VENTANA = NUM_FILAS * LADO_CADRO + MARCO * 2

NUM_CASILLAS = NUM_CADRADOS_FILA * NUM_FILAS

FPS = 60

COLOR_FONDO = [90,90,90]
COLOR_CADRO = [230,230,230]
COLOR_SELECCIONADA = [210,210,210]
COLOR_PULSADA = [190,190,190]
COLOR_MARCA = [255,50,50]

COLOR_TEXTO = [200,255,255]

MAX_ACTUALIZAR = 1

##VARIABLES

actualizar = 1

pos_casilla_mouse = False

lista_casillas = []

actualizacion_completa = True

#INICIAR PYGAME

pygame.init()

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

Surface_casillas = pygame.Surface((ANCHO_VENTANA-MARCO*2,ALTO_VENTANA-MARCO*2)).convert()

pygame.display.set_caption("Python Buscaminas")

font = pygame.font.SysFont("System", int(LADO_CADRO*1.2))

ON = True

#FUNCIONS

def num(pos):
	return pos[0]+pos[1]*NUM_CADRADOS_FILA
	
def pos(num):
	return [num % NUM_CADRADOS_FILA, num / NUM_CADRADOS_FILA]

def debuxar_casilla(n):

	posicion = pos(n)
		
	rect_cadro = pygame.Rect(posicion[0]*LADO_CADRO,posicion[1]*LADO_CADRO,LADO_CADRO,LADO_CADRO)
		
	if lista_casillas[n].aberta:
		color_cadro = COLOR_FONDO
	else:
		color_cadro = COLOR_CADRO
		
	pygame.draw.rect(Surface_casillas,color_cadro,rect_cadro)
	
	casilla = lista_casillas[n]
		
	if casilla.numero and casilla.aberta:
		text_numero = font.render(str(casilla.numero),True,COLOR_TEXTO)
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

Surface_casillas.fill(COLOR_CADRO)		

for i in range(NUM_CADRADOS_FILA+1):
	pygame.draw.line(Surface_casillas, COLOR_FONDO, [i*LADO_CADRO, 0], [i*LADO_CADRO,ALTO_VENTANA], GROSOR_LINHA)
		
for i in range(NUM_FILAS+1):
	pygame.draw.line(Surface_casillas, COLOR_FONDO, [0, i*LADO_CADRO], [ANCHO_VENTANA,i*LADO_CADRO], GROSOR_LINHA)

#GENERAR LISTA_CASILLAS

for i in range(NUM_CASILLAS):
								#pos										marcada aberta mina numero
	lista_casillas.append(casilla(pos(i),0,0,0,0,0,2))	

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
				pygame.draw.line(ventana, COLOR_FONDO, [MARCO+i*LADO_CADRO, MARCO], [MARCO+i*LADO_CADRO,ALTO_VENTANA-MARCO], GROSOR_LINHA)
		
			for i in range(NUM_FILAS+1):
				pygame.draw.line(ventana, COLOR_FONDO, [MARCO, MARCO+i*LADO_CADRO], [ANCHO_VENTANA-MARCO,MARCO+i*LADO_CADRO], GROSOR_LINHA)
		
		else:
	
			if pos_casilla_mouse:
		
				pygame.draw.line(ventana, COLOR_FONDO, 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO,ALTO_VENTANA-MARCO],
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_FONDO, 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO+LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse[0]*LADO_CADRO+LADO_CADRO,ALTO_VENTANA-MARCO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_FONDO, 
					[MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO], 
					[ANCHO_VENTANA-MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_FONDO, 
					[MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO+LADO_CADRO], 
					[ANCHO_VENTANA-MARCO, MARCO+pos_casilla_mouse[1]*LADO_CADRO+LADO_CADRO], 
					GROSOR_LINHA)
			
			if pos_casilla_mouse_anterior:
				
				pygame.draw.line(ventana, COLOR_FONDO, 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO,ALTO_VENTANA-MARCO],
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_FONDO, 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO+LADO_CADRO, MARCO], 
					[MARCO+pos_casilla_mouse_anterior[0]*LADO_CADRO+LADO_CADRO,ALTO_VENTANA-MARCO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_FONDO, 
					[MARCO, MARCO+pos_casilla_mouse_anterior[1]*LADO_CADRO], 
					[ANCHO_VENTANA-MARCO, MARCO+pos_casilla_mouse_anterior[1]*LADO_CADRO], 
					GROSOR_LINHA)
				pygame.draw.line(ventana, COLOR_FONDO, 
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
	
	if pos_mouse[0] > MARCO and pos_mouse[1] > MARCO and pos_mouse[0] < ANCHO_VENTANA-MARCO and pos_mouse[1] < ALTO_VENTANA-MARCO:
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
	
		if evento.type == 1:
			if evento.state == 1 and evento.gain == 0:
				pos_casilla_mouse = False
		
		#if evento.type == pygame.KEYDOWN:
			#if evento.key == pygame.K_SPACE:
			
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
			
			
	if not ON:
		break
	
	reloj.tick(FPS)
