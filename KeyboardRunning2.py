import pygame
from defs import *
pygame.init()
pygame.font.init()
pygame.mixer.init()
screen: pygame.Surface = pygame.display.set_mode((1920,1000))
pygame.display.set_caption("きいぼぉどらんにんぐ つー！")
clock: pygame.time.Clock = pygame.time.Clock()
pygame.mixer.music.set_volume(0.3)
nums: NUMs = NUMs(screen)
select_obj: select = select(nums, screen, ["ホーム画面に戻る", "続行"], "Continue", 1)


while nums.main.run:
    screen.fill((0,0,0))
    nums.main.events = pygame.event.get()
    for i in nums.main.events:
        if i.type == pygame.QUIT:
            nums.main.run = False
            continue
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                nums.main.back_page()
            
            elif i.key == pygame.K_F1:
                if nums.main.debug_line:
                    nums.main.debug_line = False
                else:
                    nums.main.debug_line = True

            elif i.key == pygame.K_F2:
                exit()

    if nums.main.menu == "start":     
        pygame.mixer.music.stop()
        for i in nums.main.events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    nums.main.change_page("nani")
                    nums.nani.__init__(nums, screen)
                    nums.sound.play("ok")
            

        blt(ttf("pixel", 15).render("Ver.Tohofes 2027", True, (255,255,255)), screen, (12,8))
        
        blt(ttf("pixel", 100).render("K e y b o a r d - R u n n i n g 2", True, (255,255,255)), screen, (165,255))

        blt(ttf("pixel", 60).render("スペースキーを押してスタート", True, (170, 225, 200)), screen, (580,700))

    elif nums.main.menu == "nani":
        
        if nums.nani.display() == "selected":
            nums.main.change_page("hissa")
            

    elif nums.main.menu == "hissa":
        if nums.hissa.display() == "selected":
            nums.main.change_page("runing")
            pygame.mixer.music.load(pathes("sounds/bgm.mp3"))  # 2. 読み込み（ファイル名は適宜変更）
            pygame.mixer.music.play(-1)


    elif nums.main.menu == "runing":
        nums.runs.built()

    elif nums.main.menu == "result":
        
        blt(ttf("kaisou", 110).render("結  果  発  表", True, (0,255,217)), screen, (710, 50))

        blt(ttf("kaisou", 70).render("POINTS", True, (135, 206, 235)), screen, (200, 215))
        blt(ttf("pixel", 140).render(f"{nums.runs.point}pt", True, (255, 215, 0)), screen, (200, 310))

        blt(ttf("kaisou", 70).render("RUNKS", True, (135, 206, 235)), screen, (200, 550))
        blt(ttf("pixel", 50).render(f"{len(nums.ranks.all_points)}人中", True, (250, 250,250)), screen, (200, 640))
        blt(ttf("pixel", 130).render(f"{nums.ranks.get_rank(nums.runs.point)}位", True, (255, 215,0)), screen, (200, 700))

        blt(ttf("kaisou", 70).render("RUNKINGS", True, (135, 206, 235)), screen, (970, 200))
        rank_x = 280
        for i in nums.ranks.returns():
            blt(ttf("pixel", 80).render(str(i[0]), True, (200,200,200)), screen, (970, rank_x-5))
            blt(ttf("pixel", 70).render(str(i[1]), True, (255,50,50)), screen, (1070, rank_x))
            #blt(ttf("pixel", 70).render(str(i[3]), True, (255,255,255)), screen, (1450, rank_x))
            blt(ttf("pixel", 70).render(str(i[2])+"pt", True, (255,255,255)), screen, (1480, rank_x))
            rank_x += 70

        blt(ttf("pixel", 40).render("Esc:ホーム画面にもどる", True, (230,230,230)), screen, (1250, 20))
    elif nums.main.menu == "continue":
        
        for i in nums.main.events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    if select_obj.get() == "ホーム画面に戻る":
                        nums.__init__(screen)
                    else:
                        nums.main.back_page()
                    select_obj = select(nums, screen, ["ホーム画面に戻る", "続行"], "Continue", 1)
                if i.key == pygame.K_UP:
                    if select_obj.selecting == 0:
                        pass
                    else:
                        select_obj.selecting -= 1
                        nums.sound.play("ok")
                if i.key == pygame.K_DOWN:
                    if len(select_obj.select_list)-1 == select_obj.selecting:
                        pass
                    else:
                        select_obj.selecting += 1
                        nums.sound.play("ok")
        select_obj.display()

    if nums.main.debug_line:
        debug_GUI(screen, nums, clock, interval=50)
    pygame.display.flip()
    clock.tick(nums.main.fps)

pygame.quit()