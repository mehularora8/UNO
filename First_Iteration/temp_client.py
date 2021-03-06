import pygame
from network import Network
import pickle
from Cards import Card, cards

pygame.init()

width = 800
height = 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("UNO Client")

clientNumber = 0

class Button:
    def __init__(self, text, color, x, y):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.width = 150
        self.height = 80

    def draw(self, win):
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Merriweather", 40)
        text = font.render(str(self.card.number), 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

class OnScreenCard:
    def __init__(self, card: Card, x, y):
        self.card = card
        self.x = x
        self.y = y
        self.width = 80
        self.height = 140

    def draw(self, win):
        pygame.draw.rect(win, self.card.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Merriweather", 40)
        text = font.render(str(self.card.number), 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

onScreenCards = list()

def redrawWindow(win, game, player):
    global onScreenCards

    win.fill((255,255,255))

    #Draw topmost card
    topCard = OnScreenCard(game.lastMove, 500, 500)
    topCard.draw(win)

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (int(width/2 - text.get_width()/2), int(height/2 - text.get_height()/2)))

        

    else:
        if game.turn == player:
            #Our turn
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Your Move", 1, (0, 255,255))
            win.blit(text, (50, 50))

        else:

            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Opponent\'s Move", 1, (0, 255,255))
            win.blit(text, (50, 50))

        # Draw all cards

        XPosition = 100
        YPosition = 200

        updatedCards = []

        cardsToDraw = []
        
        if player == 0:
            cardsToDraw = game.p1Cards
        else:
            cardsToDraw = game.p2Cards

        for playableCard in cardsToDraw:
            nextCard = OnScreenCard(playableCard, XPosition, YPosition)
            XPosition += 100
            nextCard.draw(win)
            updatedCards.append(nextCard)



        onScreenCards = updatedCards


    pygame.display.update()


def checkMove(move: Card, game) -> bool:
    """
    Checks if the last move was valid and returns a bool
    """
    print("Checking move")
    lastMove = game.lastMove

    if move.number == lastMove.number:
        return True

    elif move.color == lastMove.color: 
        return True

    elif move.wild: 
        return True

    return False


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getPlayerNumber()
    global onScreenCards

    while run:
        clock.tick(60)
        try:
            game = n.send("get", "C")
        except:
            run = False
            print("Connection lost.")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Only handle this event if the player is on turn.
                if game.turn == player:
                    pos = pygame.mouse.get_pos()
                    for drawnCard in onScreenCards:
                        if drawnCard.click(pos) and game.connected():
                            if checkMove(drawnCard.card, game):
                                n.send("move", "C")
                                print(drawnCard.card)
                                n.send(drawnCard.card, "M")
                                # Send move

        redrawWindow(window, game, player)

main()