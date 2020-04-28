import random
import time
import pygame as pg
from pygame.locals import *
import sys
from math import sin, cos, pi
from wuziqi import Wuziqi


          
def main():
    pg.init()
    size = 16
    line_color = (122, 122, 122)
    bg_color = (239, 228, 176)
    screen = pg.display.set_mode((size* 30, size* 30 + 40))
    pg.display.set_caption("五子棋 - by Rose")

    # 载入字体
    font_num = pg.font.SysFont('Times', 10)
    font = pg.font.SysFont('colonna', size*3)

    # 载入音效
    win_sound = pg.mixer.Sound("music/win.wav")
    win_sound.set_volume(0.1)
    lose_sound = pg.mixer.Sound("music/lose.wav")
    lose_sound.set_volume(0.1)
    white_sound = pg.mixer.Sound("music/white.wav")
    white_sound.set_volume(0.1)
    black_sound = pg.mixer.Sound("music/black.wav")
    black_sound.set_volume(0.1)
    
    # 载入图片
    white_chess = pg.image.load("image/white_chess.png").convert_alpha()
    black_chess = pg.image.load("image/black_chess.png").convert_alpha()
    last_white_chess = pg.image.load("image/last_white_chess.png").convert_alpha()
    none_chess = pg.image.load("image/none_chess.png").convert_alpha()
    start_again_image = start_again_notpress_image = pg.image.load("image/start_again_notpress.png").convert_alpha()
    start_again_press_image = pg.image.load("image/start_again_press.png").convert_alpha()
    last_step_image = last_step_notpress_image = pg.image.load("image/last_step_notpress.png").convert_alpha()
    last_step_press_image = pg.image.load("image/last_step_press.png").convert_alpha()

    start_again_image_rect = start_again_image.get_rect()
    last_step_image_rect = last_step_image.get_rect()
    start_again_image_rect.left, start_again_image_rect.top = (size*15, size*30 -5)
    last_step_image_rect.left, last_step_image_rect.top = (size*4, size*30 -5)

    me_first = me_first_not_press = font.render("> Me First_Move" ,True, (0, 0, 255))
    me_first_press = font.render("> Me First_Move" ,True, (255, 0, 0))
    ai_first = ai_first_not_press = font.render("> AI First_Move" ,True, (0, 0, 255))
    ai_first_press = font.render("> AI First_Move" ,True, (255, 0, 0))
    me_first_rect = me_first.get_rect()
    ai_first_rect = ai_first.get_rect()
    me_first_rect.left, me_first_rect.top = (size*4, size*12)
    ai_first_rect.left, ai_first_rect.top = (size*4, size*16) 

            
    clock = pg.time.Clock()
    wuziqi = Wuziqi(size)
    game_over = True
    ai_move = False
    start = True

    screen.fill(bg_color)
    for i in range(size):
        pg.draw.line(screen, line_color, (14, i * 30 + 14), (size*30 - 16, i * 30 + 14), 2)
        pg.draw.line(screen, line_color, (i * 30 + 14, 14), (i * 30 + 14, size*30 - 16), 2)

    while True:
        if start:
            screen.fill((239, 228, 176))
            for i in range(size):
                pg.draw.line(screen, line_color, (14, i * 30 + 14), (size*30 - 16, i * 30 + 14), 2)
                pg.draw.line(screen, line_color, (i * 30 + 14, 14), (i * 30 + 14, size*30 - 16), 2)
            screen.blit(me_first, (me_first_rect.left, me_first_rect.top))
            screen.blit(ai_first, (ai_first_rect.left, ai_first_rect.top))
            
        for event in pg.event.get():  
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                if start_again_image_rect.collidepoint(event.pos):
                    start_again_image = start_again_press_image
                else:
                    start_again_image = start_again_notpress_image
                if last_step_image_rect.collidepoint(event.pos):
                    last_step_image = last_step_press_image 
                else:
                    last_step_image = last_step_notpress_image
                    
                if me_first_rect.collidepoint(event.pos):
                    me_first = me_first_press
                else:
                    me_first = me_first_not_press
                if ai_first_rect.collidepoint(event.pos):
                    ai_first = ai_first_press
                else:
                    ai_first = ai_first_not_press

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                   # 重新开始游戏
                    if start_again_image_rect.collidepoint(event.pos):        
                        start = True
                        game_over = True
                    
                    # 玩家下子
                    if not game_over:                   
                        r = event.pos[1] // 30
                        c = event.pos[0] // 30
                        if r < size:
                            if wuziqi.list_qi[r][c] == 0:
                                black_sound.play()
                                time.sleep(0.2)
                                screen.blit(black_chess, (c*30+3, r*30+3))
                                last_point_player.append((r, c))
                                pg.display.flip() 
                                wuziqi.list_qi[r][c] = 1
                                ai_move = True
                                
                        # 悔棋操作
                        else:
                            if last_step_image_rect.collidepoint(event.pos) and last_point_player:
                                player = last_point_player.pop()
                                ai = last_point_ai.pop()
                                wuziqi.list_qi[player[0]][player[1]] = 0
                                wuziqi.list_qi[ai[0]][ai[1]] = 0
                                screen.blit(none_chess, (ai[1]*30+3, ai[0]*30+3))
                                if last_point_ai:
                                    screen.blit(last_white_chess, (last_point_ai[-1][1]*30+3, last_point_ai[-1][0]*30+3))
                                pg.display.flip()
                                time.sleep(0.5)
                                screen.blit(none_chess, (player[1]*30+3, player[0]*30+3))
                                pg.display.flip()
                                               
                    if start:
                        # 选择谁先手
                        if me_first_rect.collidepoint(event.pos):
                            start = False
                            game_over = False
                            wuziqi.reset()
                            last_point_player = []
                            last_point_ai = []
                            screen.fill((239, 228, 176))               
                            for i in range(size):
                                row = font_num.render(str(i), True, (0, 0, 0))
                                screen.blit(row , (2, i*30 + 10))
                                screen.blit(row , (i*30 + 10, 2))
                                pg.draw.line(screen, line_color, (14, i * 30 + 14), (size*30 - 16, i * 30 + 14), 2)
                                pg.draw.line(screen, line_color, (i * 30 + 14, 14), (i * 30 + 14, size*30 - 16), 2)
                            
                        if ai_first_rect.collidepoint(event.pos):
                            start = False
                            game_over = False
                            wuziqi.reset()
                            last_point_player = []
                            last_point_ai = []
                            screen.fill((239, 228, 176))               
                            for i in range(size):
                                row = font_num.render(str(i), True, (0, 0, 0))
                                screen.blit(row , (2, i*30 + 10))
                                screen.blit(row , (i*30 + 10, 2))
                                pg.draw.line(screen, line_color, (14, i * 30 + 14), (size*30 - 16, i * 30 + 14), 2)
                                pg.draw.line(screen, line_color, (i * 30 + 14, 14), (i * 30 + 14, size*30 - 16), 2)
                            wuziqi.list_qi[size//2 - 1][size//2 - 1] = 2
                            screen.blit(last_white_chess, ((size//2 - 1)*30+3,(size//2 - 1)*30+3))
                            last_point_ai.append((size//2 - 1,size//2 - 1))                   
                        
        if ai_move and not game_over:
            ai_move = False   
            wuziqi.check_fivepots()
            # 判定黑棋是否五子连线
            if wuziqi.max_value == -1 :
                game_over = True
                win_sound.play()  
                win1 = font.render("Congratulation !" ,True, (255, 0, 0))
                win2 = font.render("You Win !" ,True, (255, 0, 0))
                screen.blit(win1, (70, 70))
                screen.blit(win2, (130, 130))            
            else:
                # AI下子，并判定白棋是否五子连线
                time.sleep(0.8)
                wuziqi.get_value()
                if last_point_ai:
                    screen.blit(white_chess, (last_point_ai[-1][1]*30+3, last_point_ai[-1][0]*30+3))
                screen.blit(last_white_chess, (wuziqi.next_point[1]*30+3, wuziqi.next_point[0]*30+3))
                last_point_ai.append((wuziqi.next_point[0], wuziqi.next_point[1]))
                white_sound.play() 
                wuziqi.check_fivepots()
                if wuziqi.max_value == -1:
                    game_over = True
                    lose_sound.play() 
                    lose = font.render("AI Win !" ,True, (255, 0, 0))
                    screen.blit(lose, (140, 130))
        screen.blit(last_step_image, (last_step_image_rect.left, last_step_image_rect.top))
        screen.blit(start_again_image, (start_again_image_rect.left, start_again_image_rect.top))
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

                    

     
