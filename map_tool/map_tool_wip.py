"""
    The map editor for pyr_pg(this is included in the pyr_pg package folder)
    Copyright (C) 2024 Spyro24

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pygame as p
from text import text_field as inp
import pywin as pw
import time
import map_ as prm
import tiles
from time import sleep

mapt_w_h, mapt_w_w = 600, 600  # the size of the window
mapt_win = p.display.set_mode((mapt_w_w, mapt_w_h))
mapt_run = True #run the map tool
mapt_mode = "EDIT" #maptool mode
mapt_lock = False #lock the loop in to the mode
mapt_w_update = False
mapt_if_red = False
tile_map_int = []
tile_map = []
tile_list = tiles.load_tile_list()
tile_png_list = tiles.load_images_from_lst("../tiles", tile_list)
tile_s_page = 0
tile_sel = 0
tile_cur = 0 #curent tile
text_size = 20
edit_layer = 0
symbols_raw = ["close", "arrow_left", "arrow_right", "null"]
symbols_load = pw.load_iconset("./symbols/task",symbols_raw)
tile_display = True
map_edges = []
map_tile_bytes = 2 #the tile len in bytes (Default: 2)
map_x = 0
map_y = 0
map_w = 16
map_h = 16
map_draw = False
map_cur = prm.map_load(map_x,map_y, map_w, map_h, map_tile_bytes)
map_load = False
map_e_mode = None
tile_size = int(((mapt_w_h / 10) * 8) / 18)
print(tile_size)

while mapt_run:
    if mapt_mode == "EDIT":
        mapt_lock = True
        mapt_if_red = True
        mapt_win.fill((0,0,0))
        while mapt_lock:
            
            if mapt_if_red: #draw the interface
                pw.draw_rect(mapt_win, (mapt_w_h / 10) * 8, 0, mapt_w_h / 10 * 2, mapt_w_w / 10 , (125,125,125))
                pw.draw_font(mapt_win, text_size, (mapt_w_h / 10) * 8 + (mapt_w_h / 40), mapt_w_h / 40, "Tile", (0,0,0))
                pw.blit_icon(mapt_win, (mapt_w_h / 10) * 8, (mapt_w_w/ 10) * 1, symbols_load[1], (mapt_w_h / 10))
                pw.blit_icon(mapt_win, (mapt_w_h / 10) * 9, (mapt_w_w/ 10) * 1, symbols_load[2], (mapt_w_h / 10))
                tile_display = True
                mapt_w_update = True
                mapt_if_red = False
                map_draw = True
                
            if map_load:
                map_cur = prm.map_load(map_x,map_y, map_w, map_h, map_tile_bytes)
                map_load = False
                map_draw = True
                
            if map_draw:
                pw.draw_rect(mapt_win,0,0,(mapt_w_h / 10) * 8, (mapt_w_h / 10) *8, (0,0,0))
                prm.draw_map(mapt_win, ((mapt_w_h / 20),(mapt_w_h / 20)), ((mapt_w_h / 10) * 8) / 18, map_cur[0], (map_w, map_h))
                if map_e_mode == "ov":
                    prm.draw_map(mapt_win, ((mapt_w_h / 20),(mapt_w_h / 20)), ((mapt_w_h / 10) * 8) / 18, map_cur[0], (map_w, map_h))
                prm.map_border_blit(mapt_win,map_w, map_h, ((mapt_w_h / 20),(mapt_w_h / 20)),tile_size, prm.map_border(map_x, map_y,map_w,map_h,map_tile_bytes))
                mapt_w_update = True
                map_draw = False
                
            if tile_display:
                if tile_cur > 0:
                    pw.blit_icon(mapt_win, (mapt_w_h / 10) * 9, 0, tile_png_list[edit_layer][tile_cur-1], (mapt_w_h / 10))
                else:
                    pw.blit_icon(mapt_win, (mapt_w_h / 10) * 9, 0, symbols_load[3], (mapt_w_h / 10))
                mapt_w_update = True
                tile_display = False
                
            if mapt_w_update:
                p.display.update()
                mapt_w_update = False
            
            for event in p.event.get():
                if event.type == p.QUIT:
                    mapt_lock = False
                    mapt_mode = None
                    mapt_run = False
                
            if pw.p_push_button((mapt_w_h / 10) * 8, 0, mapt_w_h / 10 * 2, mapt_w_w):
                if pw.p_push_button((mapt_w_h / 10) * 8, 0, mapt_w_h / 10 * 2, mapt_w_w / 10): #open the tile selector
                    mapt_mode = "TILE_SELECT"
                    mapt_lock = False
                    
                elif pw.p_push_button((mapt_w_w / 10) * 9, (mapt_w_h / 10) * 1, mapt_w_w / 10 , mapt_w_h / 10): #left arrow button
                    tile_cur -= 1
                    tile_display = True
                    sleep(0.1)
                        
                elif pw.p_push_button((mapt_w_w / 10) * 8, (mapt_w_h / 10) * 1, mapt_w_w / 10 , mapt_w_h / 10): #Right arrow button
                    tile_cur += 1
                    tile_display = True
                    sleep(0.1)
            
            if pw.p_push_button(0,0,(mapt_w_h / 10) * 8,(mapt_w_h / 10) * 8): #MapInteraction
                if pw.p_push_button((mapt_w_h / 20),(mapt_w_h / 20) - tile_size,(mapt_w_h / 20) + tile_size* map_w,(mapt_w_h / 20)): #Go one map up
                    map_y -= 1
                    map_load = True
                    map_draw = True
                    
                if pw.p_push_button((mapt_w_h / 20),(mapt_w_h / 20) + (tile_size * (map_h)),(mapt_w_h / 20) + tile_size * map_w,(mapt_w_h / 20)):
                    map_y += 1
                    map_load = True
                    map_draw = True
            
                
    if mapt_mode == "TILE_SELECT":
        mapt_lock = True
        mapt_if_red = True
        mapt_win.fill((0,0,0))
        sleep(0.1)
        while mapt_lock:
            
            if mapt_if_red:
                mapt_win.fill((0,0,0))
                pw.icon_grid(mapt_win, 0, 0, mapt_w_w / 10, 10, 9, tile_png_list, tile_s_page, edit_layer)
                pw.blit_icon(mapt_win, (mapt_w_h / 10) * 8, (mapt_w_w/ 10) * 9, symbols_load[0], (mapt_w_h / 10))
                pw.blit_icon(mapt_win, (mapt_w_h / 10) * 1, (mapt_w_w/ 10) * 9, symbols_load[1], (mapt_w_h / 10))
                pw.blit_icon(mapt_win, (mapt_w_h / 10) * 3, (mapt_w_w/ 10) * 9, symbols_load[2], (mapt_w_h / 10))
                if tile_cur > 0:
                    pw.blit_icon(mapt_win, (mapt_w_h / 10) * 2, (mapt_w_w/ 10) * 9, tile_png_list[edit_layer][tile_cur-1], (mapt_w_h / 10))
                else:
                    pw.blit_icon(mapt_win, (mapt_w_h / 10) * 2, (mapt_w_w/ 10) * 9, symbols_load[3], (mapt_w_h / 10))
                mapt_if_red = False
                mapt_w_update = True
                
            if mapt_w_update:
                p.display.update()
                mapt_w_update = False
                
            for event in p.event.get():
                if event.type == p.QUIT:
                    mapt_lock = False
                    mapt_mode = None
                    mapt_run = False
                    
            if pw.p_push_button((mapt_w_h / 10), (mapt_w_w/ 10) * 9, mapt_w_h / 10 * 8, mapt_w_w / 10):
                if pw.p_push_button((mapt_w_w / 10) * 8, (mapt_w_h / 10) * 9, mapt_w_w / 10 , mapt_w_h / 10): #exit the tile selector
                    mapt_mode = "EDIT"
                    mapt_lock = False
                    
                if pw.p_push_button((mapt_w_w / 10), (mapt_w_h / 10) * 9, mapt_w_w / 10 , mapt_w_h / 10): #left arrow button
                    if tile_s_page > 0:
                        tile_s_page -= 1
                        mapt_if_red = True
                        sleep(0.1)
                        
                if pw.p_push_button((mapt_w_w / 10) * 3, (mapt_w_h / 10) * 9, mapt_w_w / 10 , mapt_w_h / 10): #Right arrow button
                    if tile_s_page < 729:
                        tile_s_page += 1
                        mapt_if_red = True
                        sleep(0.1)
                        
                
                    
            if pw.p_push_button(0, 0, mapt_w_h, mapt_w_w / 10 * 9):
                void, set_tile = pw.button_grid(0,0,(mapt_w_h / 10),10,9)
                if set_tile != None:
                    tile_cur = set_tile + 1
                    if tile_cur > len(tile_png_list[edit_layer]):
                        tile_cur = len(tile_png_list[edit_layer])
                    pw.blit_icon(mapt_win, (mapt_w_h / 10) * 2, (mapt_w_w/ 10) * 9, tile_png_list[edit_layer][tile_cur-1], (mapt_w_h / 10))
                    mapt_w_update = True
                
                
            

p.quit()