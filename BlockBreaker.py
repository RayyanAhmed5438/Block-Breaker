import sys
from   PyQt5.QtWidgets import QApplication,QWidget,QLabel
from   PyQt5.QtCore    import Qt,QTimer
from   PyQt5.QtGui     import QFont,QFontDatabase
from   PyQt5.QtWidgets import QGraphicsOpacityEffect
from   PyQt5.QtCore    import QPropertyAnimation
import pygame
import random

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,1950,980)

        font_id = QFontDatabase.addApplicationFont("assets/digit.TTF")
        font_familly = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.my_font = QFont(font_familly,150)


        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("assets/tap.mp3")


        self.plat        = QLabel(self)
        self.plat_x      = 550
        self.plat_y      = 850
        self.plat_width  = 250
        self.plat_heigth = 20
        self.dx          = 15


        self.ball      = QLabel("📀",self)
        self.ball_size = 15
        self.ball_x    = 660
        self.ball_y    = 820
        self.ball_dx   = 5
        self.ball_dy   = -5


        self.blocks        = []
        self.blocks_width  = 20
        self.blocks_height = 15
        self.gap_x         = 60
        self.gap_y         = 6

        
        self.win       = QLabel("YOU WIN"          ,self)
        self.over      = QLabel("GAME OVER"        ,self)
        self.big_plat  = QLabel("BIGGER PLATFORM!!",self)
        self.big_ball  = QLabel("BIGGER BALL!!"    ,self)
        self.fast_ball = QLabel("FASTER BALL!?"    ,self)


        self.fade1 = QPropertyAnimation(QGraphicsOpacityEffect(self.big_plat), b"opacity")
        self.big_plat.setGraphicsEffect(self.fade1.targetObject())


        self.fade2 = QPropertyAnimation(QGraphicsOpacityEffect(self.big_ball), b"opacity")
        self.big_ball.setGraphicsEffect(self.fade2.targetObject())

        self.fade3 = QPropertyAnimation(QGraphicsOpacityEffect(self.fast_ball), b"opacity")
        self.fast_ball.setGraphicsEffect(self.fade3.targetObject())


        self.UI()
        self.craete_blocks()
        self.raise_labels()


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_ball)
        self.timer.timeout.connect(self.check_collision)
        self.timer.timeout.connect(self.move_plat)    
        self.timer.start(18)


    def UI(self):

        self.setStyleSheet("background-color : grey;")


        self.plat.setGeometry(self.plat_x,self.plat_y,self.plat_width,self.plat_heigth)
        self.plat.setStyleSheet("background-color : green;border : 3px solid black;")


        self.ball.setStyleSheet(f"font-family : segoe UI emoji;font-size : {self.ball_size}px;")
        self.ball.move(self.ball_x,self.ball_y)


        self.over.move(550,400)
        self.over.setStyleSheet("color : lime;font-size :200px;background-color : red;border-radius : 20px;")
        self.over.setFont(self.my_font)
        self.over.hide()


        self.win.move(550,400)
        self.win.setStyleSheet("color : green;font-size :200px")
        self.win.setFont(self.my_font)
        self.win.hide()


        self.big_plat.move(400,700)
        self.big_plat.setStyleSheet("color : cyan;font-size :50px;font-weight : bold;")
        self.big_plat.hide()


        self.big_ball.move(1000,700)
        self.big_ball.setStyleSheet("color : cyan;font-size :50px;font-weight : bold;")
        self.big_ball.hide()

        self.fast_ball.move(750,500)
        self.fast_ball.setStyleSheet("color : red;font-size :50px;font-weight : bold;")
        self.fast_ball.hide()

        
    def craete_blocks(self):
         
        rows   = 20
        blocks = 24

        for row in range(rows):

            if row % 2 == 0:
                num_cols    = blocks
                row_x_start = 0 

            else:
                num_cols    = blocks-1
                row_x_start = (self.blocks_width  + self.gap_x)  // 2

            for col in range(num_cols):
                x = row_x_start + col * (self.blocks_width + self.gap_x)
                y = row * (self.blocks_height + self.gap_y)

                block = QLabel(self)
                block.setGeometry(x,y,self.blocks_width,self.blocks_height)
                block.setStyleSheet("background-color : blue;border : 4px solid black;")
                self.blocks.append(block)


    def raise_labels(self):
        self.win     .raise_()
        self.over    .raise_()
        self.big_plat.raise_()
        self.big_ball.raise_()
        self.ball    .raise_()


    def check_collision(self):
        if len(self.blocks) == 0:
            self.timer.stop()
            self.win  .show()
        ball_rect = self.ball.geometry()

        for block in self.blocks:
            block_rect = block.geometry()

            if ball_rect.intersects(block_rect):

                dx_left   = abs(ball_rect.right()   - block_rect.left())
                dx_right  = abs(block_rect.right()  - ball_rect .left())
                dy_top    = abs(ball_rect.bottom()  - block_rect.top() )
                dy_bottom = abs(block_rect.bottom() - ball_rect .top() )

                min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

                if   min_overlap == dx_left:
                    self.ball_dx = -abs(self.ball_dx) 

                elif min_overlap == dx_right:
                    self.ball_dx = abs(self.ball_dx)   

                elif min_overlap == dy_top:
                    self.ball_dy = -abs(self.ball_dy) 

                elif min_overlap == dy_bottom:
                    self.ball_dy = abs(self.ball_dy)

                power = random.randint(1,8)
                if power == 1 :
                    self.plat_width += 40
                    self.show_powerup(self.big_plat,self.fade1)

                elif power == 2:
                    self.ball_size += 4
                    self.ball.setStyleSheet(f"font-size : {self.ball_size}px;")
                    self.ball.adjustSize()
                    self.show_powerup(self.big_ball,self.fade2)

                elif power == 3:
                    self.ball_dx = (abs(self.ball_dx) + 1) * (1 if self.ball_dx > 0 else -1)
                    self.ball_dy = (abs(self.ball_dy) + 1) * (1 if self.ball_dy > 0 else -1)
                    self.show_powerup(self.fast_ball,self.fade3)

                block.hide()
                block.setParent(None)
                block.deleteLater()
                self.blocks.remove(block)
                self.play_sound()
                break


    def move_ball(self):
        x  = self.ball.x()
        y  = self.ball.y()
        x += self.ball_dx
        y += self.ball_dy

        
        W_width  = self.width()
        W_height = self.height()
        l_W      = self.ball.width()
        l_H      = self.ball.height()


        if x <= 0 or x + l_W >= W_width :
            self.ball_dx = -self.ball_dx

        if y <= 0 :
            self.ball_dy = -self.ball_dy

        if y + l_H >= W_height:
            self.timer.stop()
            self.over .show()     

        if self.ball.geometry().intersects(self.plat.geometry()):
            self.ball_dy = -self.ball_dy    
            y = self.plat_y - self.ball.height() - 1 
               
        self.ball.move(x,y)

    def restart_game(self):

        # Stop the game while resetting
        self.timer.stop()

        # Remove old blocks
        for block in self.blocks:
            block.setParent(None)
            block.deleteLater()

        self.blocks.clear()

        # -------------------------
        # RANDOM PLATFORM POSITION
        # -------------------------

        self.plat_width = 250

        max_plat_x = self.width() - self.plat_width

        self.plat_x = random.randint(0, max_plat_x)

        self.plat_y = 850

        # Random platform movement direction
        self.dx = random.choice([-15, 15])

        self.plat.setGeometry(
            self.plat_x,
            self.plat_y,
            self.plat_width,
            self.plat_heigth
        )


        # -------------------------
        # RANDOM BALL POSITION
        # -------------------------

        self.ball_size = 15

        self.ball_x = random.randint(
            int(self.plat_x),
            int(self.plat_x + self.plat_width - 20)
        )

        self.ball_y = self.plat_y - 35


        # -------------------------
        # RANDOM BALL DIRECTION
        # -------------------------

        # Random horizontal direction
        self.ball_dx = random.choice([-5, 5])

        # Ball always initially moves upward
        self.ball_dy = -5

        # Sometimes make the ball start downward
        # Remove these lines if you always want it to start upward
        if random.choice([True, False]):
            self.ball_dy = 5


        self.ball.setStyleSheet(
            f"font-family : segoe UI emoji;"
            f"font-size : {self.ball_size}px;"
        )

        self.ball.adjustSize()
        self.ball.move(
            int(self.ball_x),
            int(self.ball_y)
        )


        # Hide game messages
        self.over.hide()
        self.win.hide()

        # Hide power-up messages
        self.big_plat.hide()
        self.big_ball.hide()
        self.fast_ball.hide()


        # Recreate blocks
        self.craete_blocks()

        # Make blocks visible
        for block in self.blocks:
            block.show()


        # Put important objects on top
        self.raise_labels()

        # Start game
        self.timer.start(18)

    def keyPressEvent(self,event):

        key = event.key()

        if key == Qt.Key_Right:
            self.dx = abs(self.dx)

        elif key == Qt.Key_Left:
            self.dx = -abs(self.dx)

        elif key == Qt.Key_R:
            if not self.timer.isActive():
                self.restart_game()

    def move_plat(self):
        self.plat_x += self.dx

        if self.plat_x <= 0 :
            self.plat_x = 0
        if self.plat_x >= self.width() - self.plat.width():
            self.plat_x = self.width() - self.plat.width()

        self.plat.setGeometry(int(self.plat_x),self.plat_y,self.plat_width,self.plat_heigth)

    def play_sound(self):
        self.sound.play()

    def show_powerup(self,label,fade):
        label.show()

        fade.stop()
        fade.setStartValue(0)
        fade.setEndValue(1)
        fade.setDuration(300)
        fade.start()

        def fade_out():
            fade.stop()
            fade.setStartValue(1)
            fade.setEndValue(0)
            fade.setDuration(500)
            fade.start()

        QTimer.singleShot(800, fade_out)

   
if __name__ == "__main__":
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())        
