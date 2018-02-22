import pygame
import sys
import traceback
import myPlane
import shield
import enemy
import supply
import bullet
import os
from random import *
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# 窗口初始化
bg_size = width, height = 426, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("DX.Ssssssss -- 飞机大战Bt")

# 载入图片
background = pygame.image.load("image/bgimage.png").convert()
level2 = pygame.image.load("image/level2.jpg").convert()
level3 = pygame.image.load("image/level3.jpg").convert()
level4 = pygame.image.load("image/level4.jpg").convert()
level5 = pygame.image.load("image/level5.jpg").convert()

# 载入音乐
pygame.mixer.music.load("sound/bg_music.ogg")
pygame.mixer.music.set_volume(0.2)

e3_fly_sound = pygame.mixer.Sound("sound/e3_fly_sound.wav")
pygame.mixer.music.set_volume(0.1)

smallenemydown_sound = pygame.mixer.Sound("sound/smallPlaneDown.wav")
pygame.mixer.music.set_volume(0.1)

midenemydown_sound = pygame.mixer.Sound("sound/middlePlaneDown.wav")
pygame.mixer.music.set_volume(0.1)

bigenemydown_sound = pygame.mixer.Sound("sound/bigPlaneDown.wav")
pygame.mixer.music.set_volume(0.1)

myplanedown_sound = pygame.mixer.Sound("sound/myPlaneDown.wav")
pygame.mixer.music.set_volume(0.1)

getbomb_sound = pygame.mixer.Sound("sound/getBomb.wav")
pygame.mixer.music.set_volume(0.1)

getbullet_sound = pygame.mixer.Sound("sound/getBullet.wav")
pygame.mixer.music.set_volume(0.1)

supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.1)

bullet1_sound = pygame.mixer.Sound("sound/bullet1.wav")
supply_sound.set_volume(0.05)

bullet2_sound = pygame.mixer.Sound("sound/bullet2.wav")
supply_sound.set_volume(0.1)

game_over_sound = pygame.mixer.Sound('sound/gameover.wav')
game_over_sound.set_volume(0.1)
#播放音乐
pygame.mixer.music.play(-1)
# 绘制颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#设置背景索引
bg = 1

# 实例化小型敌机
def add_small_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.SmallEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)


# 实例化中型敌机
def add_mid_enemies(group1, group2, num):
	for i in range(num):
		e2 = enemy.MidEnemy(bg_size)
		group1.add(e2)
		group2.add(e2)


# 实例化大型敌机
def add_big_enemies(group1, group2, num):
	for i in range(num):
		e3 = enemy.BigEnemy(bg_size)
		group1.add(e3)
		group2.add(e3)


# 取消飞机
def del_enemies(group1, group2):
	for i in group1:
		group1.remove(i)
	for j in group2:
		group2.remove(j)

# 增加难度
def inc_speed(target, inc):
	for each in target:
		each.speed += inc


def main():
	global background
	global bg


	clock1 = pygame.time.Clock()
	# 实例化我方飞机
	me = myPlane.Myplane(bg_size)
	# 绘制得分
	score = 0
	best_score = 0
	score_font = pygame.font.Font("font/font.TTF", 32)

	font = pygame.font.Font('font/font.ttf', 36)
	game_over_font = pygame.font.Font('font/font.ttf', 50)

	# 实例化补给包
	bomb_supply = supply.BombSupply(bg_size)
	bullet_supply = supply.SuperbulletSupply(bg_size)
	SUPPLY_TIME = USEREVENT
	pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

	#是否切换速度
	transform = True

	#暂停敌机移动
	is_move = True


	# 实例化子弹
	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4
	for i in range(BULLET1_NUM):
		bullet1.append(bullet.Bullet(me.rect.midtop))

	# 生成超级子弹
	bullet2 = []
	bullet2_index = 0
	BULLET2_NUM = 4
	for i in range(BULLET2_NUM):
		bullet2.append(bullet.SuperBullet(me.rect.midtop))
	#设置能量条
	m = 1000
	mp = m // 20
	# 设置超级子弹定时器
	SUPER_BULLET_TIME = USEREVENT + 1

	# 是否使用超级子弹
	is_super_bullet = False

	# 设置无敌
	INVICIBLE_TIME = USEREVENT + 2

	# 设置分数记录
	recorded = False

	# 难度增加标志
	level = 1
	level_font = pygame.font.Font("font/font.ttf", 32)

	# 设置全屏炸弹
	bomb_image = pygame.image.load("image/bomb.png").convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_font = pygame.font.Font("font/font.ttf", 32)
	bomb_num = 5

	# 所有敌机放到一个组里面，用于判断和我机是否碰撞
	enemies = pygame.sprite.Group()
	# 生成小型敌机
	small_enemies = pygame.sprite.Group()
	add_small_enemies(small_enemies, enemies, 15)
	# 生成中型敌机
	mid_enemies = pygame.sprite.Group()
	add_mid_enemies(mid_enemies, enemies, 5)
	# 生成大型敌机
	big_enemies = pygame.sprite.Group()
	add_big_enemies(big_enemies, enemies, 2)

	# 生成BOSS
	bosses = pygame.sprite.Group()
	boss = enemy.Boss(bg_size)
	enemies.add(boss)
	bosses.add(boss)


	# 飞机毁灭状态索引
	small_plane_destroy = 0
	mid_plane_destroy = 0
	big_plane_destroy = 0
	# boss_plane_destroy = 0
	my_plane_destroy = 0

	# 设置暂停标志
	paused = False

	# 设置我方飞机次数
	life_image = pygame.image.load("image/lifeimage.png").convert_alpha()
	life_rect = life_image.get_rect()
	life_font = pygame.font.Font("font/font.ttf", 32)
	life_num = 5

	# 设置飞机动态效果
	switch_image = True
	# 设置延时参数
	delay = 100
	# 暂停图片
	pause_pressed_image = pygame.image.load("image/pause.png").convert_alpha()
	pause_nor_image = pygame.image.load("image/pause_nor.png").convert_alpha()
	pause_rect = pause_nor_image.get_rect()
	pause_rect.left, pause_rect.top = (width - pause_rect.width) // 2, \
	                                  (height - pause_rect.height) // 2
	pause_image = pause_nor_image
	# 我方飞机无敌效果
	shields = shield.Shield()

	# 游戏结束字体设置
	quit_text = font.render("QUIT", True, WHITE)
	again_text = font.render("Again", True, WHITE)
	quit_pos = quit_text.get_rect()
	again_pos = again_text.get_rect()
	quit_pos.left = width // 3 - quit_pos.width // 2
	quit_pos.top = height // 2 + 150
	again_pos.left = width // 3 * 2 - again_pos.width // 2
	again_pos.top = height // 2 + 150
	#设置背景索引
	bg = 1
	# 设置作弊次数
	fade_time = 1

	# 游戏帧率设置
	clock = pygame.time.Clock()

	# 游戏开始标志
	running = True
	# 设置开头游戏介绍
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
				running = False
		start = pygame.image.load("image/start.png").convert_alpha()
		screen.blit(start, (0, 0))

		pygame.display.flip()
		clock.tick(30)

	# 主程序开始
	key_pressed = pygame.key.get_pressed()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif life_num > 0 and event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					paused = not paused
					if paused:
						pygame.time.set_timer(SUPPLY_TIME, 0)
						# pygame.time.set_timer(SUPER_BULLET_TIME,0)
						pygame.mixer.music.pause()
						pygame.mixer.pause()
					# 绘制暂停按钮
					else:
						pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()

				#screen.blit(pause_image, pause_rect)
			elif event.type == MOUSEMOTION:
				if pause_rect.collidepoint(event.pos):
					pause_image = pause_nor_image
				else:
					pause_image = pause_pressed_image

			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if bomb_num:
						bomb_num -= 1
						for each in enemies:
							if each.rect.bottom > 0:
								boss.energy -= 200
								each.active = False
			if key_pressed[K_x] and key_pressed[K_k] and key_pressed[K_q]:
				if fade_time == 1:
					life_num += 2
					fade_time -= 1
					if life_num > 5:
						life_num = 5


			elif event.type == SUPPLY_TIME:
				supply_sound.play()
				if choice([False, True]):
					bomb_supply.reset()
				else:
					bullet_supply.reset()

			elif event.type == SUPER_BULLET_TIME:
				is_super_bullet = False
				pygame.time.set_timer(SUPER_BULLET_TIME, 0)

			elif event.type == INVICIBLE_TIME:
				me.invicible = False
				pygame.time.set_timer(INVICIBLE_TIME, 0)

			# gameover之后玩家的选择
			elif life_num == 0 and event.type == MOUSEBUTTONDOWN:
				mouse_pos = event.pos
				# 玩家选择退出
				if quit_pos.left < mouse_pos[0] < quit_pos.right and \
								mouse_pos[1] > quit_pos.top and \
								mouse_pos[1] < quit_pos.bottom:
					sys.exit()
				# 玩家选择再玩
				if mouse_pos[0] > again_pos.left and \
								mouse_pos[0] < again_pos.right and \
								mouse_pos[1] > again_pos.top and \
								mouse_pos[1] < again_pos.bottom:
					# 重设背景并播放背景音乐同时关闭gameover音效
					background = pygame.image.load('image/bgimage.png').convert()
					pygame.mixer.stop()
					pygame.mixer.music.play(-1)
					#重设背景图片
					bg = 1
					# 重设分数
					score = 0
					# 重新生成敌机
					enemies = pygame.sprite.Group()

					small_enemies = pygame.sprite.Group()
					add_small_enemies(small_enemies, enemies, 15)

					mid_enemies = pygame.sprite.Group()
					add_mid_enemies(mid_enemies, enemies, 5)

					big_enemies = pygame.sprite.Group()
					add_big_enemies(big_enemies, enemies, 2)
					# 重设全屏炸弹数量及玩家生命数，重设我方飞机
					bomb_num = 5
					life_num = 5
					me.reset()
					pygame.time.set_timer(INVICIBLE_TIME, 3000)
					# 开启补给包，超级子弹判断重设
					pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
					is_supper_bullet = False
					# 重设飞机毁灭恢复参数
					big_plane_destroy = 0
					middle_plane_destroy = 0
					small_plane_destroy = 0
					my_plane_destroy = 0
					# 其他设定
					fade_time = 1
					switch_image = True
					delay = 100
					paused = False
					level = 1
					recorded = False
		#背景音乐图片切换
		if bg == 1:
			screen.blit(background, (0, 0))
		if bg == 2:
			screen.blit(level2, (0, 0))
		if bg == 3:
			screen.blit(level3, (0, 0))
		if bg == 4:
			screen.blit(level4, (0, 0))
		if bg == 5:
			screen.blit(level5, (0, 0))

		if level == 1 and score >= 10000:
			if transform:
				bg = 2
				# 增加3架小飞机，1架中飞机，1架大飞机
				add_small_enemies(small_enemies, enemies, 3)
				add_mid_enemies(mid_enemies, enemies, 2)
				add_big_enemies(big_enemies, enemies, 1)
				#增加小型敌机速度
				inc_speed(small_enemies, 1)
				transform= False
				#去掉所有飞机ddddddd
				is_move = False
				boss.reset()
			if not boss.active:
				#level = 2
				is_move = True

				#复活到原地等待
				boss._return()
				transform = True
				score += 20000
				shield.active = False
				me.invicible = False

		# inc_speed(mid_enemies,1)
		# inc_speed(big_enemies,1)
		elif level == 2 and score >= 200000:
			level = 3
			bg = 3
			# 增加3架小飞机，1架中飞机，1架大飞机
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		# inc_speed(big_enemies,1)
		elif level == 3 and score >= 300000:
			level = 4
			bg = 4
			# 增加3架小飞机，1架中飞机，1架大飞机
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)
			inc_speed(big_enemies, 1)


		elif level == 4 and score >= 400000:
			level = 5
			bg = 5
			# 增加3架小飞机，1架中飞机，1架大飞机
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)
			inc_speed(big_enemies, 1)


		# print(enemies.speed)
		# 绘制BOSS敌机，随机移动

		elif level == 5 and score >= 1000000:
			# 增加3架小飞机，1架中飞机，1架大飞机
			del_enemies(small_enemies, enemies)
			del_enemies(mid_enemies, enemies)
			del_enemies(big_enemies, enemies)

		if life_num > 0 and not paused:
			key_pressed = pygame.key.get_pressed()
			# 设置我方飞机动作
			if key_pressed[K_w] or key_pressed[K_UP]:
				me.moveUp()
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				me.moveDown()
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				me.moveLeft()
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				me.moveRight()

			# 检测飞机是否碰撞
			enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
			if enemies_down and not me.invicible:
				me.active = False
				for e in enemies_down:
					e.active = False


			# 绘制大型敌机
			for each in big_enemies:
				if each.active:
					each.move()
					if switch_image:
						screen.blit(each.image1, each.rect)
					else:
						screen.blit(each.image2, each.rect)
					# 绘制血槽
					pygame.draw.line(screen, BLACK, \
					                 (each.rect.left, each.rect.top - 5), \
					                 (each.rect.right, each.rect.top - 5), \
					                 2)
					energy_remain = each.energy / enemy.BigEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color, \
					                 (each.rect.left, each.rect.top - 5), \
					                 (each.rect.left + each.rect.width * energy_remain, \
					                  each.rect.top - 5), 2)

					if each.rect.bottom >= -50:
						pass
					# e3_fly_sound.play()
				else:
					# 毁灭
					if big_plane_destroy == 0:
						bigenemydown_sound.play()
					screen.blit(each.destroy_image, each.rect)
					big_plane_destroy = (big_plane_destroy + 1) % 2
					if big_plane_destroy == 0:
						each.reset()
						score += 50000
						e3_fly_sound.stop()

			# 绘制中型敌机
			for each in mid_enemies:
				if each.active:

					each.move()
					screen.blit(each.image, each.rect)
					# 绘制血槽
					pygame.draw.line(screen, BLACK, \
					                 (each.rect.left, each.rect.top - 5), \
					                 (each.rect.right, each.rect.top - 5), \
					                 2)
					energy_remain = each.energy / enemy.MidEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color, \
					                 (each.rect.left, each.rect.top - 5), \
					                 (each.rect.left + each.rect.width * energy_remain, \
					                  each.rect.top - 5), 2)
				else:
					if mid_plane_destroy == 0:
						midenemydown_sound.play()
					screen.blit(each.destroy_image, each.rect)
					mid_plane_destroy = (mid_plane_destroy + 1) % 2
					if mid_plane_destroy == 0:
						score += 50000
						each.reset()

			# 绘制小型敌机
			for each in small_enemies:
				if each.active:
					each.move()
					screen.blit(each.image, each.rect)
				else:
					if small_plane_destroy == 0:
						smallenemydown_sound.play()
					screen.blit(each.destroy_image, each.rect)
					small_plane_destroy = (small_plane_destroy + 1) % 2
					if small_plane_destroy == 0:
						score += 1000
						each.reset()

			# 绘制我方飞机
			if me.active:
				if switch_image:
					screen.blit(me.myplane_image1, me.rect)
				else:
					screen.blit(me.myplane_image2, me.rect)
			else:
				# 毁灭
				screen.blit(me.myplane_image1, me.rect)
				if not (delay % 10):
					if my_plane_destroy == 0:
						myplanedown_sound.play()
				screen.blit(me.destroy_image, me.rect)
				my_plane_destroy = (my_plane_destroy + 1) % 4
				if my_plane_destroy == 0:
					life_num -= 1
					if life_num > 0:
						me.reset()
						sheilds.reset()
						if sheilds.active == True:
							sheilds.move((me.rect.left - 26, me.rect.top - 6))
							pygame.time.set_timer(INVICIBLE_TIME, 3 * 1000)



			# 每10帧绘制子弹

			# 绘制全屏炸弹并检测是否获得
			if bomb_supply.active:
				bomb_supply.move()
				screen.blit(bomb_supply.image, bomb_supply.rect)
				if pygame.sprite.collide_mask(bomb_supply, me):
					getbomb_sound.play()
					if bomb_num < 5:
						bomb_num += 1
					bomb_supply.active = False

			# 绘制超级子弹并检测是否获得
			if bullet_supply.active:
				bullet_supply.move()
				screen.blit(bullet_supply.image, bullet_supply.rect)
				if pygame.sprite.collide_mask(bullet_supply, me):
					getbullet_sound.play()
					is_super_bullet = True
					pygame.time.set_timer(SUPER_BULLET_TIME, 18 * 1000)
					bullet_supply.active = False

			if is_super_bullet:
				if not (delay % 10):
					bullets = bullet2
					bullets[bullet2_index].reset(me.rect.midtop)
					bullet2_sound.play()
					bullet2_index = (bullet2_index + 1) % BULLET2_NUM
			else:
				if not (delay % 10):
					bullets = bullet1
					bullet1[bullet1_index].reset(me.rect.midtop)
					bullet1_sound.play()
					bullet1_index = (bullet1_index + 1) % BULLET1_NUM

			# 检测子弹击中目标
			for b in bullets:
				if b.active:
					b.move()
					screen.blit(b.image, b.rect)
					enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
					# boss_bullet_hit = pygame.sprite.spritecollide(boss,b,False)
					if enemy_hit:
						b.active = False
						for e in enemy_hit:
							if e in mid_enemies or e in big_enemies:
								e.energy -= (2 if is_super_bullet else 1)
								if e.energy == 0:
									e.active = False
							else:
								e.active = False
			if bosses:
				for each in bosses:
					if each.active:
						each.move()
						if each.hit:
							screen.blit(each.image_hit, each.rect)
							each.hit = False
						else:
							screen.blit(each.image, each.rect)
						# 绘制血槽
						pygame.draw.line(screen, BLACK, \
						                 (each.rect.left, each.rect.top + 4), \
						                 (each.rect.right, each.rect.top + 4))
						# 当生命大于20%显示绿色，否则显示红色
						energy_remain = each.energy / enemy.Boss.energy
						if energy_remain > 0.2:
							energy_color = GREEN
						else:
							energy_color = RED
						pygame.draw.line(screen, energy_color, \
						                 (each.rect.left, each.rect.top + 4), \
						                 (each.rect.left + each.rect.width * energy_remain, \
						                  each.rect.top + 4), 4)
					else:
						if not transform:
							position = each.rect.center
							# # 原地生成一个随机奖励
							# if not choice(range(lv_dict[5])):
							# 	prize_bomb = supply.Bomb1(size, position)
							# 	_prize_bomb.add(prize_bomb)
							#
							# if not choice(range(lv_dict[5])):
							# 	prize_life = _plane.Life(size, position)
							# 	_prize_life.add(prize_life)
							#
							# _delay = 0
			if not is_move:
				for each in enemies:
					if each not in bosses:
						each.reset()


		elif paused:
			# 绘制暂停按钮
			screen.blit(pause_image, pause_rect)

		if life_num > 0:
			# 绘制全屏炸弹
			bomb_text = bomb_font.render("X %d " % bomb_num, True, GREEN)
			text1_rect = bomb_text.get_rect()
			screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
			screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text1_rect.height))

			# 显示次数
			"""life_text = life_font.render("X %d" % life_num,True,GREEN)
            text2_rect = life_text.get_rect()
            screen.blit(life_image,(250,height - 10 - life_rect.height))
            screen.blit(life_text,(250 + life_rect.width,height - 5 - text2_rect.height))
           """
			if life_num:
				for i in range(life_num):
					screen.blit(life_image, \
					            (width - 10 - (i + 1) * life_rect.width, \
					             height - 10 - life_rect.height))

			# 显示关卡等级
			level_text = level_font.render("level = %d " % level, True, GREEN)
			text2_rect = level_text.get_rect()
			screen.blit(level_text, (10, 30))

			# 显示得分
			score_text = score_font.render("Score: %s" % str(score), True, GREEN)
			screen.blit(score_text, (10, 5))
		elif life_num == 0:
			# 绘制游戏结束界面
			game_over = game_over_font.render("GAME OVER", True, WHITE)
			screen.blit(game_over, ((width - game_over.get_width()) // 2, \
			                        (height - game_over.get_height()) // 2))
			pygame.mixer.music.stop()
			pygame.time.set_timer(SUPPLY_TIME, 0)
			# 记录历史最高得分
			if not recorded:
				with open("record.data", "r") as f:
					temp = f.read()
					if temp != "":
						best_score = int(temp)
					if best_score < score:
						best_score = score
						with open("record.data", "w") as f:
							f.write(str(best_score))
					recorded = True
					pygame.mixer.stop()
					game_over_sound.play()
					background = pygame.image.load('image/gameover.png').convert()

			# 绘制分数，最高分和当前分数
			best_score_text = font.render('Best Score: %s' % str(best_score), True, WHITE)
			screen.blit(best_score_text, (40, 50))
			your_score_text = font.render('Your Score: %s' % str(score), True, WHITE)
			screen.blit(score_text, ((width - your_score_text.get_width()) // 2 + 50, \
			                         (height + game_over.get_height()) // 2 - 150))

			# 绘制选择项
			screen.blit(quit_text, quit_pos)
			screen.blit(again_text, again_pos)
			mouse_pos = pygame.mouse.get_pos()
			# 退出Quit
			if mouse_pos[0] > quit_pos.left and mouse_pos[0] < quit_pos.right and \
							mouse_pos[1] > quit_pos.top and mouse_pos[1] < quit_pos.bottom:
				quit_text = font.render("Quit", True, RED)
			else:
				quit_text = font.render("Quit", True, WHITE)

			# 重新Again
			if mouse_pos[0] > again_pos.left and mouse_pos[0] < again_pos.right and \
							mouse_pos[1] > again_pos.top and mouse_pos[1] < again_pos.bottom:
				again_text = font.render("Again", True, GREEN)
			else:
				again_text = font.render("Again", True, WHITE)

		if not (delay % 5):
			switch_image = not switch_image
		delay -= 1
		if not delay:
			delay == 100

		pygame.display.flip()
		clock.tick(60)


if __name__ == "__main__":
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()
