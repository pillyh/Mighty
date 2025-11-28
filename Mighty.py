#봇 공약정하기, 카드버리기 등 알고리즘 수정
#봇 기루바꿀때 deck_evaluate 수정하기
#누가 몇장 먹었는지 보여주기
#게임전략 구현

print('♦️ ♠️ ♥️ ♣️')
print('Rule')
print('♠️  : S, ♦️  : D, ♣️  : C, ♥️  : H, joker = joker')
print('ex) ♠️  A = SA')
print('자세한 룰은 나무위키 참조하세용 너무 길어용 노기루는 없어용')

def look(li): #문양 넣어서 잘 보이게
    if type(li) == list:
        if len(li) == 0:
            return 'No card'
        rtn = []
        for i in li:
            if i == 'joker':
                rtn.append(i)
            elif i[0] == 'S':
                a = '♠️  '+i[1:]
                rtn.append(a)
            elif i[0] == 'H':
                a = '♥️  '+i[1:]
                rtn.append(a)
            elif i[0] == 'D':
                a = '♦️  '+i[1:]
                rtn.append(a)
            elif i[0] == 'C':
                a = '♣️  '+i[1:]
                rtn.append(a)
        a = str()
        for i in rtn:
            a = a + ', ' + i
        return a[2:]
    else:
        if li[0] == 'S':
            return '♠️  '+li[1:]
        elif li[0] == 'H':
            return '♥️  '+li[1:]
        elif li[0] == 'D':
            return '♦️  '+li[1:]
        elif li[0] == 'C':
            return '♣️  '+li[1:]
        else:
            return 'joker'
        
#import
import random
import time

#카드패 생성(완)
#cardlist: 모든 카드
cardlist = ['joker']
numli = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
for i in ['S','D','H','C']:
    for j in numli:
        cardlist.append(i+j)

#spadelist: 모든 스페이드 리스트
spadelist = []
diamondlist = []
heartlist = []
cloverlist = []
for i in numli[::-1]:
    spadelist.append('S'+i)
    diamondlist.append('D'+i)
    heartlist.append('H'+i)
    cloverlist.append('C'+i)

def shapelist(shape):
    if shape == 'S':
        return spadelist
    elif shape == 'D':
        return diamondlist
    elif shape == 'H':
        return heartlist
    elif shape == 'C':
        return cloverlist

#점수카드 리스트
score_card = []
for i in ['S','D','H','C']:
    for j in numli[8:]:
        score_card.append(i+j)

#모든 기루 리스트
def all_giru(giru):
    if giru == 'S':
        return spadelist
    elif giru == 'D':
        return diamondlist
    elif giru == 'H':
        return heartlist
    else:
        return cloverlist
        
#주공 부를 수 있는거
pos_li = []
for i in ['S','D','H','C']:
    for j in range(10,21):
        a = str(j) +','+ i
        pos_li.append(a)

class Deck:
    def __init__(self, deck):
        self.deck = deck
        self.slist = list(i for i in spadelist if i in deck)
        self.hlist = list(i for i in heartlist if i in deck)
        self.dlist = list(i for i in diamondlist if i in deck)
        self.clist = list(i for i in cloverlist if i in deck)
        
    def sorted_deck(self, giru='!'): #return 티-커-기루-나머지 순 정렬
        sorted_deck = []
        if self.mighty(giru) in self.deck:
            sorted_deck.append(self.mighty(giru))
        if 'joker' in self.deck:
            sorted_deck.append('joker')
        
        if giru != '!':
            for i in self.girulist(giru):
                sorted_deck.append(i)
        
        for i in (self.slist, self.hlist, self.dlist, self.clist):
            for j in i:
                if j not in sorted_deck:
                    sorted_deck.append(j) 
            
        return sorted_deck
    
    def girulist(self, giru):#덱에있는 기루리스트 반환
        if giru == 'S':
            return self.slist
        if giru == 'H':
            return self.hlist
        if giru == 'D':
            return self.dlist
        if giru == 'C':
            return self.clist
    
    def mighty(self, giru):
        mighty = 'SA'
        if giru == 'S':
            mighty = 'DA'
        return mighty
    
    def jokercall(self,giru):
        jokercall = 'C3'
        if giru == 'C':
            jokercall = 'S3'
        return jokercall
    
    def topcard(self, giru, pot = []):#문양별 탑카드 2차원리스트
        s_topcard = []
        for i in spadelist:
            if i == self.mighty(giru):
                continue
            if i in self.slist:
                s_topcard.append(i)
            elif i in pot:
                continue
            else: 
                break
        h_topcard = []
        for i in heartlist:
            if i in self.hlist:
                h_topcard.append(i)
            elif i in pot:
                continue
            else: 
                break
        d_topcard = []
        for i in diamondlist:
            if i == self.mighty(giru):
                continue
            if i in self.dlist:
                d_topcard.append(i)
            elif i in pot:
                continue
            else: 
                break
        c_topcard = []
        for i in cloverlist:
            if i in self.clist:
                c_topcard.append(i)
            elif i in pot:
                continue
            else: 
                break
        topcard = list(set(s_topcard + h_topcard + d_topcard + c_topcard))
        return topcard
    
    def mulcard(self, giru, pot = []):
        d = self.deck[:]
        for i in d[:]:
            if i == self.mighty(giru):
                d.remove(i)
            elif i == 'joker':
                d.remove(i)
            elif i in self.topcard(self, giru, pot):
                d.remove(i)
        return d

class Player:
    def __init__(self, deck):
        self.name = 'player'
        self.deck = sorted(deck)
        self.mode = 0
        
    def position(self, revealed):
        if self.mode == 2:
            return 'player(king)'
        elif self.mode == 1 and revealed:
            return 'player(friend)'
        else:
            return 'player'
    
    def choose_friend(self, giru): #프렌 부르기
        global friend_call
        while True:
            friend_call = input('choose friend:')
            if friend_call in cardlist:
                break
            else:
                print('error')
        return friend_call

    def grab(self, giru, target_num, trash): # 쓰레기 더미에서 카드 뽑아서 덱에 넣기
        print('trash:', look(Deck(trash).sorted_deck(giru)))
        print('your deck:', look(Deck(self.deck).sorted_deck(giru)))
        self.deck.extend(trash) # 덱에 trash 추가
        print('your new deck:', look(Deck(self.deck).sorted_deck(giru)))
        
        #기루바꾸기
        print(f"giru: {look(giru)}, target: {target_num}")
        if target_num < 19:
            while True:
                change_giru = input('Change giru?...(Y/N)')
                if change_giru == 'Y':
                    while True:
                        giru = input('Enter New giru:')
                        if giru in ['S','D','H','C']:
                            target_num += 2
                            print(f"giru: {look(giru)}, target: {target_num}")
                            break
                        else:
                            print('error')
                    break
                elif change_giru == 'N':
                    break
                else:
                    print('error')
        
        global pick
        while True:
            pick = input('pick 3 cards to throw: ').split(',') #버릴거 3장 고르기
            
            pick = [p.strip() for p in pick]
            pick = list(set(pick))
            if (len(pick) == 3) and set(pick).issubset(set(self.deck)):
                for i in pick:
                    self.deck.remove(i)
                
                return (giru, target_num)
            else:
                print('error')
        
    def kill(self, giru, trash): #trash받아서 킬 부르기: 킬이 trash에 있으면 다시 부르기
        while True:
            kill = input('Choose card to kill:')
            if kill in trash:
                print('Nobody killed, kill again')
            elif kill in self.deck:
                print('error: in your deck')
            elif kill in cardlist:
                return kill
            else:
                print('error')
    
    def putcard(self, play_order, round, used_card, leadshoot = None, call=0):
        deck = self.deck
        mighty, joker, jokercall = card_change(giru)
        while True:            
            if play_order == 0:
                print('첫 순서')
            else:
                print('leadshoot:',leadshoot)
            print('your deck:', look(Deck(deck).sorted_deck(giru)))
            a = input('카드를 내세요: ')  
            
            if a in possible(giru, play_order, round, deck, leadshoot, call):
                self.deck.remove(a)
                
                if a == joker:
                    if play_order == 0:
                        while True:
                            ls = input('leadshoot:')
                            if ls in ['S','H','D','C']:
                                rtn = 'joker'+ls
                                return rtn
                            else:
                                print('error')
                    else:
                        return a
                    
                elif a == jokercall:
                    if play_order == 0 and round != 0:
                        while True:
                            con = input('jokercall?...(Y/N)')
                            if con in ['Y','N']:
                                leadshoot = a[0]
                                rtn = a + con
                                return rtn
                            else:
                                print('error')
                    else:
                        return a
                else:
                    return a
                    
            else:
                print('error')


class BOT:
    def __init__(self, deck, name):
        self.name = name
        self.deck = sorted(deck)
        self.bet = deck_evaluation(deck)
        self.mode = 0 # 0: normal, 1: friend, 2: king

    def position(self, revealed):
        if self.mode == 2:
            return self.name + '(king)'
        elif self.mode == 1 and revealed:
            return self.name + '(friend)'
        else:
            return self.name
    
    def choose_friend(self, giru):#봇이 프렌 부르기
        global friend_call
        deck = Deck(self.deck)
        #기루 반영
        (mighty, joker) = (deck.mighty(giru), 'joker')
    
        #모든 카드 좋은 순서로 정렬
        sorted_card_list = [mighty, joker]
        
        if giru == 'S':
            sorted_card_list.extend(spadelist)
        elif giru == 'D':
            sorted_card_list.extend(diamondlist)
        elif giru == 'H':
            sorted_card_list.extend(heartlist)
        else:
            sorted_card_list.extend(cloverlist)
        
        
        
        #자신에게 없는 가장 좋은 카드 골라서 프렌으로 부르기
        for i in sorted_card_list:
            if i not in deck.deck:
                friend_call = i
                break
        return friend_call
    
    def bkmk(self, n):#덱, 현재 공약 보고 부를까말까
        if n < self.bet[1]: #불러
            return 1
        else:
            return 0 #참아
    
    def grab(self, giru, target_num, trash): #카드 받고 버릴거 버리기
        
        
        print('(확인용) bot deck:', look(Deck(self.deck).sorted_deck(giru)))
        print('(확인용) trash:', look(Deck(trash).sorted_deck(giru)))
        
        new_giru = deck_evaluation(self.deck)[0]
        
        if giru == new_giru:
            pass
        else:
            if deck_evaluation(self.deck)[1] >= target_num + 2:
                giru = new_giru
                target_num += 2
                print('New giru:', look(giru), 'New target number:', look(target_num))
                
        deck = Deck(self.deck)
        mighty, joker, jokercall = (deck.mighty(giru), 'joker', deck.jokercall(giru))
        
        # 쓰레기 더미에서 카드 뽑기(임시로 대충)
        self.deck.extend(trash)
        deck = Deck(self.deck)
        
        deck_dict = dict.fromkeys(self.deck,0)
        for i in deck_dict.keys():
            #특수카드
            if i == mighty or i == joker:
                deck_dict[i] = 100
            elif i in deck.girulist(giru) and i in deck.topcard(giru):
                deck_dict[i] = 90
            elif i in deck.girulist(giru):
                deck_dict[i] = 80
            elif i in deck.topcard(giru):
                deck_dict[i] = 70
            elif i == jokercall:
                deck_dict[i] = 50
            #물패
            else:
                if i in score_card:
                    deck_dict[i] = -10
                else:
                    deck_dict[i] = 0
                
        
        smallest_keys = sorted(deck_dict, key=deck_dict.get)[:3]
        
        global pick
        pick = []
        
        for i in smallest_keys:
            self.deck.remove(i)
            pick.append(i)
        
        return (giru, target_num)
                
    def kill(self, giru, trash): #킬부르기
        joker = 'joker'
        deck = self.deck
        kill_list = [] #킬 부를 카드들 = 나한테 없는 좋은 카드들(티 제외)
        if joker not in deck:
            kill_list.append(joker)
        for i in all_giru(giru):
            if i not in deck:
                kill_list.append(i)
        
        #킬리스트 앞에서부터 확인
        #trash에 있으면 다시 킬
        for i in kill_list:
            print('kill:', look(i))
            if i in trash:
                print('Nobody killed, kill again')
            else:
                return i
    
    def putcard(self, play_order, round, used_card, leadshoot = None, call=0):
        deck = self.deck
        mighty, joker, jokercall = card_change(giru)
        pos = possible(giru, play_order, round, deck, leadshoot, call)
        random.shuffle(pos)
        rtn = pos[0]
        self.deck.remove(pos[0])
        if rtn == joker and play_order == 0:
            ls = giru
            return rtn + ls
        if rtn == jokercall and play_order == 0:
            return rtn + 'Y'
        return rtn
    
    def __str__(self):
        return self.name
    
    def putcard_1(self, play_order, round, used_card, leadshoot = None, call=0):
        deck = self.deck
        mighty, joker, jokercall = card_change(giru)
        top = Deck(self.deck).topcard(giru, used_card)
        mul = Deck(self.deck).mulcard(giru,used_card)
        gtop = []
        glist = Deck(deck).girulist(giru)
        for i in top:
            if i in shapelist(giru):
                gtop.append(i)
        pos = possible(giru, play_order, round, deck, leadshoot, call)
        if len(pos) == 1:
            return pos[0]
        
        if self.mode == 2: #주공일때
            if play_order == 0:
                if round == 0:
                    if len(set(top) - set(shapelist(giru))) != 0:
                        for i in set(top) - set(shapelist(giru)):
                            return i
                    else:
                        return mul[0]
                else:
                    if (friend_call != joker) and (joker not in deck) and (jokercall in deck):
                        return jokercall + 'Y'
                    elif len(gtop) != 0:
                        return gtop[0]
                    elif len(gtop) == 0:
                        return glist[-1]
    


def gameready(): #Players 빈 리스트 만들고 인원수 따라 gameready5/6 실행
    se = random.random()
    print("Game start")
    a = input()
    if a!="":
        random.seed(float(a))
        se = a
    random.seed(se)
    print(f"Seed: {se}")
    global Players
    Players = [] #players list 생성
    n = 0
    while n != '5' and n != '6': #인원수 선택/5,6 아니면 error
        n = input("Number of people to play:")
        if n == '5':
            return gameready5()
        elif n == '6':
            return gameready6()
        else:
            print('error')


#필요한 함수들
def deck_shuffle(n): #인원수n 따라 return (deck1, deck2, ..., trash)
    random.shuffle(cardlist)
    if n == 5:
        deck1 = cardlist[0:10]
        deck2 = cardlist[10:20]
        deck3 = cardlist[20:30]
        deck4 = cardlist[30:40]
        deck5 = cardlist[40:50]
        trash = cardlist[50:]
        t = (deck1, deck2, deck3, deck4, deck5, trash)
        
    if n == 6:
        deck1 = cardlist[0:8]
        deck2 = cardlist[8:16]
        deck3 = cardlist[16:24]
        deck4 = cardlist[24:32]
        deck5 = cardlist[32:40]
        deck6 = cardlist[40:48]
        trash = cardlist[48:]
        t = (deck1, deck2, deck3, deck4, deck5, deck6, trash)
    
    for i in t:
        if isrr(i):
            return deck_shuffle(n)
    return t

def isrr(deck):
    s = 0
    for i in deck:
        if i[1] == '1':
            s += 0.5
        elif i[1] in ['J','Q','K','A']:
            s += 1
        elif i[0] == 'j':
            s -= 1
    if s <= 0.5:
        return True
    else:
        return False

def evaluation(symbol_list): #문양별 패 평가, return cnt
    cnt = 0
    for i in symbol_list:
        if i[1] == 'J':
            cnt += 11
        elif i[1] == 'Q':
            cnt += 12
        elif i[1] == 'K':
            cnt += 13
        elif i[1] == 'A':
            cnt += 14
        else:
            n = int(i[1])
            if n > 5:
                cnt += n
            elif n == 1:
                cnt += 10
            else:
                cnt += 5
    return cnt
       
#미완(더 제대로 해야함)
def deck_evaluation(deck): # 패 평가, return (giru, target_num)
    #기루 선정
    deck = Deck(deck)
    card_ev = {}
    card_ev['S'] = evaluation(deck.slist)
    card_ev['D'] = evaluation(deck.dlist)
    card_ev['H'] = evaluation(deck.hlist)
    card_ev['C'] = evaluation(deck.clist)
    giru = max(card_ev, key = card_ev.get)

    #기루 적용
    mighty = deck.mighty(giru)
    
    #패 점수 계산
    #이게 제일 어려울듯
    #일단 대충 해둠
    target_num = 10
    if 'joker' in deck.sorted_deck(giru):
        target_num += 1
    if mighty in deck.sorted_deck(giru):
        target_num += 1
    target_num += card_ev[giru]/10
    
    target_num = int(target_num)
    return (giru, target_num)


#5마, 6마 게임: return (king, friend_call, giru, target_num)
def gameready5(): 
    #패돌리기
    t = deck_shuffle(5)
    Players.append(Player(t[0]))
    for i in range(1, 5):
        Players.append(BOT(t[i], f'bot{i}'))
    print("Your Deck:", look(Deck(Players[0].deck).sorted_deck()))
    #주공선정
    giru = ''
    target_num = 0
    i = -1
    die = [0, 0, 0, 0, 0]
    target_num = 12
    burum = False
    while True:
        i = (i + 1) % 5
        if die[i] == 1: continue
        if Players[i].name == 'player':
            while True:
                x = input(f'공약({target_num+1}이상), 기루다: ')
                x = x.replace(' ','')
                
                if x == 'die':
                    die[i] = 1
                    break
                else:
                    if x not in pos_li:
                        print('error')
                    else:
                        x, y = x.split(',')
                        x = int(x)
                        if 20 >= x > target_num:
                            giru = y
                            target_num = x
                            burum = True
                            break
                        else:
                            print('error')
        
        else:
            time.sleep(0.5)
            if Players[i].bkmk(target_num) == 1:
                target_num += 1
                giru = Players[i].bet[0]
                print(Players[i].name, target_num, look(Players[i].bet[0]))
                burum = True
            else:
                die[i] = 1
                print(Players[i].name, "die")
        print('die:', sum(die))
        print()
        
        if sum(die) == 5:
                die = [0,0,0,0,0]
                target_num -= 1
        if sum(die) == 4 and burum:
            break
    
    king = -1
    for j in range(5):
        if die[j] == 0:
            king = Players[j]
            break
    if king.name == 'player':
        print('you are king')
    else:
        print(f'{king.name} is king')
    
    king.mode = 2
    (giru, target_num) = king.grab(giru, target_num, t[5])
    
    friend_call = king.choose_friend(giru)
    
    
    return (king, friend_call, giru, target_num)

def gameready6(): #6마 게임 준비
    #패돌리기
    t = deck_shuffle(6)
    Players.append(Player(t[0]))
    for i in range(1, 6):
        Players.append(BOT(t[i], f'bot{i}'))
    deck = Deck(Players[0].deck)
    print("Your Deck:", look(deck.sorted_deck()))
    #주공선정
    giru = ''
    target_num = 0
    i = -1
    die = [0, 0, 0, 0, 0, 0]
    burum = False
    target_num = 12
    while True:
        i = (i + 1) % 6
        if die[i] == 1: continue
        if Players[i].name == 'player':
            while True:
                x = input(f'공약({target_num + 1}이상), 기루다: ')
                x = x.replace(' ','')
                if x == 'die':
                    die[i] = 1
                    break
                else:
                    if x not in pos_li:
                        print('error')
                    else:
                        x, y = x.split(',')
                        x = int(x)
                        if x > target_num:
                            giru = y
                            target_num = x
                            burum = True
                            break
                        else:
                            print('error')
        else:
            if Players[i].bkmk(target_num-1) == 1:
                target_num += 1
                giru = Players[i].bet[0]
                print(Players[i].name, target_num, look(Players[i].bet[0]))
                burum = True
            else:
                die[i] = 1
                print(Players[i].name, "die")
        print('die:', sum(die))
        print()
        
        if sum(die) == 6:
            die = [0,0,0,0,0,0]
            target_num -= 1
        if sum(die) == 5 and burum:
            break
    
    king = -1
    for j in range(6):
        if die[j] == 0:
            king = Players[j]
            break
    if king.name == 'player':
        print('you are king')
    else:
        print(f'{king.name} is king')
    king.mode = 2
    
    #킬부르기
    kill = king.kill(giru, t[6])
    for i in Players[:]:
        if kill in i.deck:
            print(i.name, "killed")
            if i.name == 'player':
                print('game end')
                exit()
            print('(확인용)killed deck:', look((Deck(i.deck)).sorted_deck(giru)))
            li = i.deck
            li.extend(t[6])
            Players.remove(i)
    
    
    random.shuffle(li)
    for i in Players:
        if i == king:
            (giru, target_num) = king.grab(giru, target_num, li[-5:])
            for j in range(5):
                li.pop()
        else:
            for j in range(2):
                i.deck.append(li.pop())


    
    friend_call = king.choose_friend(giru)
    
    return (king, friend_call, giru, target_num)



king, friend_call, giru, target_num = gameready()

#프렌 반영
friend = -1
for j in range(5):
    if friend_call in Players[j].deck:
        friend = Players[j]
        break
if friend != -1:
    friend.mode = 1
    

#지금 상황 출력
print('#####################')
print('king:',f"{king.name}")
print('target number:', target_num)
print('giru:', look(giru))
print('friend_call:',look(friend_call))
print()

#player 역할 출력
player = Players[0]
if player.mode == 2:
    print('You are king')
elif player.mode == 1:
    print('You are friend')
else:
    print('You are rival')


#확인용
print('(확인용) king:', look(Deck(king.deck).sorted_deck(giru)))
#print('(확인용) friend:', look(Deck(friend.deck).sorted_deck(giru)))


def card_change(giru):#return (mighty, joker, jokercall)
    joker = 'joker'
    mighty = 'SA'
    jokercall = 'C3'
    if giru == 'S':
        mighty = 'DA'
    if giru == 'C':
        jokercall = 'S3'
    return (mighty, joker, jokercall)

def win_sort(giru, first_card_shape): #카드 강한 순서
    (mighty, joker, jokercall) = card_change(giru)
    li = []
    li.append(mighty)
    li.append(joker)
    li.extend(all_giru(giru))
    if first_card_shape == joker:
        return [mighty, joker]
    elif first_card_shape == giru:
        pass
    else:
        if first_card_shape == 'S':
            li.extend(spadelist)
        elif first_card_shape == 'H':
            li.extend(heartlist)
        elif first_card_shape == 'D':
            li.extend(diamondlist)
        else:
            li.extend(cloverlist)
    
    return li

def win(giru, round, put_li, leadshoot, call = 0): #카드 5장의 승패 정하기, call은 조커
    mighty, joker, jokercall = card_change(giru)
    if mighty in put_li:
        return mighty
    if (call == 1) or (round == 0) or (round == 9):
        if joker in put_li:
            put_li.remove(joker)
    if joker in put_li:
        return joker
    li = list((set(shapelist(giru))&set(put_li)))
    if len(li) == 0:
        for i in shapelist(leadshoot):
            if i in put_li:
                return i
    for i in shapelist(giru):
        if i in put_li:
            return i

def possible(giru, play_order, round, deck, leadshoot, call = 0): #낼 수 있는 카드
    mighty, joker, jokercall = card_change(giru)
    
    if play_order == 0: 
        if round == 0:
            li = deck[:]
            for i in deck:
                if i in shapelist(giru):
                    li.remove(i)
            if 'joker' in deck:
                li.remove('joker')
            return(li)
            
        else:
            return deck
    else:
        if call == 1:
            if 'joker' in deck:
                if mighty not in deck:
                    return ['joker']
                else:
                    return[mighty,joker]
        
        li = []
        for i in deck:
            if i in shapelist(leadshoot):
                li.append(i)
        if len(li) == 0:
            if round == 0:
                if joker not in deck:
                    return deck
                else:
                    for i in deck:
                        if i != joker:
                            li.append(i)
                    return li
            else:
                return deck
        else:
            for i in deck:
                if i == mighty:
                    li.append(i)
                elif (i == joker) and (round != 0):
                    li.append(i)
            return li



def gameplay(Players, giru, target_num,king,friend,friend_call): #(마지막에 할거)
    (mighty, joker, jokercall) = card_change(giru)
    start = Players.index(king)
    eatcard = {p: [] for p in Players}
    eatcard[king] = list(set(pick)&set(score_card))
    revealed = False
    
    used_card = []
    for i in range(10): #게임 진행
        round = i
        call = 0 #call기본값
        print()
        print('round:',round + 1)
        #print(eatcard)
        z = 0
        for k in eatcard.keys(): #먹은 카드 보여주기
            #print()
            z += 1
            if z < 5:
                print(k.position(revealed),':', len(eatcard[k]),end = ', ')
            else:
                print(k.position(revealed),':', len(eatcard[k]),end = '')
        print()
        
        li = [] #한 라운드 돌면서 나온 카드 저장할 리스트
        for j in range(5): #한 라운드 돌기
            play_order = j
            if j == 0: #처음 내는 사람
                
                put = Players[start].putcard(play_order, round, used_card) #카드내기
                used_card.append(put)
                #leadshoot 지정
                if put[0] == 'j': #조커처리
                    leadshoot = put[-1]
                    put = put[:-1]
                elif put[-1] in ['Y','N']: #조커콜처리
                    leadshoot = put[0]
                    call = 1
                    put = put[:-1]
                else:
                    leadshoot = put[0]
                
                
                li.append(put)
                print(Players[start].position(revealed),':',look(put))
                if put == friend_call:
                    print(f'{Players[start].name} friend!')
                    revealed = True
                used_card.append(put)
                
            else: #처음 아님: 리드슈트 따라 내기
                put = Players[start].putcard(play_order, round, used_card, leadshoot, call)
                
                li.append(put)
                print(Players[start].position(revealed),':', look(put))
                if put == friend_call: #프렌 밝혀질 경우
                    print(f'{Players[start].name} friend!')
                    revealed = True
                used_card.append(put)
            
            start = (start+1)%5 #다음사람
            
        #이긴 카드 확인
        win_card = win(giru, round, li, leadshoot, call)
        start += li.index(win_card)
        start %= 5
        print()
        print(Players[start].name,'win') #이긴사람 출력
        
        #이긴 사람한테 점카 먹여주기
        e = []
        for i in li:
            if i in score_card:
                eatcard[Players[start]].append(i)
                e.append(i)
        print(f'get {look(e)}')
    
    #게임 끝, 점수 세기
    print()
    print('##############')
    
    riv_point = 0 #야당 점수
    king_point = 0 #여당 점수
    for i in eatcard.keys():
        if i.mode == 0:
            riv_point += len(eatcard[i])
        else:
            king_point += len(eatcard[i])
    print('여당:',king_point)
    print('야당:',riv_point)
    print()
    if king_point >= target_num:
        if king_point == 20:
            print('Run!!')
        print('여당 승리')
        if Players[0].mode == 0:
            print('player lose!')
        else:
            print('player win!')
            
    else:
        if riv_point >= 10:
            print('Back Run!!')
        print('야당 승리')
        if Players[0].mode == 0:
            print('player win!')
        else:
            print('player lose!')
    
    print('game end')

gameplay(Players, giru, target_num,king,friend,friend_call)

