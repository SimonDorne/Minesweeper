import sys
import time
import random
from PyQt6.QtWidgets import QWidget, QApplication, QLineEdit, QPushButton, QGridLayout,QVBoxLayout

#Klasse MyMinesweeper erbt von QWidget
class MyMinesweeper(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt6 Minesweeper')
        self.resize(600,600)
        layout =QVBoxLayout()
        self.setLayout(layout)
        self.bombe=0
        dimRow=10
        dimCol=10




        gridLayout=QGridLayout()

        #Erstellen eines Grids mit der Größe dimRow*dimCol, welches mit 0 befüllt ist
        self.minefieldGrid=[]
        for i in range(dimRow):
            row=[]
            for j in range(dimCol):
                row.append(0)
            self.minefieldGrid.append(row)

        #Erstellung von 10 paarweise verschiedenen Zufallszahlen zwischen 0 und 99
        minePos=random.sample(range(100),10)

        #Für jede Mine, ermittele den Spalten und Reiheneintrag und übertrage eine -1 in das Grid
        # divmod gibt zwei Rückgabewerte: 1. mine/dimCol 2. mine%dimCol
        for mine in minePos:
            row, col=divmod(mine,dimCol)
            self.minefieldGrid[row][col]=-1

        #Alle Felder um eine Mine sollen pro Mine um eins erhöht werden
        for row in range(dimRow):
            for col in range(dimCol):
                if self.minefieldGrid[row][col]==-1:
                    #Funktion für Erhöhen um 1
                    self.aroundMine(row,col)
                    
        
        self.buttons=[]
        for row in range(dimRow):
            for col in range(dimCol):
                button=QPushButton('')
                #buttonbeschriftung=10*row+col
                #buttonbeschriftung=self.minefieldGrid[row][col]
                #button.setText(str(buttonbeschriftung))
                button.clicked.connect(self.checkButton)
                button.setFixedSize(50,50)
                self.buttons.append(button)
                gridLayout.addWidget(button, row, col)
                self.buttons[10*row+col].setCheckable(True)
                
        

        layout.addLayout(gridLayout)
    
    #Überprüfung der 8 umliegenden Felder um eine Mine
    def aroundMine(self, mRow, mCol): 
        #Da range von x einschließend bis y ausschließend läuft, muss der linke Rand 0 und der rechte Rand 10 sein
        #Etwas unübersichtlicher aber verständlicher wäre: min(9,mRow+1)+1
        for row in range(max(0,mRow-1), min(10,mRow+2)):
            for col in range(max(0,mCol-1), min(10, mCol+2)):
                if self.minefieldGrid[row][col]!=-1:
                    self.minefieldGrid[row][col]+=1


    def foundZero(self, fRow,fCol):
        for row in range(max(0,fRow-1), min(10,fRow+2)):
            for col in range(max(0,fCol-1), min(10, fCol+2)):
                button=self.buttons[10*row+col]
                if button.isCheckable():
                    button.click()
                    self.buttons[10*row+col].setCheckable(False)
                    
                    
    def checkButton(self):
        sender=self.sender()
        index=self.buttons.index(sender)
        cRow,cCol=divmod(index,10)
        if sender.text()=='' and self.bombe==0:
            valueAtField=self.minefieldGrid[cRow][cCol]
            if valueAtField==-1:
                sender.setText('💣')
                sender.setStyleSheet(' QPushButton {background-color: #eb8c90;color:black}')
                self.bombe=1
                for element in self.buttons:
                    element.setCheckable(False)
            else:
                sender.setText(str(valueAtField))
                sender.setStyleSheet('QPushButton {background-color: #40505c}')
                if valueAtField==0:
                    self.foundZero(cRow,cCol)



        





app = QApplication(sys.argv)
app.setStyleSheet('''
    QWidget{
        font-size: 25px;
    }
    QPushButton{
        font-size: 25px;
    }
''')
window = MyMinesweeper()
window.show()

app.exec()
