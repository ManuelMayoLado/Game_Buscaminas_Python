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
		self.pos = pos
		self.seleccionada = seleccionada
		self.pulsada = pulsada
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

COLOR_TEXTO = [250,250,250]

##VARIABLES

actualizar = 1

pos_casilla_mouse = False

lista_cadros = []

for i in range(NUM_CASILLAS):
								#pos										seleccionada pulsada aberta mina numero
	lista_cadros.append(casilla([i-i/NUM_CADRADOS_FILA*NUM_CADRADOS_FILA,i/NUM_CADRADOS_FILA],0,0,0,0,0,2))

#INICIAR PYGAME

pygame.init()

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

Surface_casillas = pygame.Surface((ANCHO_VENTANA,ALTO_VENTANA))

pygame.display.set_caption("Python Buscaminas")

font = pygame.font.SysFont("System", int(LADO_CADRO*1.2))

ON = True

###################################################################
####BUCLE XOGO
###################################################################

while ON:
	
	reloj = pygame.time.Clock()
	
	##DEBUXAR VENTANA
	#--------------------------------------------------
	
	if actualizar:
		ventana.fill(COLOR_FONDO)
	
		#DEBUXAR CASILLAS
		
	if actualizar:
		
		for i in lista_cadros:
		
			rect_cadro = pygame.Rect(i.pos[0]*LADO_CADRO+MARCO,i.pos[1]*LADO_CADRO+MARCO,LADO_CADRO,LADO_CADRO)
		
			if i.aberta:
				color_cadro = COLOR_FONDO
			elif i.pulsada:
				if i.marcada:
					color_cadro = COLOR_SELECCIONADA
				else:
					color_cadro = COLOR_PULSADA
			elif i.seleccionada:
				color_cadro = COLOR_SELECCIONADA
			else:
				color_cadro = COLOR_CADRO
			pygame.draw.rect(ventana,color_cadro,rect_cadro)
		
			if i.numero and i.aberta:
				text_numero = font.render(str(i.numero),True,COLOR_TEXTO)
				ventana.blit(text_numero,[
									i.pos[0]*LADO_CADRO+MARCO+text_numero.get_width()/1.6,
									i.pos[1]*LADO_CADRO+MARCO+text_numero.get_height()/5.1
									])
		
			if not i.aberta and i.marcada:
				text_numero = font.render("?",True,COLOR_MARCA)
				ventana.blit(text_numero,[
									i.pos[0]*LADO_CADRO+MARCO+text_numero.get_width()/2.,
									i.pos[1]*LADO_CADRO+MARCO+text_numero.get_height()/5.1
									])
			
			if i.seleccionada:
				i.seleccionada = 0
			if i.pulsada:
				i.pulsada = 0				
	
		#PEGAR SURFACE_CASILAS
		
	#ventana.blit(Surface_casillas,(0,0))
	
		#DEBUXAR CADRO_MOUSE
	'''
	if pos_casilla_mouse:
		
		num_casilla = pos_casilla_mouse[0]+pos_casilla_mouse[1]*NUM_CADRADOS_FILA
		
		if lista_cadros[num_casilla].pulsada:
			if lista_cadros[num_casilla].marcada:
				color_cadro = COLOR_SELECCIONADA
			else:
				color_cadro = COLOR_PULSADA
		elif lista_cadros[num_casilla].seleccionada:
			color_cadro = COLOR_SELECCIONADA
				
		rect_cadro = pygame.Rect(lista_cadros[num_casilla].pos[0]*LADO_CADRO+MARCO,lista_cadros[num_casilla].pos[1]*LADO_CADRO+MARCO,LADO_CADRO,LADO_CADRO)	
		pygame.draw.rect(ventana,color_cadro,rect_cadro)
	'''
		#DEBUXAR CADRICULA
	
	for i in range(NUM_CADRADOS_FILA+1):
		pygame.draw.line(ventana, COLOR_FONDO, [MARCO+i*LADO_CADRO, MARCO], [MARCO+i*LADO_CADRO,ALTO_VENTANA-MARCO], GROSOR_LINHA)
		
	for i in range(NUM_FILAS+1):
		pygame.draw.line(ventana, COLOR_FONDO, [MARCO, MARCO+i*LADO_CADRO], [ANCHO_VENTANA-MARCO,MARCO+i*LADO_CADRO], GROSOR_LINHA)
	
	##MOUSE
	#--------------------------------------------------
	
	pos_mouse = pygame.mouse.get_pos()
	
	pos_casilla_mouse_anterior = pos_casilla_mouse
	
	if pos_mouse[0] > MARCO and pos_mouse[1] > MARCO and pos_mouse[0] < ANCHO_VENTANA-MARCO and pos_mouse[1] < ALTO_VENTANA-MARCO:
		pos_casilla_mouse = [(pos_mouse[0]-MARCO)/LADO_CADRO,(pos_mouse[1]-MARCO)/LADO_CADRO]
	else:
		pos_casilla_mouse = False
		
	if pos_casilla_mouse and pygame.mouse.get_pressed()[0]:
		lista_cadros[pos_casilla_mouse[0]+pos_casilla_mouse[1]*NUM_CADRADOS_FILA].pulsada = 1
	elif pos_casilla_mouse:
		lista_cadros[pos_casilla_mouse[0]+pos_casilla_mouse[1]*NUM_CADRADOS_FILA].seleccionada = 1
		
	if not pos_casilla_mouse == pos_casilla_mouse_anterior:
		actualizar = 3
		
	##EVENTOS
	#--------------------------------------------------
	
	for evento in pygame.event.get():
	
		#if evento.type == pygame.KEYDOWN:
			#if evento.key == pygame.K_SPACE:
			
		if evento.type == pygame.MOUSEBUTTONDOWN:
			if evento.button == 1:
				actualizar = 3
			
		if evento.type == pygame.MOUSEBUTTONUP:
			if pos_mouse[0] > MARCO and pos_mouse[1] > MARCO and pos_mouse[0] < ANCHO_VENTANA-MARCO and pos_mouse[1] < ALTO_VENTANA-MARCO:
				num_casilla = pos_casilla_mouse[0]+pos_casilla_mouse[1]*NUM_CADRADOS_FILA
				
				if evento.button == 1:
					if not lista_cadros[num_casilla].marcada:
						lista_cadros[num_casilla].aberta = 1
						actualizar = 3
						
				if evento.button == 3:
					if not lista_cadros[num_casilla].marcada:
						lista_cadros[num_casilla].marcada = 1
						actualizar = 3
					else:
						lista_cadros[num_casilla].marcada = 0
						actualizar = 3
		
		if evento.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
			
			
	if not ON:
		break
		
	#ACTUALIZAR VENTANA
	#--------------------------------------------------
	
	if actualizar:
		pygame.display.update()
		
	actualizar = max(actualizar-1,0)
	
	reloj.tick(FPS)
