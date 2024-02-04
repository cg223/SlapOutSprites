###Class Definitions
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
class Sprite(object):
    def __init__(self, img_url, cx, cy, width, height, visible):
        self.sprite = Image(img_url, cx, cy, align='center', width=width, height=height, visible=visible)
        self.url = img_url
        
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
class Player(object):
    def __init__(self, x, y, width, height, player, wins):
        self.x = x
        self.y = y
        self.player = player
        
        self.width = width
        self.height = height
        self.health = 100
        self.stamina = 100
        self.stepsSinceAction = 0
        self.isBlocking = False
        self.isDashing = False
        self.framesToDash = 7
        self.dashFrames = 0
        self.dashTargetX = 0
        self.dashTargetY = 0
        
        self.currentSprite = None 
        self.currentSpriteState = None
        self.currentSpriteDirection = None
        self.walkAnimCounter = 0
        self.slapAnimCounter = 0
        self.knockAnimCounter = 0
        self.actionFinished = True
        self.isSlapping = False
        self.wins = wins
        
        self.hitBox = Oval(self.x, self.y, 35, 40, visible=False)
        self.slapRange = Circle(self.x, self.y, 50, visible=False)
        
        self.inputs = []
    
    def handleSpriteFrame(self, name, typeOfAnim, frame):
        # indexOfSpriteList = app.sprites[name].index(typeOfAnim) + 1 ### ITS GIVING A URL
        return game.playerSprites[self.player][name][game.playerSprites[self.player][name].index(typeOfAnim) + 1][frame]
    
    def stateMachine(self):
        self.currentSpriteState[1] = self.currentSpriteState[0][:4].lower() + self.currentSpriteDirection
        
        # possible to add other anims***
        match self.currentSpriteState[0]:
            case "Knoking":
                self.knockAnimCounter += 0.2
                if self.knockAnimCounter >= 2:
                    self.knockAnimCounter = 0
                    self.actionFinished = True
                    
                self.currentSprite.sprite.visible = False
                nextFrame = self.handleSpriteFrame(self.currentSpriteState[0], self.currentSpriteState[1], int(self.knockAnimCounter))
                nextFrame.sprite.centerX, nextFrame.sprite.centerY = self.currentSprite.sprite.centerX, self.currentSprite.sprite.centerY
                self.currentSprite = nextFrame
                self.currentSprite.sprite.visible = True
            case "Slapping":
                self.slapAnimCounter += 0.4
                if self.slapAnimCounter >= 4:
                    self.slapAnimCounter = 0
                    self.actionFinished = True
                    
                self.currentSprite.sprite.visible = False
                nextFrame = self.handleSpriteFrame(self.currentSpriteState[0], self.currentSpriteState[1], int(self.slapAnimCounter))
                nextFrame.sprite.centerX, nextFrame.sprite.centerY = self.currentSprite.sprite.centerX, self.currentSprite.sprite.centerY
                self.currentSprite = nextFrame
                self.currentSprite.sprite.visible = True
            case "Bloking":
                self.currentSprite.sprite.visible = False
                nextFrame = self.handleSpriteFrame(self.currentSpriteState[0], self.currentSpriteState[1], 0)
                nextFrame.sprite.centerX, nextFrame.sprite.centerY = self.currentSprite.sprite.centerX, self.currentSprite.sprite.centerY
                self.currentSprite = nextFrame
                self.currentSprite.centerX, self.currentSprite.centerY = self.x, self.y
                self.currentSprite.sprite.visible = True
            case "Walking":
                self.walkAnimCounter += 0.25
                if self.walkAnimCounter >= 4:
                    self.walkAnimCounter = 0
                self.currentSprite.sprite.visible = False
                nextFrame = self.handleSpriteFrame(self.currentSpriteState[0], self.currentSpriteState[1], int(self.walkAnimCounter))
                nextFrame.sprite.centerX, nextFrame.sprite.centerY = self.currentSprite.sprite.centerX, self.currentSprite.sprite.centerY
                self.currentSprite = nextFrame
                self.currentSprite.sprite.visible = True
            case "Idle":
                self.currentSprite.sprite.visible = False
                nextFrame = self.handleSpriteFrame(self.currentSpriteState[0], self.currentSpriteState[1], 0)
                nextFrame.sprite.centerX, nextFrame.sprite.centerY = self.currentSprite.sprite.centerX, self.currentSprite.sprite.centerY
                self.currentSprite = nextFrame
                self.currentSprite.centerX, self.currentSprite.centerY = self.x, self.y
                self.currentSprite.sprite.visible = True
            case _:
                pass

        
    def handleKeyHold(self, key):
        if key in self.actionKeys:
            if self.actionKeys[key] == 'BLOCK':
                self.attemptBlock()
        elif key in self.moveKeys.keys():
            if not self.isBlocking:
                if len(self.inputs) < 3:
                    self.inputs.append(key)
                    if self.actionFinished:
                        self.currentSpriteState[0] = "Walking" 
                        self.actionFinished = False
    
    def handleKeyPress(self, key):
        if key in self.actionKeys.keys():
            if not self.isBlocking:
                if self.actionKeys[key] == 'SLAP':
                    self.attemptSlap()
            
            if self.actionKeys[key] == 'DASH':
                if not self.isDashing:
                    self.attemptDash()
                
    def handleKeyRelease(self, key):
        if key in self.actionKeys.keys():
            if self.actionKeys[key] == 'BLOCK':
                self.actionFinished = True
                self.isBlocking = False
        
        if key in self.moveKeys.keys():
            if self.currentSpriteState[0] == "Walking":
                self.actionFinished = True
                
    def handleOnStep(self):
        if not game.stage.paused:
            if len(self.inputs) > 0:
                dx, dy = self.moveKeys[self.inputs[-1]]
                self.inputs.pop(0)
                self.attemptMove(dx, dy)
            
            angle = angleTo(self.currentSprite.sprite.centerX, self.currentSprite.sprite.centerY, self.opponent.x, self.opponent.y)
            if angle >= 0 and angle < 90:
                self.currentSpriteDirection = "BR"
                self.opponent.currentSprite.sprite.toFront()
                self.currentSprite.sprite.toFront()
            elif angle >= 90 and angle < 180:
                self.currentSpriteDirection = "FR"
                self.currentSprite.sprite.toFront()
                self.opponent.currentSprite.sprite.toFront()
            elif angle >= 180 and angle < 270:
                self.currentSpriteDirection = "FL"
                self.currentSprite.sprite.toFront()
                self.opponent.currentSprite.sprite.toFront()
            else:
                self.currentSpriteDirection = "BL"
                self.opponent.currentSprite.sprite.toFront()
                self.currentSprite.sprite.toFront()
                
            if self.actionFinished:
                self.currentSpriteState[0] = "Idle"
                

            self.stateMachine()
            
            self.stepsSinceAction += 1
            self.handleStamina()
            self.animateDash()
                
    
            if self.stamina > 0:
                if self.player == 'Player 1':
                    left = game.stage.p1Stamina.left
                    game.stage.p1Stamina.width = self.stamina/100 * 146
                    game.stage.p1Stamina.left = left
                    
                else:
                    right = game.stage.p2Stamina.right
                    game.stage.p2Stamina.width = self.stamina/100 * 146
                    game.stage.p2Stamina.right = right
                    
            if self.health > 0:
                if self.player == 'Player 1':
                    left = game.stage.p1Health.left
                    game.stage.p1Health.width = self.health/100 * 146
                    game.stage.p1Health.left = left
                    
                else:
                    right = game.stage.p2Health.right
                    game.stage.p2Health.width = self.health/100 * 146
                    game.stage.p2Health.right = right
            else:
                game.stage.endRound(self.opponent)
                
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.currentSprite.sprite.centerX += dx
        self.currentSprite.sprite.centerY += dy
        self.hitBox.centerX += dx
        self.hitBox.centerY += dy
        self.slapRange.centerX += dx
        self.slapRange.centerY += dy
        self.playWalkSound()
        
    def setOpponent(self, opponent):
        self.opponent = opponent
    
    def attemptMove(self, dx, dy):
        if not game.stage.paused:
            if self.currentSprite.sprite.left + dx >= 30 and self.currentSprite.sprite.right + dx <= 365 and self.currentSprite.sprite.bottom + dy >= 120 and self.currentSprite.sprite.bottom + dy <= 335:
                self.hitBox.centerX += dx
                self.hitBox.centerY += dy
                if not self.hitBox.hitsShape(self.opponent.hitBox):
                    self.move(dx, dy)
                else: # disables walking anim when colliding to op
                    if self.currentSpriteState[0] == "Walking":
                        self.actionFinished = True
                self.hitBox.centerX -= dx
                self.hitBox.centerY -= dy
            else: # disables walking anim when colliding to bound
                if self.currentSpriteState[0] == "Walking":
                    self.actionFinished = True
        
    def setKeys(self, keys, move):
        if move:
            self.moveKeys = keys
        else:
            self.actionKeys = keys
        
    def attemptSlap(self):
        self.playWooshSound()
        self.stamina -= 5
        if self.stamina < 0:
            self.stamina = 0
        if distance(self.hitBox.centerX, self.hitBox.centerY, self.opponent.hitBox.centerX, self.opponent.hitBox.centerY) < 50:
            if self.stamina > 0:
                if self.stepsSinceAction > 10:
                    self.actionFinished = False
                    self.currentSpriteState[0] = "Slapping"
                    self.slapAnimCounter = 0
                    base = 25
                    damage = base
                    if self.stamina > 0:
                        damage *= (self.stamina/100) * 0.9
                        if self.opponent.isBlocking:
                            damage *= 0.2
                        self.slap(damage)
                    else:
                        self.slap(0.5)
                        self.playTiredSound()
        self.stepsSinceAction = 0
            
    def slap(self, damage):
        self.playSlapSound()
        self.stamina -= 10
        self.opponent.knockback(8)
        self.knockback(4)
        self.opponent.health -= damage
        self.opponent.playHurtSound()
        
        self.opponent.currentSpriteState[0] = 'Knoking'
        self.opponent.actionFinished = False
        self.opponent.knockAnimCounter = 0
        
    def knockback(self, amount):
        angle = angleTo(self.opponent.x, self.opponent.y, self.x, self.y)
        newCx, newCy = getPointInDir(self.currentSprite.sprite.centerX, self.currentSprite.sprite.centerY, angle, amount)
        self.currentSprite.sprite.centerX = newCx
        self.currentSprite.sprite.centerY = newCy
        self.hitBox.centerX = newCx
        self.hitBox.centerY = newCy
        self.slapRange.centerX, self.slapRange.centerY = newCx, newCy
        
        if self.currentSprite.sprite.left < 30 or self.currentSprite.sprite.right > 365:
            self.currentSprite.sprite.centerX = self.x
            self.hitBox.centerX = self.x
            self.slapRange.centerX = self.x
        else:
            self.x = newCx
        
        if self.currentSprite.sprite.bottom > 335 or self.currentSprite.sprite.top < 120:
            self.currentSprite.sprite.centerY = self.y
            self.hitBox.centerY = self.y
            self.slapRange.centerY = self.y
        else:
            self.y = newCy
        
    def handleStamina(self):
        if self.stepsSinceAction > 30:
            self.stamina += (self.stepsSinceAction - 30) * 0.05
            if self.stamina > 100:
                self.stamina = 100
                
    def playHurtSound(self):
        choice(game.hurtSounds).play()
        
    def playSlapSound(self):
        choice(game.slapSounds).play()
        
    def playWalkSound(self):
        choice(game.walkSounds).play()
        
    def playTiredSound(self):
        choice(game.tiredSounds).play()
        
    def playWooshSound(self):
        choice(game.wooshSounds).play()
        
    def attemptBlock(self):
        if self.stamina > 0:
            self.currentSpriteState[0] = "Bloking" 
            self.actionFinished = False
            self.block()
        else:
            self.stepsSinceAction = 0
            self.actionFinished = True
            self.isBlocking = False
        
    
    def block(self):
        self.isBlocking = True
        if self.stepsSinceAction > 30:
            self.stepsSinceAction = 30
        self.stamina -= 0.5
        
    def attemptDash(self):
        if self.stamina > 50:
            self.dash()
        
    def dash(self):
        self.playWooshSound()
        self.stamina -= 25
        self.stepsSinceAction = 0
        self.isDashing = True
        angle = angleTo(self.opponent.x, self.opponent.y, self.x, self.y)
        self.dashTargetX, self.dashTargetY = getPointInDir(self.x, self.y, angle, 40)
        self.dashFrames = 0
    
    def animateDash(self):
        if self.isDashing:
            self.dashFrames += 1
            if self.dashFrames < self.framesToDash:
                dx = (self.dashTargetX - self.x) / 2
                dy = (self.dashTargetY - self.y) / 2
                self.currentSprite.sprite.centerX += dx
                self.currentSprite.sprite.centerY += dy
                if self.currentSprite.sprite.left < 30:
                    self.currentSprite.sprite.left = 30
                elif self.currentSprite.sprite.right > 365:
                    self.currentSprite.sprite.right = 365
                if self.currentSprite.sprite.bottom < 120:
                    self.currentSprite.sprite.bottom = 120
                elif self.currentSprite.sprite.bottom > 335:
                    self.currentSprite.sprite.bottom = 335
                self.x = self.currentSprite.sprite.centerX
                self.y = self.currentSprite.sprite.centerY
                self.hitBox.centerX = self.x
                self.hitBox.centerY = self.y
            else:
                self.isDashing = False
        
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
class GameState(object):
    def __init__(self):
        self.level = 'MENU'
        self.stage = StageState(self.level)
        self.load = False

        self.playerImageList = []
        self.playerSprites = {
            "Player 1" : {},
            "Player 2" : {},
        }
        
        # --- Player 1 ---
        self.initializeSprites(
            "Player 1",
            "Idle",
            ["idleFR", "idleFL", "idleBR", "idleBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player1FR.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1FLFix.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1BR.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1BL.png?raw=true"],
            ],
            )
        self.initializeSprites(
            "Player 1",
            "Walking",
            ["walkFR", "walkFL", "walkBR", "walkBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FRw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FRw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FRw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FRw_4.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FLw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FLw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FLw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1FLw_4.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BRw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BRw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BRw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BRw_4.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BLw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BLw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BLw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Walking/p1BLw_4.png?raw=true"],
            ],
            )
        self.initializeSprites(
            "Player 1",
            "Slapping",
            ["slapFR", "slapFL", "slapBR", "slapBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FRs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FRs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FRs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FRs_3.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FLs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FLs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FLs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1FLs_3.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BRs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BRs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BRs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BRs_3.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BLs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BLs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BLs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Slapping/p1BLs_3.png?raw=true"],
            ],
            )
        self.initializeSprites(
            "Player 1",
            "Bloking",
            ["blokFR", "blokFL", "blokBR", "blokBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player1Blocking/p1FRb.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Blocking/p1FLb.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Blocking/p1BRb.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Blocking/p1BLb.png?raw=true"],
            ],
            )
        
        self.initializeSprites(
            "Player 1",
            "Knoking",
            ["knokFR", "knokFL", "knokBR", "knokBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1FRk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1FRk_2.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1FLk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1FLk_2.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1BRk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1BRk_2.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1BLk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player1Knockback/p1BLk_2.png?raw=true"],
            ],
            )
        # --- Player 2 -----------------------------------------------------------------------------------------
        self.initializeSprites(
            "Player 2",
            "Idle",
            ["idleFR", "idleFL", "idleBR", "idleBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player2FR.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2FL.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2BR.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2BL.png?raw=true"],
            ],
            )
        self.initializeSprites(
            "Player 2",
            "Walking",
            ["walkFR", "walkFL", "walkBR", "walkBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FRw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FRw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FRw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FRw_4.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FLw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FLw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FLw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2FLw_4.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BRw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BRw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BRw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BRw_4.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BLw_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BLw_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BLw_3.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Walking/p2BLw_4.png?raw=true"],
            ],
            )
        self.initializeSprites(
            "Player 2",
            "Slapping",
            ["slapFR", "slapFL", "slapBR", "slapBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FRs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FRs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FRs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FRs_3.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FLs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FLs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FLs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2FLs_3.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BRs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BRs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BRs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BRs_3.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BLs_initial.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BLs_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BLs_2.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Slapping/p2BLs_3.png?raw=true"],
            ],
            )
        self.initializeSprites(
            "Player 2",
            "Bloking",
            ["blokFR", "blokFL", "blokBR", "blokBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player2Blocking/p2FRb.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Blocking/p2FLb.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Blocking/p2BRb.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Blocking/p2BLb.png?raw=true"],
            ],
            )
        
        self.initializeSprites(
            "Player 2",
            "Knoking",
            ["knokFR", "knokFL", "knokBR", "knokBL"],
            [["https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2FRk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2FRk_2.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2FLk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2FLk_2.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2BRk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2BRk_2.png?raw=true"],
            ["https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2BLk_1.png?raw=true", "https://github.com/cg223/SlapOutSprites/blob/main/player2Knockback/p2BLk_2.png?raw=true"],
            ],
            )
        # ---------------------------------------------------------
        self.initializeSounds()
        
    def initializeSounds(self):
        self.hurtSounds = [
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/hurt1..mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/hurt2.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/hurt3.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/hurt4.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/hurt5.mp3?raw=true'),
            ]
        self.slapSounds = [
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/slap1.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/slap2.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/slap3.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/slap4.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/slap5.mp3?raw=true'),
            ]
        self.walkSounds = [
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/walk1.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/walk2.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/walk3.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/walk4.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/walk5.mp3?raw=true'),
            ]
        self.tiredSounds = [
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/tired1.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/tired2.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/tired3.mp3?raw=true'),
            ]
        self.wooshSounds = [
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/woosh1.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/woosh2.mp3?raw=true'),
            Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/woosh3.mp3?raw=true'),
            ]
            
    def initializeSprites(self, player, name, animNameList, urlList, ):
        self.playerSprites[player][name] = []
        numOfItems = len(animNameList)
        
        for i in range(numOfItems):
            #turning url into sprites
            listOfCreatedSprites = []
            for url in urlList[i]:
                spriteCreated = Sprite(url, 1000, 1000, 60, 60, False)
                listOfCreatedSprites.append(spriteCreated)
                self.playerImageList.append(spriteCreated)
                
            self.playerSprites[player][name].append(animNameList[i])
            self.playerSprites[player][name].append(listOfCreatedSprites)

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
class StageState(object):
    def __init__(self, level):
        self.level = level
        self.drawing = []
        self.paused = True
        self.counting = False
        self.countdownSteps = 0
        self.sequencers = []
        self.isEnded = False
        self.isPlayingMusic = False
        self.defMenuMusic()
        
        self.round = 1
        self.roundsWon = [0, 0, 0]
        self.playerOneWins = 0
        self.playerTwoWins = 0

        if level == 'MENU':
            self.drawMenu()
        elif level == 'FIGHT':
            self.drawStage()
            self.counting = True
        elif level == 'TUTORIAL':
            self.drawTutorial()
    
    def addPlayers(self):
        # making sure all sprites are invisible before starting up 
        for img in game.playerImageList:
            img.sprite.visible = False
        # ----
        playerOneX = 100
        playerOneY = 100
        self.playerOne = Player(playerOneX, playerOneY, 60, 60, 'Player 1', self.playerOneWins)
        self.playerOne.currentSpriteState = ["Idle", "idleFR"]
        self.playerOne.currentSprite = self.playerOne.handleSpriteFrame(self.playerOne.currentSpriteState[0], self.playerOne.currentSpriteState[1], 0)
        self.playerOne.currentSprite.sprite.centerX, self.playerOne.currentSprite.sprite.centerY = playerOneX, playerOneY
        self.playerOne.currentSprite.sprite.visible = True
        self.playerOne.currentSprite.sprite.toFront()
        self.playerOne.setKeys({
            'a': (-5, 0),
            'd': (5, 0),
            'w': (0, -5),
            's': (0, 5),
        }, True)
        self.playerOne.setKeys({
            'c': 'SLAP',
            'v': 'BLOCK',
            'b': 'DASH',
        }, False)
        
        playerTwoX = 300
        playerTwoY = 300
        self.playerTwo = Player(playerTwoX, playerTwoY, 60, 60, 'Player 2', self.playerTwoWins)

        self.playerTwo.currentSpriteState = ["Idle", "idleBL"]
        self.playerTwo.currentSprite = self.playerTwo.handleSpriteFrame(self.playerTwo.currentSpriteState[0], self.playerTwo.currentSpriteState[1], 0)
        self.playerTwo.currentSprite.sprite.centerX, self.playerTwo.currentSprite.sprite.centerY = playerTwoX, playerTwoY
        self.playerTwo.currentSprite.sprite.visible = True
        self.playerTwo.currentSprite.sprite.toFront()
        
        self.playerTwo.setKeys({
            'left': (-5, 0),
            'right': (5, 0),
            'up': (0, -5),
            'down': (0, 5),
        }, True)
        self.playerTwo.setKeys({
            '/': 'SLAP',
            '.': 'BLOCK',
            ',': 'DASH',
        }, False)
        
        self.playerOne.setOpponent(self.playerTwo)
        self.playerTwo.setOpponent(self.playerOne)
        
        self.drawing.append(self.playerOne.currentSprite.sprite)
        self.drawing.append(self.playerTwo.currentSprite.sprite)
    
    def drawMenu(self):
        app.background = 'dimGray'
        self.logo = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/SlapOutLogo.png?raw=true', 200, 80, 370, 108.225, True)
        self.playButton = Rect(50, 160, 300, 90, fill='darkGray', border='black')
        self.playText = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/PlayText.png?raw=true', 200, 205, 140, 70, True)
        self.tutorialButton = Rect(50, 260, 300, 90, fill='darkGray', border='black', visible = True)
        self.tutorialText = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/TutorialText.png?raw=true', 200, 305, 283, 70, True)

        self.drawing.append(self.logo.sprite)
        self.drawing.append(self.playButton)
        self.drawing.append(self.tutorialButton)
        self.drawing.append(self.playText.sprite)
        self.drawing.append(self.tutorialText.sprite)
        
    def drawStage(self):
        app.background = gradient('darkSlateGray', 'black')
        self.ring = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/SlapOutRingFkx.png?raw=true', 200, 175, 445, 375, True)
        self.drawing.append(self.ring.sprite)
        self.drawUI()
        self.addPlayers()
        
    def drawUI(self):
        self.p1HealthBar = Rect(50, 16, 150, 20, fill='darkGray', border='black')
        self.p1Health = Rect(52, 18, 146, 16, fill=gradient('limeGreen', 'lime', start='left'))
        self.p1StaminaBar = Rect(50, 36, 150, 12, fill='darkGray', border='black')
        self.p1Stamina = Rect(52, 38, 146, 8, fill=gradient('darkOrange', 'orange', start='left'))
        self.p1Circle = Circle(30, 30, 30, fill=gradient('darkGray', 'gray'))
        self.p1Icon = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/player1Icon.png?raw=true', 30, 30, 60, 60, True)
        self.p1Border = Circle(30, 30, 30, fill=None, border='black', borderWidth=3)
        
        self.p2HealthBar = Rect(200, 16, 150, 20, fill='darkGray', border='black')
        self.p2Health = Rect(202, 18, 146, 16, fill=gradient('limeGreen', 'lime', start='right'))
        self.p2StaminaBar = Rect(200, 36, 150, 12, fill='darkGray', border='black')
        self.p2Stamina = Rect(202, 38, 146, 8, fill=gradient('darkOrange', 'orange', start='right'))
        self.p2Circle = Circle(370, 30, 30, fill=gradient('darkGray', 'gray'))
        self.p2Icon = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/player2Icon.png?raw=true', 370, 30, 60, 60, True)
        self.p2Border = Circle(370, 30, 30, fill=None, border='black', borderWidth=3)
        
        self.roundVisuals = Group(
            Circle(160, 375, 18, fill = 'darkSlateGray', border = 'black', opacity = 100),
            Circle(200, 375, 18, fill = 'darkSlateGray', border = 'black', opacity = 100),
            Circle(240, 375, 18, fill = 'darkSlateGray', border = 'black', opacity = 100),
            )
        
        for i in range(len(self.roundsWon)):
            if self.roundsWon[i] == 1:
                self.roundVisuals.children[i].fill = 'lime'
            elif self.roundsWon[i] == 2:
                self.roundVisuals.children[i].fill = 'orange'
        
        self.drawing.append(self.roundVisuals)
        
        self.drawing.append(self.p1HealthBar)
        self.drawing.append(self.p1Health)
        self.drawing.append(self.p1StaminaBar)
        self.drawing.append(self.p1Stamina)
        self.drawing.append(self.p1Circle)
        self.drawing.append(self.p1Icon.sprite)
        self.drawing.append(self.p1Border)
        
        self.drawing.append(self.p2HealthBar)
        self.drawing.append(self.p2Health)
        self.drawing.append(self.p2StaminaBar)
        self.drawing.append(self.p2Stamina)
        self.drawing.append(self.p2Circle)
        self.drawing.append(self.p2Icon.sprite)
        self.drawing.append(self.p2Border)
        
    def drawTutorial(self):
        self.playerOneInfo = Group(
            Label("-Player 1 Controls-", 90, 30, font = 'orbitron', bold = True, fill = 'white', border = 'black', borderWidth = 0.5, size = 16),
            Label("LEFT----[a]", 90, 60, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("RIGHT---[d]", 90, 90, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("UP------[w]", 90, 120, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("DOWN----[s]", 90, 150, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("SLAP----[c]", 90, 180, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("BLOCK---[v]", 90, 210, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("DODGE---[b]", 90, 240, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            )
        self.playerTwoInfo = Group(
            Label("-Player 2 Controls-", 310, 30, font = 'orbitron', bold = True, fill = 'white', border = 'black', borderWidth = 0.5, size = 16),
            Label("LEFT----[larrow]", 310, 60, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("RIGHT---[rarrow]", 310, 90, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("UP------[uarrow]", 310, 120, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("DOWN----[darrow]", 310, 150, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("SLAP----[/]", 310, 180, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("BLOCK---[period]", 310, 210, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            Label("DODGE---[coma]", 310, 240, font = 'orbitron', bold = True, fill = 'orange', border = 'black', borderWidth = 0.5, size = 15),
            )
        self.guideSprites = Group(
            Image("https://github.com/cg223/SlapOutSprites/blob/main/SlapInstruction.png?raw=true", 75, 340, align = 'center', width = 110, height = 65),
            Image("https://github.com/cg223/SlapOutSprites/blob/main/BlockInstruction.png?raw=true", 200, 340, align = 'center', width = 110, height = 65),
            Image("https://github.com/cg223/SlapOutSprites/blob/main/DashInstruction.png?raw=true", 325, 340, align = 'center', width = 110, height = 65),
            )
            
        self.backButton = Rect(200, 80, 50, 50,align = 'center', fill='darkSlateGray', border='black')
        self.backLabel = Label("<", 200, 80, fill='white', bold=True, size=30)
        
        self.drawing.append(self.backButton)
        self.drawing.append(self.backLabel)
        for item in self.playerOneInfo:
            self.drawing.append(item)
        for item in self.playerTwoInfo:
            self.drawing.append(item)
        for item in self.guideSprites:
            self.drawing.append(item)
        
    def clear(self):
        for item in self.drawing:
            app.group.remove(item)
        # for visual in self.roundVisuals:
        #     app.group.remove(visual)
            
    def drawLoadingScreen(self):
        # tips = [
        #     'The less stamina you have, the less damage you do!',
        #     'Slappers train their entire lives for competitions',
        #     'There are over 1000 slapping leagues in slapville!',
        #     '\"A great is slapper is one who never gets slapped\" -somebody',
        #     'Slapping is the most effecient form of exercise!',
        #     'Did you know it takes 23,034 slaps to cook a piece of chicken?',
        #     'Pretty cool sprite implementation am i right?',
        #     'Slap and Stone!',
        #     'Hire Protography for all your photography needs!',
        #     'Turn the volume up to listen to the epik sounds!',
        #     'Sticks & Stones may break my bones, but slaps will hurt more.',
        #     'Did you know this game\'s code is under 1000 lines?'
        #     ]
        tips = [
            'The less stamina you have, the less damage you do!',
            'You can hold your block, but it doesn\'t last forever!',
            'A good dodger = God-like performance!',
            '\"A great is slapper is one who never gets slapped\" -somebody',
            'Hire Protography for all your photography needs!',
            'Turn the volume up to listen to the epik sounds!',
            ]
        
        self.loadingScreen = Rect(0, 0, 400, 400, fill=gradient('slateGray', 'darkSlateGray'))
        self.loadingLogo = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/SlapOutLogo.png?raw=true', 200, 80, 370, 108.225, True)
        self.loadingBar = Rect(10, 300, 380, 50, fill='slateGray', border='darkGray')
        self.progressBar = Rect(10, 300, 1, 50, fill='white')
        self.tip = Label(choice(tips), 200, 270, fill='white', bold=True, size=1)
        while(self.tip.right < self.loadingBar.right):
            self.tip.size += 1
        self.tip.size -= 1
        self.tip.bottom = 290
        
    def removeLoadingScreen(self):
        app.group.remove(self.loadingScreen)
        app.group.remove(self.loadingLogo.sprite)
        app.group.remove(self.loadingBar)
        app.group.remove(self.progressBar)
        app.group.remove(self.tip)
        
    def moveProgressBar(self, amount):
        left = self.progressBar.left
        self.progressBar.width += amount
        self.progressBar.left = left
        
    def endRound(self, player):
        if "1" in player.player:
            self.roundsWon[self.round-1] = 1
            self.playerOneWins += 1
        else:
            self.roundsWon[self.round-1] = 2
            self.playerTwoWins += 1
            
        self.round += 1
        player.wins += 1
        
        if player.wins >= 2:
            self.win(player)
        else:
            self.resetRound()
    
    def resetRound(self):
        self.clear()
        self.drawStage()
        self.paused = True
        self.countdownSteps = 0
        self.countdown()
    
    def win(self, winner):
        self.isEnded = True
        app.background = 'slateGray'
        self.clear()
        # self.clearRoundVisuals()
        self.paused = True
        winLogo = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/SlapOutLogo.png?raw=true', 200, 80, 370, 108.225, True)
        winner.opponent.currentSprite.sprite.visible = False
        
        winner.currentSpriteState = ["Idle", "idleFR"]
        winner.currentSprite.sprite.visible = False
        winner.currentSprite = winner.handleSpriteFrame(winner.currentSpriteState[0], winner.currentSpriteState[1], 0)
        winner.currentSprite.sprite.visible = True
        winner.currentSprite.sprite.centerX, winner.currentSprite.sprite.centerY = 200, 170
        
        winLabel1 = Label('Ladies and Gentleman,', 200, 220, size=30, fill='white', bold=True)
        winLabel2 = Label('we have a new champion!', 200, 250, size=30, fill='white', bold=True)
        winLabel3 = Label(f'{winner.player} wins!', 200, 290, size=30, fill='white', bold=True)
        
        self.resetButton = Rect(50, 320, 300, 50, fill='darkSlateGray', border='black')
        resetLabel = Label('RESTART', 200, 345, size=30, fill='white', bold=True, font='orbitron')
        
        #-----
        self.drawing.append(winLogo.sprite)
        self.drawing.append(winLabel1)
        self.drawing.append(winLabel2)
        self.drawing.append(winLabel3)
        self.drawing.append(resetLabel)
        self.drawing.append(self.resetButton)
        
    def reset(self):
        self.clear()
        
        game.level = "MENU"
        game.stage = StageState(game.level)
 
        
    def countdown(self):
        three = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/3.png?raw=true', 200, 200, 150, 286, False)
        two   = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/2.png?raw=true', 200, 200, 150, 286, False)
        one   = Sprite('https://github.com/cg223/SlapOutSprites/blob/main/1.png?raw=true', 200, 200, 150, 286, False)
        
        self.roundSprites = {
            1: Sprite('https://github.com/cg223/SlapOutSprites/blob/main/Rounds/Round%201.png?raw=true', 200, 200, 340, 150, False),
            2: Sprite('https://github.com/cg223/SlapOutSprites/blob/main/Rounds/Round%202.png?raw=true', 200, 200, 340, 150, False),
            3: Sprite('https://github.com/cg223/SlapOutSprites/blob/main/Rounds/Round%203.png?raw=true', 200, 200, 340, 150, False),
        }
        
        self.numSprites = {
            0: self.roundSprites,
            1: one,
            2: two,
            3: three,
        }
        
        self.num = 3
        self.counting = True
        
    def handleOnStep(self):
        if self.counting:
            if self.countdownSteps == 0:
                self.numSprites[self.num].sprite.visible = True
                self.numSprites[self.num].sprite.toFront()
            
            elif self.countdownSteps % 30 == 0:
                self.num -= 1
                
                if self.num in self.numSprites:
                    if self.num == 0:
                        self.numSprites[self.num][self.round].sprite.visible = True
                    else:
                        self.numSprites[self.num].sprite.visible = True
                        self.numSprites[self.num].sprite.toFront()
                        
                else:
                    self.counting = False
                    self.paused = False
                    
                
                if self.num == -1:
                    self.numSprites[0][self.round].sprite.visible = False
                else:
                    self.numSprites[self.num+1].sprite.visible = False
                    
            self.countdownSteps += 1
            
    def defMenuMusic(self):
        self.menuMusic = Sound('https://github.com/cg223/SlapOutSprites/blob/main/sounds/Slap%20Happy%20Riddim%20-%20Konrad%20OldMoney.mp3?raw=true')
    
    def playMenuMusic(self):
        self.menuMusic.play(restart=True)
        self.isPlayingMusic = True
        
    def stopMenuMusic(self):
        self.menuMusic.pause()
        self.isPlayingMusic = False
        
game = GameState()

###--------------------------------------------------------------------------------------------
###Event Functions
def onStep():
    if not game.stage.paused:
        if game.stage.playerOne != None:
            game.stage.playerOne.handleOnStep()
            game.stage.playerTwo.handleOnStep()
            
    game.stage.handleOnStep()
        
def onKeyHold(keys):
    if not game.stage.paused:
        for key in keys:
            if game.stage.playerOne != None:
                game.stage.playerOne.handleKeyHold(key)
                game.stage.playerTwo.handleKeyHold(key)
            
def onKeyPress(key):
    if game.level == 'FIGHT':
        if game.stage.playerOne != None:
            if not game.stage.paused:
                game.stage.playerOne.handleKeyPress(key)
                game.stage.playerTwo.handleKeyPress(key)
        
def onKeyRelease(key):
    if game.level == 'FIGHT':
        if game.stage.playerOne != None:
            if not game.stage.paused:
                game.stage.playerOne.handleKeyRelease(key)
                game.stage.playerTwo.handleKeyRelease(key)
        
def onMousePress(mouseX, mouseY):
    if game.level == 'MENU':
        if game.stage.playButton.contains(mouseX, mouseY):
            game.stage.stopMenuMusic()
            game.level = 'FIGHT'
            game.stage.clear()
            game.stage = StageState(game.level)
            
            if game.load:
                game.stage.drawLoadingScreen()
                while(game.stage.progressBar.width < 380):
                    game.stage.moveProgressBar(randrange(15, 55))
                    if game.stage.progressBar.width > 380:
                        game.stage.progressBar.width = 380
                    sleep(randrange(1, 6)/10)
            
                sleep(1)
                game.stage.removeLoadingScreen()
            
            game.stage.countdown()
            game.stage.countdownSteps = 0
            
        elif game.stage.tutorialButton.contains(mouseX, mouseY):
            game.level = 'TUTORIAL'
            game.stage.clear()
            game.stage = StageState(game.level)
    
    if game.stage.isEnded:
        if game.stage.resetButton.contains(mouseX, mouseY):
            game.stage.playerOne.currentSprite.sprite.visible = False
            game.stage.playerTwo.currentSprite.sprite.visible = False
            game.stage.reset()
    
    if game.level == "TUTORIAL":
        if game.stage.backButton.contains(mouseX, mouseY):
            game.level = "MENU"
            # ^ wouldnt you just call game.stage.clear()?
            for item in game.stage.playerOneInfo:
                item.visible = False
            for item in game.stage.playerTwoInfo:
                item.visible = False
            for item in game.stage.guideSprites:
                item.visible = False
            game.stage.backButton.visible = False
            
            game.stage.drawMenu()
