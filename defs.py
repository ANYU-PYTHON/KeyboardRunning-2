import pygame
import time
from datetime import datetime
import threading
import pickle
import functools

@functools.cache
def ttf(ttf, size, mode=None):
    """
    ttf の Docstring
    
    :ttf: 必須 フォント名(kaisou➔kaisoutai.ttf, pixel➔PixelMplus10-Regular.ttf, bis➔BIZUDGothic-Regular.ttf)
    :size: 必須 フォントのサイズ
    :mode: 任意 sys➔SysFontの使用
    """
    import pygame as pg
    pg.init()

    ttfn: str = "ttfs/"
    if ttf=="kaisou":
        ttfn+="kaisoutai.ttf"
    elif ttf=="pixel":
        ttfn+="PixelMplus10-Regular.ttf"
    elif ttf == "ipa":
        ttfn += "ipagp.ttf"
    elif ttf == "bis":
        ttfn+="BIZUDGothic-Regular.ttf"
    ttfs: pg.font.Font = pg.font.Font(ttfn, size) 
    return ttfs


def CEN(text: str, size: float, msize_x=1920, msize_y=1080, mode="None", font=None):
    """
    text-テキスト
    size-大きさ
    msize-x-モニターの大きさ(x)
    msize-y-モニターの大きさ(y)
    mode-デフォで中心に来る座標、"HOW?"でそれのX_Yの大きさ
    """
    if mode == "None":
        x_y = ttf("kaisou", size).size(text)
        X=(msize_x-x_y[0])/2
        Y=(msize_y-x_y[1])/2
        return [X,Y]
    if mode == "img":
        X=(msize_x-text[0])/2
        Y=(msize_y-text[1])/2
        return [X,Y]
    elif mode == "()":
        x_y = ttf("pixel", size).size(text)
        X=(msize_x-x_y[0])/2
        Y=(msize_y-x_y[1])/2
        return (X,Y)
    elif mode == "HOW?":
        if font == "ipa":
            x_y = ttf("ipa", size).size(text)
        elif font is not None:
            x_y = ttf(font, size).size(text)
        else:
            x_y = ttf("pixel", size).size(text)
        return x_y





def blt(obj: pygame.Surface, screen: pygame.Surface, XY):
    """
    obj-描画するオブジェクト
    screen-描画先のスクリーン
    """
    screen.blit(obj, XY)





class NUMs:
    """
    Class main
    ---
    display_size(tuple) : (1920,1000)
    menu(str) : "start"
    back_menu(list) : ["start"]
    run(bool) : True
    fps(int) : 60
    debug_line(bool) : False
    
    Class nani
    ---
    select(str) : None
    """
    def __init__(self, screen: pygame.Surface):
        self.main: MAIN = MAIN(self, screen)
        self.nani: NANI = NANI(self, screen)
        self.hissa: HISSA = HISSA(self, screen)
        self.runs: RUNS = RUNS(self, screen)
        self.sound: SOUNDS = SOUNDS()
        self.ranks: ranking = ranking()

class MAIN:
    """
        Class main
        ---
        **display_size**(tuple) : (1920,1000)
        **menu**(str) : "start"
        **back_menu**(list) : ["start"]
        **run**(bool) : True
        **fps**(int) : 60
        **debug_line**(bool) : False

        ### defs
        **change_page**:<br>
            ページ遷移を簡単に実現します。<br>
            また、戻るページがわかるよう、back_menuを更新します。

        **back_page**:<br>
            ページバックを簡単に実現します。<br>
            また、back_menuが空の場合は、ホーム画面に移動します。
    """
    def __init__(self, num: NUMs, screen: pygame.Surface):
        self.display_size: tuple = (1920,1000)
        self.menu: str  = "start"
        self.events: list[pygame.event.Event] = []
        self.screen: pygame.Surface = screen
        self.num: NUMs = num
        self.menu_list: list[str] = ["start", "nani", "hissa", "runing"]
        self.run: bool = True
        self.fps: int = 60                                       # 意図しない速さ変更の可能性あり
        self.debug_line: bool = False
        self.nani: str = None
        self.hissa: str = None
        

    def change_page(self, New_page: str):
        """
        **New_page** : Str
            移動する先の新しい画面。
        """
        if New_page == "runing":
            countdown(self.screen, self.num)
            self.num.runs.__init__(self.num, self.screen)
            self.num.runs.start = time.time()
        

        self.menu = New_page



    def back_page(self):
        if self.menu == "start":
            return
        elif self.menu == "runing":
            self.menu = "continue"
            pygame.mixer.music.pause()
            return
        elif self.menu == "nani":
            self.num.__init__(self.screen)
        elif self.menu == "continue":
            self.menu = "runing"
            pygame.mixer.music.unpause()
            return
        elif self.menu == "result":
            pygame.mixer.music.stop()
            self.num.__init__(self.screen)
            return
        if self.menu not in self.menu_list:
            self.num.__init__(self.screen)
            return
        for i in range(len(self.menu_list)):
            if self.menu == self.menu_list[i]:
                self.menu = self.menu_list[i-1]
                return

class SOUNDS:
    from typing import Literal
    def __init__(self):
        self.sounds = {
            "bad": pygame.mixer.Sound("sounds/BAD.mp3"),
            "end": pygame.mixer.Sound("sounds/END.mp3"),
            "oks": pygame.mixer.Sound("sounds/OK.mp3"),
            "ok": pygame.mixer.Sound("sounds/PI.mp3"),
            "start": pygame.mixer.Sound("sounds/start.mp3"),
            "pon": pygame.mixer.Sound("sounds/timing.mp3"),
            "bom": pygame.mixer.Sound("sounds/bomb.mp3"),
            "don": pygame.mixer.Sound("sounds/DON.mp3"),
            "slow": pygame.mixer.Sound("sounds/SLOW.mp3"),
            "pun": pygame.mixer.Sound("sounds/PUN.mp3")
        }

    def play(self, sound: Literal["bad", "end", "oks", "ok", "start", "pon", "bom", "don", "slow", "pun"]):
        self.sounds[sound].play()

def countdown(screen: pygame.Surface, num: NUMs):
    time1 = time.time() +0.5
    playd: list[str] = []
    redy = True
    start_text = ""

    
    while redy:
        text_time = ttf("pixel", 150).render(start_text, True, (135, 206, 235))
        screen.fill((0,0,0))
        xy = CEN(start_text, 150, 1910, 1050)
        blt(text_time, screen, xy)

        if 2 < time.time() - time1 >= 1:
            start_text = "3"
            if start_text in playd:
                pass
            else:
                playd.append(start_text)
                num.sound.play("pon")

        if 3 < time.time() - time1 >= 2:
            start_text = "2"
            if start_text in playd:
                pass
            else:
                playd.append(start_text)
                num.sound.play("pon")

        if 4 < time.time() - time1 >= 3:
            start_text = "Ready?"
            if start_text in playd:
                pass
            else:
                playd.append(start_text)
                num.sound.play("pon")

        if 5 < time.time() - time1 >= 4:
            start_text = "Go!"
            if start_text in playd:
                pass
            else:
                playd.append(start_text)
                num.sound.play("start")

        if time.time() - time1 > 5.4:
            playd = []
            redy = False

        pygame.display.flip()

def CEN1(text, size, screen_width, screen_height):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255,255,255))
    rect = text_surface.get_rect(center=(screen_width//2, screen_height//2))
    return rect.topleft

def end(screen: pygame.Surface, nums: NUMs, types: str):
    """
    **types**: str, "over" or "fin"
    """
    
    if types == "over":
        end_text = "Game Over"
        end_color = (250,0,0)
    elif types == "fin":
        end_text = "Finish"
        end_color = (135, 206, 235)
    text_obj = ttf("pixel", 150).render(end_text, True, end_color).convert_alpha()

    run = True
    clock1 = pygame.time.Clock()
    
    num = 0
    alp = 255
    nums.sound.play("end")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                Scre = False
                    

                # アルファフェード処理
        if num >= 60:
            alp -= 3
            if alp < 0:
                alp = 0
            if alp == 0:
                run = False
            text_obj.set_alpha(alp)

        # 描画
        screen.fill((0,0,0))
        screen.blit(text_obj, CEN1(end_text, 150, 1920, 1080))
        pygame.display.flip()

        num += 1
        clock1.tick(70)



class select:
    
    def __init__(self, num:NUMs, screens: pygame.Surface, lists: list[str], title: str, initable_value: int, ok_txt: str = "決定"):
        self.screen_object: pygame.Surface = screens
        self.nums: NUMs = num
        self.title: str = title
        self.select_list: list[str] = lists
        self.select_list_ttf: dict[str,pygame.Surface] = {}
        self.select_list_xy: dict[str,tuple[int, int]] = {}
        self.selecting: int = initable_value
        self.color: dict = {"select": (229, 215, 79), "other": (190,190,190)}
        self.ok_text: str = ok_txt

    def display(self):
        all_y = 0
        for i in self.select_list:
            all_y += 170
        all_y -= 90
        title_obj = ttf("kaisou", 110).render(self.title, True, (0,255,217))
        title_x = (self.nums.main.display_size[0] - title_obj.get_size()[0])/2
        point_y = int((self.nums.main.display_size[1] - 120 - all_y)/2 + 110) #始点
        title_y = point_y/3                                                      # タイトル距離変更はここ
        blt(title_obj, self.screen_object, (title_x, title_y))
        
        # レンダリング定義
        for i in self.select_list:
            
            self.select_list_ttf[i] = ttf("pixel", 80).render(i, True, self.color["other"])
            if self.select_list[self.selecting] == i:
                # 現在選択中
                self.select_list_ttf[i] = ttf("pixel", 80).render(i, True, self.color["select"])
                # ここでpolygon を描画、その他はこの後まとめて [(710,350), (660,320), (660,380)]
                
        
        if self.select_list_xy == {}:
            for i in self.select_list:
                self.select_list_xy[i] = ((self.nums.main.display_size[0]-self.select_list_ttf[i].get_size()[0])/2 , point_y)
                point_y += 170
        else:
            pass
        for i in self.select_list:
            if self.select_list[self.selecting] == i:#                   右中央     左上        左下
                #                                   文字との間隔                  フォントサイズ/2
                por_point_light_c = (self.select_list_xy[i][0]-20, self.select_list_xy[i][1]+40)
                por_point_left_up = (self.select_list_xy[i][0]-70, self.select_list_xy[i][1]+10)
                por_point_left_down = (self.select_list_xy[i][0]-70, self.select_list_xy[i][1]+70)
                pygame.draw.polygon(self.screen_object, (255, 255, 0), [por_point_light_c, por_point_left_up, por_point_left_down])
                font_iti_light = self.select_list_ttf[i].get_size()[0]+self.select_list_xy[i][0]
                por_point_light_c = (font_iti_light+5, self.select_list_xy[i][1]+40)
                por_point_left_up = (font_iti_light+55, self.select_list_xy[i][1]+10)
                por_point_left_down = (font_iti_light+55, self.select_list_xy[i][1]+70)
                pygame.draw.polygon(self.screen_object, (255, 255, 0), [por_point_light_c, por_point_left_up, por_point_left_down])

        for i in self.select_list:
            blt(self.select_list_ttf[i], self.screen_object, self.select_list_xy[i])

        blt(ttf("pixel",65).render(f"Spaceキーで{self.ok_text}", True, (240, 0, 0)), self.screen_object, (1300, self.nums.main.display_size[1] - 100))
        blt(ttf("kaisou",70).render(f"Esc : 戻る", True, (200,200,200)), self.screen_object, (20,10))

    def get(self):
        return self.select_list[self.selecting]

class NANI:
    """
        Class nani
        ---
        select(str) : None
    """
    def __init__(self, num: NUMs, screen: pygame.Surface):
        self.select: str = ""
        self.select_list: list[str] = ["かんたん", "ふつう", "むずかしめ", "なにこれって言いたくなるモード"]
        self.selectobj: select = select(num, screen, self.select_list, "難 易 度 選 択", 1)
        self.num: NUMs = num

    def display(self):
        for i in self.num.main.events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    self.num.main.nani = self.selectobj.get()
                    self.num.sound.play("ok")
                    return "selected"
                if i.key == pygame.K_UP:
                    if self.selectobj.selecting == 0:
                        pass
                    else:
                        self.selectobj.selecting -= 1
                        self.num.sound.play("ok")
                if i.key == pygame.K_DOWN:
                    if len(self.selectobj.select_list)-1 == self.selectobj.selecting:
                        pass
                    else:
                        self.selectobj.selecting += 1
                        self.num.sound.play("ok")

        # 選択画面（for文）を表示するselect.displayを呼び出す予定の関数
        
        self.selectobj.display()

class HISSA:
    def __init__(self, nums: NUMs, screens: pygame.Surface):
        self.nums = nums
        self.select_list: list[str] = ["カミナリ", "ビーム", "スロー"]
        self.select_obj: select = select(nums, screens, self.select_list, "必殺技選択", 0, ok_txt="開始")
        return

    def display(self):
        for i in self.nums.main.events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    self.nums.main.hissa = self.select_obj.get()
                    self.nums.sound.play("ok")
                    return "selected"
                if i.key == pygame.K_UP:
                    if self.select_obj.selecting == 0:
                        pass
                    else:
                        self.select_obj.selecting -= 1
                        self.nums.sound.play("ok")
                if i.key == pygame.K_DOWN:
                    if len(self.select_obj.select_list)-1 == self.select_obj.selecting:
                        pass
                    else:
                        self.select_obj.selecting += 1
                        self.nums.sound.play("ok")
        self.select_obj.display()


class bullet:
    def __init__(self, nums: NUMs,  text: list[str], screens: pygame.Surface):
        self.X: int = nums.main.display_size[0]
        self.Y: int = 610
        self.texts: list[str] = text
        self.all_texts: str = ""
        for i in text:
            self.all_texts += i
        self.nums: NUMs = nums
        self.color: tuple[int,int,int] = (140,150,175)
        self.screen: pygame.Surface = screens
        self.front_back: int = 20
        self.up_down: int = 5
        self.rect_obj: pygame.Rect = None
        if nums.main.nani == "かんたん":
            self.speead = 2.5
        elif nums.main.nani == "なにこれって言いたくなるモード":
            self.speead = 5.5
        elif nums.main.nani == "むずかしめ":
            self.speead = 4.3
        else:
            self.speead = 3.7

    def hissa_slow(self):
        if self.nums.runs.hissa_now and self.nums.main.hissa == "ビーム":
            if self.nums.main.nani == "かんたん":
                self.speead = 1.5
            elif self.nums.main.nani == "なにこれって言いたくなるモード":
                self.speead = 3.5
            elif self.nums.main.nani == "むずかしめ":
                self.speead = 3.0
            else:
                self.speead = 2.5
        else:
            if self.nums.main.nani == "かんたん":
                self.speead = 2.5
            elif self.nums.main.nani == "なにこれって言いたくなるモード":
                self.speead = 5.5
            elif self.nums.main.nani == "むずかしめ":
                self.speead = 4.3
            else:
                self.speead = 3.7
    def built(self):
        text = ""
        for i in self.texts:
            text += i
        text_obj = ttf("ipa", 60).render(text, True, (255,255,255))
        text_xy = (self.X+self.front_back, self.Y+self.up_down)

        bullet_xy = (
                    self.X, self.Y, 
                    self.front_back*2+CEN(text, 60, mode="HOW?", font="ipa")[0], 
                    self.up_down*2+70
                    )
        self.rect_obj = pygame.Rect(
                    self.X, self.Y, 
                    self.front_back*2+CEN(text, 60, mode="HOW?", font="ipa")[0], 
                    self.up_down*2+70
                    )
        pygame.draw.rect(self.screen, self.color, bullet_xy, border_radius=10)
        blt(text_obj, self.screen, text_xy)

        self.X -= self.speead

    def delete(self):
        self.nums.runs.bullets["f"].append(self)
        del self.nums.runs.bullets["t"][0]

class stone:
    def __init__(self, num:NUMs, xy: tuple[int, int], screen:pygame.Surface):
        self.xy: list[int] = [xy[0], xy[1]]
        self.screen: pygame.Surface = screen
        self.num: NUMs = num
    def built(self):
        if self.xy[0] <= -30:
            del self.num.runs.stones[0]
            return
        pygame.draw.rect(self.screen, (111, 111, 111), (self.xy[0], self.xy[1], 30, 30))
        self.xy[0]-=2

class RUNS:
    def __init__(self, num: NUMs, screens: pygame.Surface):
        import time
        # ---初期関連実装---
        self.start: int = time.time()
        self.num: NUMs = num
        self.screen: pygame.Surface = screens
        # ---弾関連実装---
        self.bullets: dict[str, list[bullet]] = {"t":[], "f":[]}
        self.max_space: float = 2.5
        # ---ポイント関連実装---
        self.point: int = 0
        # ---HP関連実装---
        self.hp: int = 7
        self.hp_img: pygame.Surface = pygame.transform.scale(pygame.image.load(f"imgs/HP.png").convert_alpha(), (100,100))
        # ---コンボ関連実装---
        self.combo: int = 0
        # ---ビーム関連実装---
        self.beam: float = time.time() -1         # 0.5s
        self.beam_to_X: int = 0
        # ---ユーザー関連実装---
        self.user: float = time.time() - 10
        self.user_now: int = 0
        self.usr_xy: list[int] = [10, 550]
        self.usr_obj: list[pygame.Surface] = [
            pygame.transform.scale(pygame.image.load(f"imgs/usr1.png").convert_alpha(), (170,220)), 
            pygame.transform.scale(pygame.image.load(f"imgs/usr2.png").convert_alpha(), (170,220)), 
            pygame.transform.scale(pygame.image.load(f"imgs/usr3.png").convert_alpha(), (170,220))
            ]
        
        # ---石関連実装---
        self.stones_xys: list[tuple[int, int]] = [(num.main.display_size[0], 825), (num.main.display_size[0], 925)]
        self.stone: list[bool] = [True] + [False] * 200
        self.stones: list[stone] = [stone(num, self.stones_xys[1], screens)]
        self.stone_now: int = 0
        # ---必殺技関連実装---
        self.hissa_now: bool = False             # 発動中か
        self.hissa_time: float = None            # スタートタイム
        self.hissa_info: str = "チャージ中"       # チャージ中/発動可 50,120
        self.hissa_cool: int = 15
        self.hissa_cool_now: float = time.time() - 10
        self.hissa_while: dict[str, float] = {"カミナリ": 0.7, "ビーム": 0.2, "スロー": 10}   # 動作(表示)時間
        # ~~~カミナリ~~~    360,250
        self.don_img: pygame.Surface = pygame.transform.scale(pygame.image.load("imgs/DOON.png").convert_alpha(), (208,390))
        # ~~~必殺ビーム~~~
        self.pun_num: int = 7                   # 残り打てる回数


        if num.main.nani == "かんたん":
            self.max_space: float = 8
            self.min_space: float = 1.2
            self.user_spead: float = 1
            self.hp = 8
            self.points: dict[str, int] = {"nom": 3, "miss": -5, "combo": 4, "hp": 10, "one": 2, "don": 15, "pun": 12}
        elif num.main.nani == "なにこれって言いたくなるモード":
            self.points: dict[str, int] = {"nom": 5, "miss": -15, "combo": 4, "hp": 20, "one": 3, "don": 10, "pun": 12}
            self.max_space: float = 2.5
            self.min_space: float = 0.3
            self.user_spead: float = 0.15
            self.hp = 5
        elif num.main.nani == "むずかしめ":
            self.points: dict[str, int] = {"nom": 3, "miss": -10, "combo": 3, "hp": 10, "one": 3, "don": 10, "pun": 12}
            self.max_space: float = 4
            self.min_space: float = 0.4
            self.user_spead: float = 0.25
            self.hp = 6
        else:
            self.max_space: float = 4.5
            self.min_space: float = 0.8
            self.user_spead: float = 0.3
            self.points: dict[str, int] = {"nom": 3, "miss": -7, "combo": 3, "hp": 10, "one": 2, "don": 10, "pun": 10}
        self.last_create: float = time.time() - self.max_space -1 
        self.alphabet: list[str] = [chr(i) for i in range(ord("a"), ord("z") + 1)]           # アルファベット一覧生成式

    def words(self, nanis: list[int]):
        if nanis == None:
            nanis = [1,1,1,1,1,1,2,2,2,2]
        import random
        File1 = open("EASY.ptn")
        File2 = open("NOMAL.ptn")
        File3 = open("HARD.ptn")
        RE1 = File1.readlines()
        RE2 = File2.readlines()
        RE3 = File3.readlines()
        File1.close()
        File2.close()
        File3.close()
        sl = random.choice(nanis)
        if sl == 1:
            return random.choice(RE1).split(";")[1].split("\n")[0].split("+")
        elif sl == 2:
            return random.choice(RE2).split(";")[1].split("\n")[0].split("+")
        elif sl == 3:
            return random.choice(RE3).split(";")[1].split("\n")[0].split("+")

    def create(self, OPT=False):
        import random
        import time
        if self.num.main.nani == "かんたん":
            per_list = [True] + [False] * 450
            word_per = [1,1,1,1,1,1,2,2,2,2]
        elif self.num.main.nani == "なにこれって言いたくなるモード":
            per_list = [True] + [False] * 70
            word_per = [2,2,2,2,3,3,2,3,3,3]
        elif self.num.main.nani == "むずかしめ":
            per_list = [True] + [False] * 170
            word_per = [1,1,2,2,2,2,2,2,2,2]
        else:
            per_list = [True] + [False] * 190
            word_per = [1,1,1,1,2,2,2,2,2,2]
        if time.time()-self.last_create>=self.max_space:
            word = self.words(word_per)
            bl = bullet(self.num, word, self.screen)
            self.last_create = time.time()
        elif random.choice(per_list):
            if self.min_space>=time.time()-self.last_create:
                return None
            word = self.words(word_per)
            bl = bullet(self.num, word, self.screen)
            self.last_create = time.time()
        else:
            bl = None
        return bl


    def built(self):
        import time
        import random
        for event in self.num.main.events:
            if event.type == pygame.KEYDOWN:
                # 入力された文字を直接取得（例: 'a', 'A', '!' など）
                char = event.unicode
                
                if self.hissa_now != True and self.bullets["t"] != []:                          # 必殺技実行中の場合
                    if event.key == pygame.K_SPACE and self.num.main.hissa == "ビーム":
                        if self.pun_num>0:
                            self.hissa_now = True
                            self.hissa_time = time.time()
                            self.num.sound.play("pun")
                            self.beam_to_X = self.bullets["t"][0].X-20
                            self.bullets["t"][0].delete()
                            self.pun_num -= 1
                            self.point += self.points["pun"]
                    elif event.key == pygame.K_SPACE and self.hissa_cool <= (time.time()-self.hissa_cool_now):
                        self.hissa_now = True
                        self.hissa_time = time.time()
                        if self.num.main.hissa == "カミナリ":
                            self.num.sound.play("don")
                        elif self.num.main.hissa == "スロー":
                            self.num.sound.play("slow")
                        
                if char not in self.alphabet or self.bullets["t"] == []:
                    pass
                else:
                    self.beam = time.time()
                    self.beam_to_X = self.bullets["t"][0].X-20
                    if self.bullets["t"][0].texts[0] == char: #あってるか判定
                        self.point += self.points["one"]         #ポイント追加
                        
                        self.combo += 1
                        self.beam = time.time()
                        del self.bullets["t"][0].texts[0]
                        if self.bullets["t"][0].texts == []:     #もし最後なら
                            self.point += self.points["nom"]  
                            self.num.sound.play("oks")
                            self.bullets["t"][0].delete()         #ここでbullets["t"]→["f"]へも移動する
                        else:
                            self.num.sound.play("ok")
                        
                    else:
                        self.point += self.points["miss"] 
                        self.num.sound.play("bad")
                        if self.combo > 1:
                            self.point += self.points["combo"]*self.combo
                        self.combo = 0
                        if self.num.main.nani == "なにこれって言いたくなるモード":
                            self.bullets["t"][0].texts.append(str(char))

        if 70-int(time.time()-self.start) <= 0:
            self.screen.fill((0,0,0))
            self.num.ranks.players_num += 1
            if self.combo > 1:
                self.point += self.points["combo"]*self.combo
            self.point += self.points["hp"]*self.hp
            task = threading.Thread(
                target=self.num.ranks.update,
                kwargs={"up": True, "userpoint": self.point},
                daemon=False
            )
            task.start()
            end(self.screen, self.num, "fin")
            self.num.main.change_page("result")
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/bgm_result.mp3")  # 読み込み
            pygame.mixer.music.play(-1) 
            self.screen.fill((0,0,0))
            return
        elif self.hp == 0:
            self.screen.fill((0,0,0))
            self.num.ranks.players_num += 1
            if self.combo > 1:
                self.point += self.points["combo"]*self.combo
            self.point += self.points["hp"]*self.hp
            task = threading.Thread(
                target=self.num.ranks.update,
                kwargs={"up": True, "userpoint": self.point},
                daemon=False
            )
            task.start()
            end(self.screen, self.num, "over")
            
            
            self.num.main.change_page("result")
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/bgm_result.mp3")  # 読み込み
            pygame.mixer.music.play(-1) 
            self.screen.fill((0,0,0))
            return

        # 必殺技 infos
        if self.num.main.hissa != "ビーム":
            if self.hissa_now:
                self.hissa_info = "発動中"
            elif time.time() - self.hissa_cool_now >= self.hissa_cool:
                self.hissa_info = "発動可"
            else:
                self.hissa_info = "チャージ中"
        else:
            if self.pun_num >= 0:
                self.hissa_info = f"残り{self.pun_num}発"
            else:
                self.hissa_info = f"弾切れ"
        blt(ttf("pixel", 50).render(self.hissa_info, True, (200,200,0)), self.screen, (50, 120))


        
        new_bl_obj = self.num.runs.create()                          # 弾生成
        if new_bl_obj != None:
            self.bullets["t"].append(new_bl_obj)
        if self.bullets["t"] != []:
            self.bullets["t"][0].color = (125, 210, 220)
            self.bullets["t"][0].up_down = 8
            

        if random.choice(self.stone):
            self.stones.append(stone(self.num, self.stones_xys[self.stone_now], self.screen))
            if self.stone_now == 1:
                self.stone_now = 0
            else:
                self.stone_now = 1
        

        
        for i in reversed(self.bullets["t"]):         # 弾描画
            i.hissa_slow()
            i.built()

        if time.time() - self.user >= self.user_spead:
            if self.user_now == 1:
                self.user_now = 0
            else:
                self.user_now = 1
            self.user = time.time()

        
        if self.hissa_now:                                # 必殺技が起動中の場合
            if time.time()-self.hissa_time >= self.hissa_while[self.num.main.hissa]:
                self.hissa_now = False
                self.hissa_cool_now = time.time()       # 間隔更新
            elif self.num.main.hissa == "カミナリ":
                blt(self.don_img, self.screen, (360,390))
                for i in self.bullets["t"]:
                    if i.X <= 950:
                        i.delete()
                        self.point += self.points["don"]
            elif self.num.main.hissa == "ビーム":
                pygame.draw.line(self.screen, (0, 207, 210), (160,660), (self.beam_to_X, 660), width=7)
                
            self.user_now = 2
            

        
        blt(self.usr_obj[self.user_now], self.screen, self.usr_xy)

        # 衝突判定
        if self.bullets["t"] != [] and self.usr_obj[self.user_now].get_rect(topleft=(self.usr_xy[0], self.usr_xy[1])).colliderect(self.bullets["t"][0].rect_obj):
            self.num.sound.play("bom")
            self.combo = 0
            self.hp -= 1
            self.bullets["t"][0].delete()

        pygame.draw.rect(self.screen, (139, 115, 56), (-1, 780, self.num.main.display_size[0]+2, self.num.main.display_size[1]+1))

        blt(ttf("pixel", 23).render(f"POINT", True, (220, 223, 0)), self.screen, (80,5))
        blt(ttf("pixel", 90).render(f"{self.point} Pt", True, (220, 223, 0)), self.screen, (80,20))

        if self.combo > 1:
            #blt(ttf("pixel", 23).render(f"COMBO", True, (220,0,0)), self.screen, (480,2))
            blt(ttf("pixel", 80).render(f"{self.combo} Combo", True, (220, 0, 0)), self.screen, (480,20))

        
        blt(ttf("pixel", 80).render(f"HP", True, (255,0,0)), self.screen, (890, 20))
        blt(ttf("pixel", 90).render(f"x{self.hp}", True, (255,0,0)), self.screen, (985, 20))

        blt(ttf("pixel", 60).render(f"のこり", True, (250,250,250)), self.screen, (1530, 60))
        blt(ttf("pixel", 120).render(f"{70-int(time.time()-self.start)}", True, (250,250,250)), self.screen, (1710, 10))
        blt(ttf("pixel", 60).render(f"s", True, (250,250,250)), self.screen, (1840, 60))


        if self.stones != []:
            for i in self.stones:
                i.built()

        if time.time() - self.beam  <= 0.05:
            pygame.draw.line(self.screen, (255, 215, 0), (160,660), (self.beam_to_X, 660), width=2)



class ranking:
    def __init__(self):
        self.all_points: list[list] = []
        self.rankings: list[list] = []
        try:
            with open('all_points.pkl', 'rb') as f:
                data = pickle.load(f)
                self.all_points: list[list] = data[0]
                self.players_num: int = data[1]
        except FileNotFoundError:
            with open('all_points.pkl', 'wb') as f:
                pickle.dump([self.all_points, 0], f)
            self.players_num: int = 0

    def update(self, up: bool, userpoint: int = None):
        try:
            with open('all_points.pkl', 'rb') as f:
                self.all_points: list[list] = pickle.load(f)[0]
        except FileNotFoundError:
            with open('all_points.pkl', 'wb') as f:
                pickle.dump([self.all_points, self.players_num], f)
        if up:
            userdata = ([f"player@{self.players_num}", userpoint, datetime.now().strftime("%m%d.%H-%M.%S")])
            self.all_points.append(userdata)
        with open('all_points.pkl', 'wb') as f:
            pickle.dump([self.all_points, self.players_num], f)


        self.rankings = [
            [i, *player]
            for i, player in enumerate(
                sorted(self.all_points, key=lambda x: x[1], reverse=True)[:10],
                start = 1
            )
        ]


    def returns(self):
        self.update(up=False)
        return self.rankings

    def get_rank(self, point: int) -> int:
        return sum(player[1] > point for player in self.all_points) + 1
























def debug_GUI(screen: pygame.Surface, nums: NUMs, clock: pygame.time.Clock, interval: int = 100):
    blt(ttf("pixel", 40).render(f"KeyboardRunning DebugMODE", True, (255,0,0)), screen, (10,0))
    if nums.main.menu in nums.main.menu_list:
        blt(ttf("pixel", 30).render(f"menu : {nums.main.menu}", True, (255,0,0)), screen, (10,50))
    else:
        blt(ttf("pixel", 30).render(f"menu(Not Found) : {nums.main.menu}", True, (255,0,0)), screen, (10,50))
    blt(ttf("pixel", 30).render(f"display : {nums.main.display_size}", True, (255,0,0)), screen, (10,90))
        # FPS表示
    fps = clock.get_fps()

    fps_text = ttf("pixel", 30).render(
        f"FPS : {fps:.1f}",
        True,
        (0, 255, 0) if fps >= 55 else (255, 0, 0)
    )

    blt(fps_text, screen, (10, 130))
    width, height = screen.get_size()
    font = ttf("bis", 10)

    # 中心座標
    center_x = width // 2
    center_y = height // 2

    # グリッドの色
    grid_color = (160, 160, 160)
    center_color = (255, 0, 0)

    # -------------------------
    # 縦線
    # -------------------------
    for x in range(center_x % interval, width, interval):

        color = center_color if x == center_x else grid_color

        pygame.draw.line(
            screen,
            color,
            (x, 0),
            (x, height),
            1
        )

        text = font.render(str(x), True, color)
        screen.blit(text, (x + 4, height - 25))

    # -------------------------
    # 中心より左側の縦線
    # -------------------------
    for x in range(center_x - interval, -1, -interval):

        pygame.draw.line(
            screen,
            grid_color,
            (x, 0),
            (x, height),
            1
        )

        text = font.render(str(x), True, grid_color)
        screen.blit(text, (x + 4, height - 25))

    # -------------------------
    # 横線
    # -------------------------
    for y in range(center_y % interval, height, interval):

        color = center_color if y == center_y else grid_color

        pygame.draw.line(
            screen,
            color,
            (0, y),
            (width, y),
            1
        )

        text = font.render(str(y), True, color)
        screen.blit(text, (width - 45, y + 4))

    # -------------------------
    # 中心より上側の横線
    # -------------------------
    for y in range(center_y - interval, -1, -interval):

        pygame.draw.line(
            screen,
            grid_color,
            (0, y),
            (width, y),
            1
        )

        text = font.render(str(y), True, grid_color)
        screen.blit(text, (width - 45, y + 4))


    # =========================
    # マウス座標
    # =========================

    mouse_x, mouse_y = pygame.mouse.get_pos()

    mouse_text = font.render(
        f"({mouse_x}, {mouse_y})",
        True,
        (255, 255, 255)
    )

    # 余白
    padding_x = 7
    padding_y = 5

    box_width = mouse_text.get_width() + padding_x * 2
    box_height = mouse_text.get_height() + padding_y * 2

    # -------------------------
    # マウスの左上に表示
    # -------------------------

    box_x = mouse_x - box_width - 12
    box_y = mouse_y - box_height - 12

    # 左端からはみ出す場合は右上へ
    if box_x < 0:
        box_x = mouse_x + 12

    # 上端からはみ出す場合は左下へ
    if box_y < 0:
        box_y = mouse_y + 12

    # -------------------------
    # 背景
    # -------------------------

    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (box_x, box_y, box_width, box_height)
    )

    # -------------------------
    # 枠線
    # -------------------------

    pygame.draw.rect(
        screen,
        (220, 220, 220),
        (box_x, box_y, box_width, box_height),
        1
    )

    # -------------------------
    # 座標
    # -------------------------

    screen.blit(
        mouse_text,
        (
            box_x + padding_x,
            box_y + padding_y
        )
    )