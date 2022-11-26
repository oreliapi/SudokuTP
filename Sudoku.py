import os
import random
import math
import copy

try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

import inspect


# from https://www.cs.cmu.edu/~112-3/notes/term-project.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# from https://www.cs.cmu.edu/~112-3/notes/term-project.html
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

boards = [[],[],[],[],[]]
solutions = [[],[],[],[],[]]

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
    elif filename.endswith('.txt') and filename.endswith('solution.txt'):
        pathToFile = f'boards/{filename}'
        fileContents = readFile(pathToFile)
        newBoard = []
        for number in fileContents:
            if number != " " and number !=  "\n":
                newBoard += number
        if filename.startswith('easy'):
            solutions[0].append(newBoard)
        elif filename.startswith('medium'):
            solutions[1].append(newBoard)
        elif filename.startswith('hard'):
            solutions[2].append(newBoard)
        elif filename.startswith('expert'):
            solutions[3].append(newBoard)
        elif filename.startswith('evil'):
            solutions[4].append(newBoard)

# contents = 'This is just a string. Woohoo!'
# writeFile('someFolder/myFileName.txt', contents)

#from https://www.cs.cmu.edu/~112-3/notes/runAppWithScreensDemo2.py

##################################################################
# runAppWithScreens() and setActiveScreen(screen)
##################################################################

def runAppWithScreens(initialScreen, *args, **kwargs):
    global _callerGlobals
    _callerGlobals = inspect.stack()[1][0].f_globals

    appFnNames = ['onAppStart',
                  'onKeyPress', 'onKeyHold', 'onKeyRelease',
                  'onMousePress', 'onMouseDrag', 'onMouseRelease',
                  'onMouseMove', 'onStep', 'redrawAll']
             
    def checkForAppFns():
        globalVars = _callerGlobals # globals()
        for appFnName in appFnNames:
            if appFnName in globalVars:
                raise Exception(f'Do not define {appFnName} when using screens')
   
    def getScreenFnNames(appFnName):
        globalVars = _callerGlobals # globals()
        screenFnNames = [ ]
        for globalVarName in globalVars:
            screenAppSuffix = f'_{appFnName}'
            if globalVarName.endswith(screenAppSuffix):
                screenFnNames.append(globalVarName)
        return screenFnNames
   
    def wrapScreenFns():
        globalVars = _callerGlobals # globals()
        for appFnName in appFnNames:
            screenFnNames = getScreenFnNames(appFnName)
            if (screenFnNames != [ ]) or (appFnName == 'onAppStart'):
                globalVars[appFnName] = makeAppFnWrapper(appFnName)
   
    def makeAppFnWrapper(appFnName):
        if appFnName == 'onAppStart':
            def onAppStartWrapper(app):
                globalVars = _callerGlobals # globals()
                for screenFnName in getScreenFnNames('onScreenStart'):
                    screenFn = globalVars[screenFnName]
                    screenFn(app)
            return onAppStartWrapper
        else:
            def appFnWrapper(*args):
                globalVars = _callerGlobals # globals()
                screen = globalVars['_activeScreen']
                wrappedFnName = ('onScreenStart'
                                 if appFnName == 'onAppStart' else appFnName)
                screenFnName = f'{screen}_{wrappedFnName}'
                if screenFnName in globalVars:
                    screenFn = globalVars[screenFnName]
                    return screenFn(*args)
            return appFnWrapper

    def go():
        checkForAppFns()
        wrapScreenFns()
        setActiveScreen(initialScreen)
        runApp(*args, **kwargs)
   
    go()

def setActiveScreen(screen):
    globalVars = _callerGlobals # globals()
    if (screen in [None, '']) or (not isinstance(screen, str)):
        raise Exception(f'{repr(screen)} is not a valid screen')
    redrawAllFnName = f'{screen}_redrawAll'
    if redrawAllFnName not in globalVars:
        raise Exception(f'Screen {screen} requires {redrawAllFnName}()')
    globalVars['_activeScreen'] = screen

##################################################################
# end of runAppWithScreens() and setActiveScreen(screen)
##################################################################

#Splash Screen
def splash_onScreenStart(app):
    pass

def splash_redrawAll(app):
    drawLabel('S U D O K U',app.width/2,app.height/2-150,fill='darkSlateBlue',size=60,font = 'monospace',bold=True)
    drawLabel('PLAY',app.width/2,app.height/2+100,size=30)
    drawLabel('HELP',app.width/2,app.height/2+150,size=30)
    
def splash_onMousePress(app,mouseX,mouseY):
    if 350<=mouseX<=450 and 437<=mouseY<=459:
        setActiveScreen('play')
    elif 350<mouseX<=450 and 487<=mouseY<=509:
        setActiveScreen('help')

#Help Screen
def help_onScreenStart(app):
    pass

def help_redrawAll(app):
    #Instructions from https://www.nytimes.com/puzzles/sudoku/easy
    drawLabel('Fill the grid with your keyboard so that every row, column and'+
                ' 3×3 box contains the digits 1 to 9, without repeating.',
                app.width/2,app.height/2,size=14)
    drawLabel('BACK TO HOMEPAGE',100,39,size=10)

def help_onMousePress(app,mouseX,mouseY):
    if 48<=mouseX<=153 and 33<=mouseY<=42:
        setActiveScreen('splash')

#State Class
class State:
    def __init__(self,board):
        self.board = board
        legals = [[],[],[],[],[],[],[],[],[]]
        for row in range(9):
            for i in range(9):
                legals[row].append({'1','2','3','4','5','6','7','8','9'})
        self.legals = legals
        for row in range(9):
            for col in range(9):
                self.ban(row,col,self.board[row][col])
    def set(self,row,col,value):
        self.board[row][col] = value
    def updateLegals(self):
        for row in range(9):
            for col in range(9):
                self.ban(row,col,self.board[row][col])
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
        
#Play Screen
def play_onScreenStart(app):
    app.difficulty = 0
    app.boardNum = None
    setUpBoard(app)
    newBoard(app)
    setUpClickBoard(app)
    app.setDifficulty = False
    app.setUserNewBoard = False 
    app.manual = True

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
    app.clickBoardTop = app.boardTop+app.clickBoardHeight 
    app.clickCellBorderWidth = 1.5
    app.clickBoard = [[1,2,3],[4,5,6],[7,8,9]]
    app.clickSelection = None

def newBoard(app):
    app.illegal = []
    app.won = False
    app.boardNum = random.randrange(0,3)
    app.givenBoard = boards[app.difficulty][app.boardNum]
    app.userBoard = State(copy.deepcopy(app.givenBoard))
    #app.userBoard = copy.deepcopy(app.givenBoard)
    app.selection = None
    if app.difficulty == 0:
        app.manual = True
    else:
        app.manual = False
        
def userNewBoard(app):
    app.illegal = []
    app.won = False
    app.givenBoard = [['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],
                    ['0','0','0','0','0','0','0','0','0']]
    app.userBoard = State(copy.deepcopy(app.givenBoard))
    #app.userBoard = copy.deepcopy(app.givenBoard)
    app.selection = None
    app.preventSetting = False

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

def drawDifficultyScreen(app):
    for i in range(len(app.levels)):
        drawRect(305,100+20*i,145,20,align='center',fill='white',border='gray',borderWidth=0.5)
    for i in range(len(app.levels)):
        drawLabel(app.levels[i],305,100+20*i)

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
    drawRect(675,500,50,25,border = 'black', fill = None,align='center')
    drawLabel('DELETE',675,500,size = 10, bold = True)

def drawClickBoardBorder(app):
    drawRect(app.clickBoardLeft, app.clickBoardTop, app.clickBoardWidth, app.clickBoardHeight,
             fill = None, border = 'black', borderWidth = 2*app.clickCellBorderWidth)

def drawClickCell(app, row, col):
    cellLeft, cellTop = getClickCellLeftTop(app, row, col)
    cellWidth, cellHeight = getClickCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = None, 
             border = 'black', borderWidth = app.clickCellBorderWidth)

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
    drawLabel('Sudoku!',300,40,size=30)
    drawRect(305,80,145,20,align='center',fill= None,border='gray',borderWidth=0.5)
    drawLabel(f'Difficulty: {app.levels[app.difficulty]}',300,80,size = 16)
    drawPolygon(362,78,373,78,368,82, fill = 'gray')
    drawRect(300,120,80,30,align='center',fill='gainsboro')
    drawLabel('NEW BOARD', 300,120,size = 10)
    drawLabel('BACK TO HOMEPAGE',100,39,size=10)
    drawLabel('MAKE YOUR OWN BOARD',690,39,size=10)
    if app.won:
        drawLabel('You win!',600,100,size=30)
    if app.setUserNewBoard:
        drawLabel('SETTING UP YOUR BOARD...', 690,60,size=10)
        drawLabel('CLICK HERE TO PLAY YOUR BOARD', 690,80,size=10)
        if app.preventSetting:
            drawLabel('YOUR BOARD MUST BE LEGAL',690,100,size=10,fill='red')

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
                        cellTop+cellHeight/2, bold = True, size = 16)
            if app.userBoard.board[row][col] in "123456789":
                drawLabel(app.userBoard.board[row][col],cellLeft+cellWidth/2,
                        cellTop+cellHeight/2, size = 16)

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
                fill=None, border='black', borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if app.won:
        color = 'honeydew'
    else:
        if (row,col) in app.illegal:
            color = 'fireBrick'
        elif (row,col) == app.selection:
            color = "thistle"
        elif app.givenBoard[row][col] != "0":
            color = "ghostWhite"
        else:
            color = None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
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
        if 600 <= mouseX <= 780 and 76 <= mouseY <= 86:
            if app.illegal != []:
                app.preventSetting = True
            else:
                app.preventSetting = False
                app.setUserNewBoard = False
    if not app.setDifficulty:
        if 260 <= mouseX <= 340 and 90 <= mouseY <= 150:
            newBoard(app)
        if 232.5<=mouseX<=377.5 and 70<=mouseY<=90:
            app.setDifficulty = True
    else:   
        if 232.5<=mouseX<=377.5 and 90<=mouseY<=190:
            for i in range(len(app.levels)):
                if 90+20*i<mouseY<110+20*i:
                    app.difficulty = i
            app.setDifficulty = False
    if 625<=mouseX<=755 and 33<= mouseY <= 45:
        app.setUserNewBoard = True
        userNewBoard(app)
    if 48<=mouseX<=153 and 33<=mouseY<=42:
        setActiveScreen('splash')
    elif 650<=mouseX<=700 and 487.5<=mouseY<=512.5:
        if app.selection != None:
            if app.setUserNewBoard:
                app.givenBoard[app.selection[0]][app.selection[1]] = "0"
                moveMade(app,app.selection[0],app.selection[1])
            else:
                if app.givenBoard[app.selection[0]][app.selection[1]] == '0':
                    app.userBoard.set(app.selection[0],app.selection[1],'0')
                    #app.userBoard[app.selection[0]][app.selection[1]] = "0"
                    if app.manual == False:
                        app.userBoard.updateLegals()
                    moveMade(app,app.selection[0],app.selection[1])
    else:
        selectedCell = getCell(app, mouseX, mouseY)
        selectedClickCell = getClickCell(app, mouseX, mouseY)
        if selectedCell != None:
            if selectedCell == app.selection:
                app.selection = None
            else:
                app.selection = selectedCell
        if selectedClickCell != None:
            if selectedClickCell == app.clickSelection:
                app.clickSelection = None
            else:
                app.clickSelection = selectedClickCell
        else:
            app.clickSelection = None
        if app.selection != None and app.clickSelection != None:
            if app.setUserNewBoard:
                app.givenBoard[app.selection[0]][app.selection[1]] = str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]])
                moveMade(app,app.selection[0],app.selection[1])
            else:
                if app.givenBoard[app.selection[0]][app.selection[1]] == '0':
                    app.userBoard.set(app.selection[0],app.selection[1],str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]]))
                    if app.manual == False:
                        app.userBoard.updateLegals()
                    #app.userBoard[app.selection[0]][app.selection[1]] = str(app.clickBoard[app.clickSelection[0]][app.clickSelection[1]])
                    moveMade(app,app.selection[0],app.selection[1])

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
                        app.userBoard.board[app.selection[0]][app.selection[1]] = key
                        if app.manual == False:
                            app.userBoard.updateLegals()
                        moveMade(app,app.selection[0],app.selection[1])
    elif key == "backspace":
        if app.selection != None:
            if app.selection != None:
                if app.setUserNewBoard == True:
                    app.givenBoard[app.selection[0]][app.selection[1]] = '0'
                    moveMade(app,app.selection[0],app.selection[1])
                else:
                    if app.givenBoard[app.selection[0]][app.selection[1]] == '0':
                        if app.userBoard.board[app.selection[0]][app.selection[1]] != "0":
                            app.userBoard.board[app.selection[0]][app.selection[1]] = "0"
                            if app.manual == False:
                                app.userBoard.updateLegals()
                            moveMade(app,app.selection[0],app.selection[1])
    elif key == "up":
        if app.selection != None and app.selection[0] > 0:
            if findNext(app,list(app.selection),-1,0) != None:
                app.selection = findNext(app,list(app.selection),-1,0)
    elif key == "down":
        if app.selection != None and app.selection[0] < 8:
            if findNext(app,list(app.selection),1,0) != None:
                app.selection = findNext(app,list(app.selection),1,0)
    elif key == "right":
        if app.selection != None and app.selection[1] < 8:
            if findNext(app,list(app.selection),0,1) != None:
                app.selection = findNext(app,list(app.selection),0,1)
    elif key == "left":
        if app.selection != None and app.selection[1] > 0:
            if findNext(app,list(app.selection),0,-1) != None:
                app.selection = findNext(app,list(app.selection),0,-1)

def findNext(app, selection,dx,dy):
    selection[0] += dx
    selection[1] += dy
    while app.givenBoard[(selection[0])][selection[1]] != "0":
        selection[0] += dx
        selection[1] += dy
        if selection[0] < 0 or selection[0] > 8 or selection[1] < 0 or selection[1] > 8:
            return None
    return (selection[0],selection[1])

def moveMade(app,row,col):
    print(app.userBoard.legals)
    if app.setUserNewBoard:
        board = app.givenBoard
    else:
        board = app.userBoard.board
    if not isLegalSudoku(board,row,col):
        app.illegal += [(row,col)]
    else:
        if (row,col) in app.illegal:
            app.illegal.remove((row,col))
    if boardFull(app) and app.illegal==[]:
        app.won = True
    if app.setUserNewBoard:
        if app.illegal == []:
            app.preventSetting = False

def boardFull(app):
    for row in range(9):
        for col in range(9):
            if app.userBoard.board[row][col] == '0':
                return False
    return True

def isLegalSudoku(grid,row,col):
    rowInGrid = copy.copy(grid[row])
    rowInGrid.pop(col)
    if isRepeat(rowInGrid,grid[row][col]):
        print("row has repeats")
        return False
    column = []
    for rownum in range(len(grid)):
        if rownum != row:
            column += [grid[rownum][col]]
    if isRepeat(column,grid[row][col]):
        print("column has repeats")
        return False
    rowsec = row//3
    colsec = col//3
    section = []
    for i in range(3):
        for j in range(3):
            if rowsec*3+i != row and colsec*3+j != col:
                section += [grid[rowsec*3+i][colsec*3+j]]
    if isRepeat(section,grid[row][col]):
        print("section has repeats")
        return False
    return True

def isRepeat(L,element):
    if element != '0' and str(element) in L:
        return True
    else:
        return False

                
runAppWithScreens(initialScreen='splash',width=800,height=700)
