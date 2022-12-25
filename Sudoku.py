import os
import random as rand
import math
import copy
import itertools
from cmu_graphics import *

# from https://www.cs.cmu.edu/~112-3/notes/term-project.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# from https://www.cs.cmu.edu/~112-3/notes/term-project.html
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

boards = [[],[],[],[],[],[]]

def formatBoard(file):
    board = [[],[],[],[],[],[],[],[],[]]
    row = 0
    col = 0
    for element in file:
        if element in {'0','1','2','3','4','5','6','7','8','9'}:
            board[row].append(element)
            col += 1
            if col == 9:
                row += 1
                col = 0
    for row in range(9):
        while len(board[row]) != 9:
            board[row].append('0')
    return board

#from https://www.cs.cmu.edu/~112-3/notes/term-project.html
for filename in os.listdir('boards'):
    if filename.endswith('.txt') and not filename.endswith('solution.txt'):
        pathToFile = f'boards/{filename}'
        fileContents = readFile(pathToFile)
        newBoard = formatBoard(fileContents)
        if filename.startswith('easy'):
            boards[0].append(newBoard)
        elif filename.startswith('medium'):
            boards[1].append(newBoard)
        elif filename.startswith('hard'):
            boards[2].append(newBoard)
        elif filename.startswith('expert'):
            boards[3].append(newBoard)
        elif filename.startswith('evil'):
            boards[4].append(newBoard)
        elif filename.startswith('sc5a'):
            boards[5].append(newBoard)

#Splash Screen
def splash_onScreenStart(app):
    pass

def splash_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='lavender')
    drawLabel('S U D O K U',app.width/2,app.height/2-150,fill='darkSlateBlue',size=60,font = 'monospace',bold=True)
    drawLabel('PLAY',app.width/2,app.height/2+100,size=30)
    drawLabel('HELP',app.width/2,app.height/2+150,size=30)
    
def splash_onMousePress(app,mouseX,mouseY):
    if 350<=mouseX<=450 and 462<=mouseY<=484:
        setActiveScreen('play')
    elif 350<mouseX<=450 and 512<=mouseY<=534:
        setActiveScreen('help')

#Help Screen
def help_onScreenStart(app):
    pass

def help_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='lavender')
    drawRect(200,100,400,500,fill='white')
    drawLabel('HOW TO PLAY',220,120,size=25,align='left-top',font='serif')
    #Instructions from https://www.nytimes.com/puzzles/sudoku/easy
    drawLabel('Fill the grid with your keyboard so that every row, column',220,160,size=14,align='left-top')
    drawLabel('and 3×3 box contains the 3×3 box contains the digits 1',220,180,size=14,align='left-top')
    drawLabel('to 9, without repeating.',220,200,size=14,align='left-top')
    drawLabel('Use Normal Mode to enter numbers you are confident',220,240,align='left-top',size=14)
    drawLabel('about. Use Candidate Mode to add or remove multiple',220,260,align='left-top',size=14)
    drawLabel('possibilities for a square.',220,280,align='left-top',size=14)
    drawLabel('The Hint button will highlight or play the next logical',220,320,align='left-top',size=14)
    drawLabel('square to solve that is empty',220,340,align='left-top',size=14)
    drawLabel('CONTROLS',220,380,size=25,align='left-top',font='serif')
    drawLabel('Toggle Auto-Candidate: m',220,420,size=14,align='left-top')
    drawLabel('Toggle Normal/Candidate Mode: l',220,440,size=14,align='left-top')
    drawLabel('Get Hint: h',220,460,size=14,align='left-top')
    drawLabel('Play Hint: p',220,480,size=14,align='left-top')
    drawLabel('Play Singleton: s',220,500,size=14,align='left-top')
    drawLabel('Undo: u',220,520,size=14,align='left-top')
    drawLabel('Redo: r',220,540,size=14,align='left-top')
    drawLabel('BACK TO HOMEPAGE',100,39,size=10,)
    drawRect(355,580,90,40,fill='mediumSlateBlue')
    drawLabel('PLAY',app.width/2,600,size=30,bold=True)

def help_onMousePress(app,mouseX,mouseY):
    if 45<=mouseX<=157 and 33<=mouseY<=43:
        setActiveScreen('splash')
    elif 355<=mouseX<=445 and 580<=mouseY<=620:
        setActiveScreen('play')

#settings screen
def settings_onScreenStart(app):
    app.highlightConflicts = True
    app.clock = True
    app.showLegals = True
    app.theme = 'basic'
    app.givenCol = 'lightGray'
    app.selectedCol = 'lightYellow'

def settings_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='lavender')
    drawRect(200,150,400,400,fill='white')
    drawLabel('x',580,170,size=20)
    drawLabel('Settings',220,170,align='top-left',size=35,font='serif')
    drawLabel('Highlight conflicts',245,220,align='top-left',size=16)
    if app.highlightConflicts:
        drawRect(220,220,12,12,fill='purple',border='black')
    else:
        drawRect(220,220,12,12,fill=None,border='black')
    drawLabel('Show clock',245,250,align='top-left',size=16)
    if app.clock:
        drawRect(220,250,12,12,fill='purple',border='black')
    else:
        drawRect(220,250,12,12,fill=None,border='black')
    drawLabel('Show candidates',245,280,align='top-left',size=16)
    if app.showLegals:
        drawRect(220,280,12,12,fill='purple',border='black')
    else:
        drawRect(220,280,12,12,fill=None,border='black')
    drawLabel('Themes',220,330,font='serif',size=35,align='top-left')
    drawLabel('Basic',245,380,size=16,align='top-left')
    if app.theme == 'basic':
        drawRect(220,380,12,12,fill='purple',border='black')
    else:
        drawRect(220,380,12,12,fill=None,border='black')
    drawLabel('Purple',245,410,size=16,align='top-left')
    if app.theme == 'purple':
        drawRect(220,410,12,12,fill='purple',border='black')
    else:
        drawRect(220,410,12,12,fill=None,border='black')
    drawLabel('Watermelon',245,440,size=16,align='top-left')
    if app.theme == 'watermelon':
        drawRect(220,440,12,12,fill='purple',border='black')
    else:
        drawRect(220,440,12,12,fill=None,border='black')

def settings_onMousePress(app,mouseX,mouseY):
    print(mouseX,mouseY)
    if 572<=mouseX<=589 and 164<=mouseY<=175:
        setActiveScreen('play')
    elif 220<=mouseX<=232 and 220<=mouseY<=232:
        app.highlightConflicts = not app.highlightConflicts
    elif 220<=mouseX<=232 and 250<=mouseY<=262:
        app.clock = not app.clock
    elif 220<=mouseX<=232 and 280<=mouseY<=292:
        app.showLegals = not app.showLegals
    elif 220<=mouseX<=232 and 380<=mouseY<=392:
        app.theme = 'basic'
    elif 220<=mouseX<=232 and 410<=mouseY<=422:
        app.theme = 'purple'
    elif 220<=mouseX<=232 and 440<=mouseY<=452:
        app.theme = 'watermelon'
    if app.theme == 'basic':
        app.givenCol = 'lightGray'
        app.selectedCol = 'lemonChiffon'
    elif app.theme == 'purple':
        app.givenCol = 'ghostWhite'
        app.selectedCol = 'thistle'
    elif app.theme == 'watermelon':
        app.givenCol = 'pink'
        app.selectedCol = 'darkSeaGreen'

#State Class
class State:
    emptyLegals = [[],[],[],[],[],[],[],[],[]]
    for row in range(9):
            for i in range(9):
                emptyLegals[row].append(set())
    fullLegals = [[],[],[],[],[],[],[],[],[]]
    for row in range(9):
            for i in range(9):
                fullLegals[row].append({'1','2','3','4','5','6','7','8','9'})
    def __init__(self,board):
        self.board = board
        self.legals = copy.deepcopy(State.emptyLegals)
        self.manualLegals = copy.deepcopy(State.emptyLegals)
        self.startLegals = copy.deepcopy(State.fullLegals)
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != '0':
                    self.startLegals[row][col] = set()
        self.bannedLegals = []
    def set(self,row,col,value):
        self.board[row][col] = value
    def updateLegals(self):
        self.legals = copy.deepcopy(self.startLegals)
        for row in range(9):
            for col in range(9):
                self.ban(row,col,self.board[row][col])
                if self.board[row][col] != '0':
                    self.legals[row][col] = set()
        for (row,col,val) in self.bannedLegals:
            if val in self.legals[row][col]:
                self.legals[row][col].remove(val)
    def ban(self,row,col,value):
        for colVal in range(9):
            if value in self.legals[row][colVal]:
                self.legals[row][colVal].remove(value)
        for rowVal in range(9):
            if value in self.legals[rowVal][col]:
                self.legals[rowVal][col].remove(value)
        rowsec = row//3
        colsec = col//3
        for i in range(3):
            for j in range(3):
                if value in self.legals[rowsec*3+i][colsec*3+j]:
                    self.legals[rowsec*3+i][colsec*3+j].remove(value)
    def banLegal(self,row,col,val):
        if val in self.legals[row][col]:
            self.legals[row][col].remove(val)
            self.bannedLegals.append((row,col,val))
        
#Play Screen
def play_onScreenStart(app):
    app.regions = []
    for i in range(27):
        app.regions.append([])
    for row in range(9):
        for col in range(9):
            app.regions[row].append((row,col))
            app.regions[col+9].append((row,col))
    for row in range(3):
        for col in range(3):
            for i in range(3):
                for j in range(3):
                    app.regions[18+row*3+col].append((row*3+i,col*3+j))
    app.competition = False
    app.difficulty = 0
    app.boardNum = None
    setUpBoard(app)
    newBoard(app)
    setUpClickBoard(app)
    app.setDifficulty = False
    app.setUserNewBoard = False 
    app.manual = True
    app.stepsPerSecond = 1
    app.timer = 0

def play_onStep(app):
    if not app.won:
        app.timer += 1

def setUpBoard(app):
    app.rows = 9
    app.cols = 9
    app.boardWidth = 500
    app.boardHeight = 500
    app.boardLeft = 50
    app.boardTop = 150
    app.cellBorderWidth = 1
    app.levels = ('Easy','Medium','Hard','Expert','Evil')

def setUpClickBoard(app):
    app.clickRows = 3
    app.clickCols = 3
    app.clickBoardLeft = 590
    app.clickBoardWidth = app.boardWidth/3
    app.clickBoardHeight = app.boardHeight/3
    app.clickBoardTop = app.boardTop+50
    app.clickCellBorderWidth = 1.5
    app.clickBoard = [[1,2,3],[4,5,6],[7,8,9]]
    app.clickSelection = None

def newBoard(app):
    app.timer = 0
    app.setUserNewBoard = False
    app.setHint = False
    app.hintCells = None
    app.moveCounter = -1
    app.movesMade = []
    app.illegal = []
    app.won = False
    app.lost = False
    app.noSingletons = False
    app.boardNum = rand.randrange(0,len(boards[app.difficulty]))
    if app.competition:
        app.givenBoard = boards[5][0]
    else:
        app.givenBoard = boards[app.difficulty][app.boardNum]
    app.userBoard = State(copy.deepcopy(app.givenBoard))
    app.selection = None
    app.legalMode = False
    if app.difficulty == 0:
        app.manual = True
    else:
        app.manual = False
    app.userBoard.updateLegals()
    app.solvedBoard = State(copy.deepcopy(app.givenBoard))
    app.solvedBoard.updateLegals()
    solveBoard(app)

def userNewBoard(app):
    app.timer = 0
    app.setHint = False
    app.hintCells = None
    app.moveCounter = -1
    app.movesMade = []
    app.illegal = []
    app.noSingletons = False
    app.won = False
    app.givenBoard = [['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0']]
    app.userBoard = State(copy.deepcopy(app.givenBoard))
    app.selection = None
    app.preventSetting = False
    app.manual = True
    app.legalMode = False

def solveBoard(app):
    if findCellWithFewestLegals(app) == None:
        return True
    else:
        partialSolve(app)
        (row,col) = findCellWithFewestLegals(app)
        for i in app.solvedBoard.legals[row][col]:
            if isValidInput(app,row,col,i):
                app.solvedBoard.board[row][col] = i
                if solveBoard(app) != None:
                    app.solvedBoard.updateLegals()
                    return solveBoard(app)
                else:
                    app.solvedBoard.board[row][col] = '0'
        return None

        
def isValidInput(app,row,col,val):
    if val in app.solvedBoard.board[row]:
        return False
    for i in range(9):
        if app.solvedBoard.board[i][col] == val:
            return False
    rowsec = row//3
    colsec = col//3
    for i in range(3):
        for j in range(3):
            if app.solvedBoard.board[rowsec*3+i][colsec*3+j] == val:
                return False
    return True

def partialSolve(app):
    for region in app.regions:
        secTracker = dict()
        for cell in region:
            if len(app.solvedBoard.legals[cell[0]][cell[1]]) == 1:
                app.solvedBoard.board[cell[0]][cell[1]] = sorted(app.solvedBoard.legals[cell[0]][cell[1]])[0]
            for legal in app.solvedBoard.legals[cell[0]][cell[1]]:
                if legal not in secTracker:
                    secTracker[legal] = {(cell[0],cell[1])}
                else:
                    secTracker[legal].add((cell[0],cell[1]))
        for key in secTracker:
            if len(secTracker[key]) == 1:
                row = sorted(secTracker[key])[0][0]
                col = sorted(secTracker[key])[0][1]
                app.solvedBoard.board[row][col] = key

def findCellWithFewestLegals(app):
    fewestLegals = 10
    cell = (None,None)
    for row in range(9):
        for col in range(9):
            if (app.solvedBoard.board[row][col] == '0' and 
            len(app.solvedBoard.legals[row][col]) < fewestLegals):
                cell = (row,col)
                fewestLegals = len(app.solvedBoard.legals[row][col])
    if cell == (None,None):
        return None
    else:
        return cell

def uniqueNewBoard(app):
    contents = app.getTextInput('Enter Numbers Here:')
    fileName = app.getTextInput('Name your board:')
    writeFile(f'boards/{fileName}.txt', contents)
    app.givenBoard = formatBoard(contents)

def play_redrawAll(app):
    drawBoard(app)
    drawBlockBorder(app)
    drawBoardBorder(app)
    drawNumbers(app)
    drawClickBoard(app)
    drawClickBoardBorder(app)
    drawClickNumbers(app)
    drawInstructions(app)
    if app.setDifficulty:
        drawDifficultyScreen(app)
    if app.setHint:
        drawHint(app)

def drawHint(app):
    drawRect(643,100,74,20,border='dimGray',borderWidth=1,fill=None)
    drawLabel('Show',680,110)
    drawRect(643,120,74,20,border='dimGray',borderWidth=1,fill=None)
    drawLabel('Play',680,130)

def drawDifficultyScreen(app):
    for i in range(len(app.levels)):
        drawRect(359,100+20*i,82,20,align='center',fill='white',border='gray',borderWidth=0.5)
    for i in range(len(app.levels)):
        drawLabel(app.levels[i],359,100+20*i)

def drawClickNumbers(app):
    for row in range(3):
        for col in range(3):
            cellLeft, cellTop = getClickCellLeftTop(app, row, col)
            cellWidth, cellHeight = getClickCellSize(app)
            drawLabel(app.clickBoard[row][col],cellLeft+cellWidth/2,
                        cellTop+cellHeight/2, bold = True, size = 16)

def drawClickBoard(app):
    for row in range(app.clickRows):
        for col in range(app.clickCols):
            drawClickCell(app, row, col)
    drawRect(675,385,50,25,border = 'dimGray', fill = None,align='center')
    drawLabel('DELETE',675,385,size = 10, bold = True)

def drawClickBoardBorder(app):
    drawRect(app.clickBoardLeft, app.clickBoardTop, app.clickBoardWidth, app.clickBoardHeight,
             fill = None, border = 'dimGray', borderWidth = 2*app.clickCellBorderWidth)

def drawClickCell(app, row, col):
    cellLeft, cellTop = getClickCellLeftTop(app, row, col)
    cellWidth, cellHeight = getClickCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = None, 
             border = 'dimGray', borderWidth = app.clickCellBorderWidth)

def getClickCellLeftTop(app, row, col):
    cellWidth, cellHeight = getClickCellSize(app)
    cellLeft = app.clickBoardLeft + col * cellWidth
    cellTop = app.clickBoardTop + row * cellHeight
    return (cellLeft, cellTop)
    
def getClickCellSize(app):
    cellWidth = app.clickBoardWidth / app.clickCols
    cellHeight = app.clickBoardHeight / app.clickRows
    return (cellWidth, cellHeight)

def drawInstructions(app):
    drawLine(0,60,app.width,60,lineWidth=1)
    drawLine(0,100,app.width,100,lineWidth=1)
    drawLabel('SUDOKU',app.width/2,30,size=30,font='serif',bold=True)
    drawRect(359,80,82,20,align='center',fill= None,border='gray',borderWidth=0.5)
    drawLabel(f'{app.levels[app.difficulty]}',356,80,size = 16,font='sans-serif')
    drawPolygon(385,78,396,78,391,82, fill = 'gray')
    drawRect(450,80,80,20,align='center',fill='gainsboro')
    drawLabel('NEW BOARD',450,80,size = 10,font='sans-serif')
    drawLabel('BACK TO HOMEPAGE',100,30,size=10,font='sans-serif')
    if app.won:
        drawLabel('You win!',300,132,size=30)
        if app.competition:
            submitBoard(app)
    if app.lost:
        drawLabel('You lost!',490,80,size=30)
    if app.setUserNewBoard:
        drawLabel('Set up your board or click here to enter text', 300,132,size=15)
        drawLabel('PLAY', 300,676,size=20)
        if app.preventSetting:
            drawLabel('YOUR BOARD MUST BE LEGAL',300,695,size=10,fill='red')
    else:
        drawLabel('MAKE YOUR OWN BOARD',690,30,size=10,font='sans-serif')
        drawRect(592,150,160,25,fill=None,border='dimGray')
        if app.legalMode:
            drawRect(672,150,80,25)
            colX = 'white'
            colY = 'dimGray'
        else:
            drawRect(592,150,80,25)
            colX = 'dimGray'
            colY = 'white'
        drawLabel("Normal",632,162.5,size=12,fill=colY)
        drawLabel("Candidate",712,162.5,size=12,fill=colX)
        if app.manual:
            drawRect(590,403,15,15,fill=None,border='dimGray',borderWidth=1.5)
        else:
            drawRect(590,403,15,15,fill='purple',border='dimGray',borderWidth=1.5)
        drawLabel('Auto Canditate Mode',665,410,font='sans-serif')
        drawRect(675,440,100,20,fill=None,align='center',border='dimGray')
        drawLabel('PLAY SINGLETON',675,440,size=10)
        if app.noSingletons:
            drawLabel("There are no available singletons!",675,460,size=10,fill='red')
        drawLabel("Undo",70,80,size=20)
        drawLabel("Redo",140,80,size=20)
        drawLabel('Hint',672,80,size=20)
        drawLabel('Help',620,80,size=20)
        drawLabel('Settings',750,80,size=20)
        drawPolygon(692,78,703,78,698,82, fill = 'gray')
        minutes = app.timer//60
        seconds = app.timer - minutes*60
        if seconds < 10:
            seconds = '0'+str(seconds)
        if app.clock:
            drawLabel(f'{minutes}:{seconds}',210,80,size=20)

def submitBoard(app):
    board = ''
    for row in range(9):
        for col in range(9):
            if row == 8 and col == 8:
                board += app.userBoard.board[row][col]
            else:
                board += app.userBoard.board[row][col] + ' '
        if row != 8:
            board += '\n'
    contents = board
    fileName = 'submittedBoard'
    writeFile(f'boards/{fileName}.txt', contents)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawNumbers(app):
    for row in range(len(app.userBoard.board)):
        for col in range(len(app.userBoard.board[0])):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            if app.givenBoard[row][col] != "0":
                drawLabel(app.givenBoard[row][col],cellLeft+cellWidth/2,
                        cellTop+cellHeight/2, bold = True, size = 28)
            elif app.userBoard.board[row][col] in "123456789":
                drawLabel(app.userBoard.board[row][col],cellLeft+cellWidth/2,
                        cellTop+cellHeight/2, size = 28)
            else:
                if app.manual:
                    drawLegals(app,app.userBoard.manualLegals[row][col],cellLeft+cellWidth/2,
                        cellTop+cellHeight/2)
                else:
                    drawLegals(app,app.userBoard.legals[row][col],cellLeft+cellWidth/2,
                        cellTop+cellHeight/2)

def drawLegals(app,legals,midX,midY):
    if app.showLegals:
        cellWidth, cellHeight = getCellSize(app)
        cellWidth //= 3
        cellHeight //=3
        topX,topY = midX-cellWidth, midY-cellHeight
        row = 0
        col = 0
        for i in range(1,10):
            if str(i) in legals:
                drawLabel(i,topX+cellWidth*row,topY+cellHeight*col, size=11,fill='dimGray')
            row += 1
            if row == 3:
                row = 0
                col += 1

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=4*app.cellBorderWidth)

def drawBlockBorder(app):
    for i in range(3):
        for j in range(3):
            blockLeft, blockTop = getCellLeftTop(app,i*3,j*3)
            cellWidth, cellHeight = getCellSize(app)
            drawRect(blockLeft, blockTop, cellWidth*3, cellHeight*3,
                fill=None, border='dimGray', borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if app.competition and app.lost:
        color = 'fireBrick'
    if app.won:
        color = 'honeydew'
    else:
        if (row,col) == app.selection:
            color = app.selectedCol
        elif app.givenBoard[row][col] != "0":
            color = app.givenCol
        else:
            color = None
        if not app.competition:
            if app.highlightConflicts:
                if (row,col) in app.illegal:
                    color = 'fireBrick'
            if app.hintCells != None and (row,col) in app.hintCells[0]:
                color = 'lavenderBlush'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='dimGray',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def play_onMousePress(app, mouseX, mouseY):
    if app.setUserNewBoard:
        if 153 <= mouseX <= 447 and 125 <= mouseY <= 137:
            uniqueNewBoard(app)
        elif 270 <= mouseX <= 329 and 668 <= mouseY <= 682:
            if app.illegal != []:
                app.preventSetting = True
            app.solvedBoard = State(copy.deepcopy(app.givenBoard))
            if solveBoard(app) == None:
                app.preventSetting = True
            else:
                app.preventSetting = False
                app.userBoard = State(copy.deepcopy(app.givenBoard))
                app.setUserNewBoard = False
                app.solvedBoard.updateLegals()
                solveBoard(app)           
    if app.setDifficulty:
        if 318<=mouseX<=401 and 90<=mouseY<=190:
            for i in range(len(app.levels)):
                if 90+20*i<mouseY<110+20*i:
                    app.difficulty = i
            app.setDifficulty = False
    else:   
        if not app.competition:
            if 625<=mouseX<=725 and 430<=mouseY<=450:
                playSingleton(app)
            if 650 <= mouseX <= 710 and 72 <= mouseY <= 88:
                app.setHint = not app.setHint
            if app.setHint:
                if 643 <= mouseX <= 717 and 100 <= mouseY <= 120:
                    app.hintCells = findHint(app,app.userBoard)
                    app.setHint = False
                elif 643 <= mouseX <= 717 and 121 <= mouseY <= 140:
                    app.hintCells = findHint(app,app.userBoard)
                    playHintCell(app)
                    app.setHint = False
        if 594 <= mouseX <= 645 and 72 <= mouseY <= 88:
            setActiveScreen('help')
        elif 410 <= mouseX <= 490 and 70 <= mouseY <= 90:
            newBoard(app)
        elif 319<=mouseX<=401 and 70<=mouseY<=90:
            app.setDifficulty = True
        elif 590< mouseX<= 605 and 403<=mouseY<=418:
            app.manual = not app.manual
            if not app.manual:
                app.noSingletons = False
                app.userBoard.updateLegals()
        elif 710<mouseX<=790 and 72<=mouseY<=88:
            setActiveScreen('settings')
        if 45<=mouseX<=97 and 73<=mouseY<=87:
            undoMove(app)
        elif 115<=mouseX<=167 and 73<=mouseY<=87:
            redoMove(app)
        elif 592<=mouseX<=672 and 150<=mouseY<=175:
            app.legalMode = False
        elif 672<=mouseX<=752 and 150<=mouseY<=175:
            app.legalMode = True
        if 625<=mouseX<=755 and 25<= mouseY <= 35:
            app.setUserNewBoard = True
            userNewBoard(app)
        if 45<=mouseX<=157 and 23<=mouseY<=35:
            setActiveScreen('splash')
        elif 655<=mouseX<=680 and 372.5<=mouseY<=397.5:
            if app.selection != None:
                if app.setUserNewBoard:
                    app.givenBoard[app.selection[0]][app.selection[1]] = "0"
                    moveMade(app,app.selection[0],app.selection[1])
                else:
                    if not app.legalMode:
                        if app.givenBoard[app.selection[0]][app.selection[1]] == '0':
                            trackMove(app,app.selection[0],app.selection[1],app.userBoard.board[app.selection[0]][app.selection[1]],'0')
                            app.userBoard.set(app.selection[0],app.selection[1],'0')
                            moveMade(app,app.selection[0],app.selection[1])
        else:
            selectedCell = getCell(app, mouseX, mouseY)
            selectedClickCell = getClickCell(app, mouseX, mouseY)
            if selectedCell != None:
                if selectedCell == app.selection:
                    app.selection = None
                else:
                    app.selection = selectedCell
            app.clickSelection = selectedClickCell
            if app.selection != None and app.clickSelection != None:
                if app.setUserNewBoard:
                    app.givenBoard[app.selection[0]][app.selection[1]] = str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]])
                    moveMade(app,app.selection[0],app.selection[1])
                else:
                    if app.givenBoard[app.selection[0]][app.selection[1]] == '0':
                        if app.legalMode:
                            if not app.manual:
                                app.userBoard.manualLegals = copy.deepcopy(app.userBoard.legals)
                                app.manual = True
                            if str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]) in app.userBoard.manualLegals[app.selection[0]][app.selection[1]]:
                                app.userBoard.manualLegals[app.selection[0]][app.selection[1]].remove(str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]))
                                if app.solvedBoard.board[app.selection[0]][app.selection[1]] == str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]):
                                    app.illegal += [(app.selection[0],app.selection[1])]
                                    if app.competition:
                                        app.lost = True
                            else:
                                app.userBoard.manualLegals[app.selection[0]][app.selection[1]].add(str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]))
                                if app.solvedBoard.board[app.selection[0]][app.selection[1]] == str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]):
                                    if (app.selection[0],app.selection[1]) in app.illegal:
                                        app.illegal.remove((app.selection[0],app.selection[1]))
                        else:
                            trackMove(app,app.selection[0],app.selection[1],app.userBoard.board[app.selection[0]][app.selection[1]],str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]))
                            app.userBoard.set(app.selection[0],app.selection[1],str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]))
                            moveMade(app,app.selection[0],app.selection[1])


def findHint(app,board):
    #hint1
    for row in range(9):
        for col in range(9):
            if len(board.legals[row][col]) == 1:
                return ([(row,col)],sorted(board.legals[row][col])[0])
    #hint2
    for N in range(2,6):
        for region in app.regions:
            for targetCells in itertools.combinations(region, N):
                for valueCombo in itertools.combinations(['1','2','3','4','5','6','7','8','9'],N):
                    if isObviousTuple(board,targetCells,valueCombo):
                        if isLegalBan(region,board,targetCells,valueCombo):
                            return (list(targetCells),valueCombo)
    #hint3
    for region in app.regions:
        secTracker = dict()
        for cell in region:
            if len(board.legals[cell[0]][cell[1]]) == 1:
                board.board[cell[0]][cell[1]] = sorted(board.legals[cell[0]][cell[1]])[0]
            for legal in board.legals[cell[0]][cell[1]]:
                if legal not in secTracker:
                    secTracker[legal] = {(cell[0],cell[1])}
                else:
                    secTracker[legal].add((cell[0],cell[1]))
        for key in secTracker:
            if len(secTracker[key]) == 1:
                row = sorted(secTracker[key])[0][0]
                col = sorted(secTracker[key])[0][1]
                return ([(row,col)],key)
    return None

def isLegalBan(region,board,targetCells,valueCombo):
    for cell in region:
        if cell not in targetCells:
            for value in valueCombo:
                if value in board.legals[cell[0]][cell[1]]:
                    return True
    return False

def isObviousTuple(board,cells,values):
    for cell in cells:
        if set(values) != board.legals[cell[0]][cell[1]]:
            return False
    return True

def playHintCell(app):
    if app.hintCells != None:
        cells = app.hintCells[0]
        vals = app.hintCells[1]
        for (row,col) in cells:
            if len(vals) == 1:
                app.userBoard.board[row][col] = vals
                moveMade(app,row,col)
            else:
                for region in app.regions:
                    if cellInRegion(cells,region):
                        for val in vals:
                            banValInRegion(app,region,val,cells)

def cellInRegion(cells,region):
    for cell in cells:
        if cell not in region:
            return False
    return True 

def banValInRegion(app,region,val,cells):
    for cell in region:
        if cell not in cells:
            app.userBoard.banLegal(cell[0],cell[1],val)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)
    else:
        return None

def getClickCell(app, x, y):
    dx = x - app.clickBoardLeft
    dy = y - app.clickBoardTop
    cellWidth, cellHeight = getClickCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.clickRows) and (0 <= col < app.clickCols):
        return (row, col)
    else:
        return None

def play_onKeyPress(app,key):
    if key in "123456789":
        if app.selection != None:
            if app.setUserNewBoard == True:
                app.givenBoard[app.selection[0]][app.selection[1]] = key
                moveMade(app,app.selection[0],app.selection[1])
            else:
                if app.givenBoard[app.selection[0]][app.selection[1]] == '0':
                    if app.userBoard.board[app.selection[0]][app.selection[1]] != "-1":
                        if app.legalMode and app.manual:
                            if key in app.userBoard.manualLegals[app.selection[0]][app.selection[1]]:
                                app.userBoard.manualLegals[app.selection[0]][app.selection[1]].remove(key)
                                if app.solvedBoard.board[app.selection[0]][app.selection[1]] == key:
                                    if app.competition:
                                        app.lost = True
                                    app.illegal += [(app.selection[0],app.selection[1])]
                            else:
                                app.userBoard.manualLegals[app.selection[0]][app.selection[1]].add(key)
                                if app.solvedBoard.board[app.selection[0]][app.selection[1]] == key:
                                    if (app.selection[0],app.selection[1]) in app.illegal:
                                        app.illegal.remove((app.selection[0],app.selection[1]))
                        else:
                            trackMove(app,app.selection[0],app.selection[1],app.userBoard.board[app.selection[0]][app.selection[1]],key)
                            app.userBoard.board[app.selection[0]][app.selection[1]] = key
                            moveMade(app,app.selection[0],app.selection[1])
                            app.userBoard.updateLegals()
    if not app.competition:
        if key == 's':
            playSingleton(app)
        elif key == 'h':
            app.hintCells = findHint(app,app.userBoard)
        elif key == 'p':
            app.hintCells = findHint(app,app.userBoard)
            playHintCell(app)
    if key == 'u':
        undoMove(app)
    elif key == 'r':
        redoMove(app)
    elif key == 'l':
        app.legalMode = not app.legalMode
    elif key == 'm':
        app.manual = not app.manual
        if not app.manual:
            app.noSingletons = False
            app.userBoard.updateLegals()
    elif key == "backspace":
        if app.selection != None:
            if app.selection != None:
                if app.setUserNewBoard == True:
                    app.givenBoard[app.selection[0]][app.selection[1]] = '0'
                    moveMade(app,app.selection[0],app.selection[1])
                else:
                    if not app.legalMode:
                        if app.givenBoard[app.selection[0]][app.selection[1]] == '0':
                            if app.userBoard.board[app.selection[0]][app.selection[1]] != "0":
                                trackMove(app,app.selection[0],app.selection[1],app.userBoard.board[app.selection[0]][app.selection[1]],'0')
                                app.userBoard.board[app.selection[0]][app.selection[1]] = "0"
                                moveMade(app,app.selection[0],app.selection[1])
                                app.userBoard.updateLegals()
    elif key == "up":
        if app.selection != None and app.selection[0] > 0:
            app.selection = findNext(list(app.selection),-1,0)
    elif key == "down":
        if app.selection != None and app.selection[0] < 8:
            if findNext(list(app.selection),1,0) != None:
                app.selection = findNext(list(app.selection),1,0)
    elif key == "right":
        if app.selection != None and app.selection[1] < 8:
            if findNext(list(app.selection),0,1) != None:
                app.selection = findNext(list(app.selection),0,1)
    elif key == "left":
        if app.selection != None and app.selection[1] > 0:
            if findNext(list(app.selection),0,-1) != None:
                app.selection = findNext(list(app.selection),0,-1)

def playSingleton(app):
    for row in range(9):
        for col in range(9):
            if len(app.userBoard.legals[row][col]) == 1:
                trackMove(app,row,col,'0',sorted(app.userBoard.legals[row][col])[0])
                app.userBoard.set(row,col,sorted(app.userBoard.legals[row][col])[0])
                moveMade(app,row,col)
                app.userBoard.updateLegals()
                app.noSingletons = False
                return
    app.noSingletons = True

def findNext(selection,dx,dy):
    selection[0] += dx
    selection[1] += dy
    if selection[0] < 0 or selection[0] > 8 or selection[1] < 0 or selection[1] > 8:
        return None
    return (selection[0],selection[1])

def trackMove(app,row,col,oldVal,newVal):
    app.movesMade += [(row,col,oldVal,newVal)]
    app.moveCounter = len(app.movesMade)-1

def moveMade(app,row,col):
    app.hintCells = None
    app.noSingletons = False
    app.userBoard.updateLegals()
    if app.setUserNewBoard:
        board = app.givenBoard
    else:
        board = app.userBoard.board
    if not isLegalSudoku(board,row,col):
        #competiton mode
        if app.competition:
            app.lost = True
        app.illegal += [(row,col)]
    else:
        if (row,col) in app.illegal:
            app.illegal.remove((row,col))
    if not app.setUserNewBoard:
        if app.userBoard.board[row][col] != '0' and app.userBoard.board[row][col] != app.solvedBoard.board[row][col]:
            #competiton mode
            if app.competition:
                app.lost = True
            app.illegal += [(row,col)]
        else:
            if (row,col) in app.illegal:
                app.illegal.remove((row,col))
    if boardFull(app.userBoard.board) and app.illegal==[]:
        app.won = True
    if app.setUserNewBoard:
        if app.illegal == []:
            app.preventSetting = False

def undoMove(app):
    if app.moveCounter != -1:
        (row,col,oldVal,_) = app.movesMade[app.moveCounter]
        app.moveCounter -= 1
        app.userBoard.set(row,col,oldVal)
        moveMade(app,row,col)

def redoMove(app):
    if app.moveCounter != len(app.movesMade) - 1:
        (row,col,_,newVal) = app.movesMade[app.moveCounter+1]
        app.moveCounter += 1
        app.userBoard.set(row,col,newVal)
        moveMade(app,row,col)

def boardFull(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                return False
    return True

def isLegalSudoku(grid,row,col):
    rowInGrid = copy.copy(grid[row])
    rowInGrid.pop(col)
    if isRepeat(rowInGrid,grid[row][col]):
        return False
    column = []
    for rownum in range(len(grid)):
        if rownum != row:
            column += [grid[rownum][col]]
    if isRepeat(column,grid[row][col]):
        return False
    rowsec = row//3
    colsec = col//3
    section = []
    for i in range(3):
        for j in range(3):
            if rowsec*3+i != row and colsec*3+j != col:
                section += [grid[rowsec*3+i][colsec*3+j]]
    if isRepeat(section,grid[row][col]):
        return False
    return True

def isRepeat(L,element):
    if element != '0' and str(element) in L:
        return True
    else:
        return False
              
runAppWithScreens(initialScreen='splash',width=800,height=750)