import customtkinter as CTK
import random
import requests
import tkinter.font as Font
import math

#pyinstaller --noconfirm --onedir --noconsole HangManCTK.py

keyboardLayouts = [
    ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"],
    ["ABCDEFGHIJ", "KLMNOPQRS", "TUVWXYZ"],
    ["AZERTYUIOP", "QSDFGHJKL", "MWXCVBN"]
]

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()

wordDirectories = [None, None, None, None,
                    "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/d9cddf5e16140df9e14f19c2de76a0ef36fd2748/wordle-La.txt",
                    "https://raw.githubusercontent.com/getify/dwordly-game/main/six-letter-words.json", 
                    "https://raw.githubusercontent.com/powerlanguage/word-lists/master/common-7-letter-words.txt",
                    "https://raw.githubusercontent.com/ghsec/BurpOriginalPayload/master/8%20letter%20words.pay",
                    "https://raw.githubusercontent.com/ghsec/BurpOriginalPayload/master/9%20letter%20words.pay",
                    "https://raw.githubusercontent.com/ghsec/BurpOriginalPayload/master/10%20letter%20words.pay",
                    "https://raw.githubusercontent.com/ghsec/BurpOriginalPayload/master/11%20letter%20words.pay",
                    "https://raw.githubusercontent.com/ghsec/BurpOriginalPayload/master/12%20letter%20words.pay"
                    ]

class HangMan(CTK.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("HangMan")
        self.defaultGeometry = "658x412"
        self.geometry(self.defaultGeometry)
        self._fg_color = "gray26"
        self.LeftFrame = CTK.CTkFrame(self, fg_color="transparent", corner_radius=0, border_width=0)
        self.LeftFrame.pack(side="left", fill="both", expand=True)
        self.HotBar = CTK.CTkFrame(self.LeftFrame, fg_color="transparent", corner_radius=0, border_width=0)
        self.TopFrame = CTK.CTkFrame(self.LeftFrame, fg_color="transparent", corner_radius=0, border_width=0)
        self.BottomFrame = CTK.CTkFrame(self.LeftFrame, fg_color="transparent", width=612, height=540, corner_radius=0, border_width=0)
        self.RightFrame = CTK.CTkFrame(self, fg_color="transparent", width=320, corner_radius=0, border_width=0)
        self.currentLayout = 0
        self.keysList = keyboardLayouts[self.currentLayout]
        self.layouts = [x[0][0:6] for x in keyboardLayouts]
        self.resultLabel = CTK.CTkLabel(self.TopFrame, corner_radius=12, width=520, height=24, font=CTK.CTkFont(family="Arial Black", size=15, weight=Font.NORMAL), fg_color="gray12")
        self.wordSize = 5
        self.GenerateWordList(self.wordSize)
        self.GenMysteryWord()
        self.MainWindow()
    
    def GenMysteryWord(self):
        self.mysteryWord = self.wordList[random.randint(0, len(self.wordList) -1)]
        self.hiddenMysteryWord = ["-" for i in range(len(self.mysteryWord))]
        self.correctGuesses = 0
        self.guessCount = self.totalGuesses = math.floor(225 * (1/-(len(self.mysteryWord)+4)**2) + 13)
        self.BindKeyboard()
    
    def BindKeyboard(self):
        for c in alphabet:
            self.bind(f'<KeyPress-{c}>', self.RemoteGuess)
    
    def UnBindKeyboard(self):
        for c in alphabet:
            self.unbind(f'<KeyPress-{c}>')
    
    def RemoteGuess(self, event):
        self.unbind(f"<KeyPress-{event.char}>")
        self.Guess((event.char).upper())

    def MainWindow(self):
        font = CTK.CTkFont(family="Arial Black", size=38, weight=Font.NORMAL)
        font1 = CTK.CTkFont(family="Arial Black", size=15, weight=Font.NORMAL)
        font2 = CTK.CTkFont(family="Arial Black", size=32, weight=Font.BOLD)
        self.HotBar.pack(side="top", fill="x")
        self.TopFrame.pack(side="top", fill="both")
        self.BottomFrame.pack(side="bottom", pady=12)   
        self.WordGen = CTK.CTkButton(self.HotBar, width=80, height=24, font=font1, text="NEW WORD", command=self.GenerateNew)
        self.WordGen.pack(side="left", padx=6, pady=6)
        self.GuessCounter = CTK.CTkLabel(self.HotBar, width=40, height=40, font=font2, text=self.guessCount, text_color=self.HueCalc())
        self.GuessCounter.pack(side="left", padx=174, pady=6, anchor="n")
        self.SettingsBtn = CTK.CTkButton(self.HotBar, width=60, height=24, text="SETTINGS", font=font1, command=self.SettingsMenu)
        self.SettingsBtn.pack(side="right", padx=6, pady=6)
        self.WordEty = CTK.CTkEntry(self.TopFrame, width=540, height=70, border_color="gray23", font=font, justify="center")
        self.WordEty.pack(side="top", pady=14, padx=20)
        self.WordEty.insert(0, self.hiddenMysteryWord)
        self.WordEty.configure(state="disabled")
        self.MapButtons(self.BottomFrame)
    
    def ComboCallBack(self, choice):
        nums = [x for x in choice if x.isdigit()]
        num = "".join(nums)
        self.wordSize = int(num)

    def SettingsMenu(self):
        self.geometry("828x412")
        for key in self.keyDict.values():
            key.configure(state="disabled")
        self.WordGen.configure(state="disabled")
        self.SettingsBtn.configure(state="disabled")
        font = CTK.CTkFont(family="Arial Black", size=9, weight=Font.NORMAL)
        font1 = CTK.CTkFont(family="Arial Black", size=15, weight=Font.NORMAL)
        font2 = CTK.CTkFont(family="Arial Black", size=13, weight=Font.NORMAL)
        font3 = CTK.CTkFont(family="Arial", size=10, weight=Font.NORMAL)
        self.RightFrame.pack(side="right", fill="y")
        self.ChangeKeyLayoutBtn = CTK.CTkButton(self.RightFrame, width=60, height=24, text=self.layouts[self.currentLayout].upper(), font=font1, command=self.ChangeKeyLayout)
        self.ChangeKeyLayoutBtn.pack(side="top", padx=10, pady=30)
        self.DisclaimerLbl = CTK.CTkLabel(self.RightFrame, font=font3, text="Disclaimer: Words with more then 7\nletters are much harder to guess")
        self.DisclaimerLbl.pack(side="top", padx=10, pady=2)
        self.ComboBox = CTK.CTkComboBox(self.RightFrame, font=font2, dropdown_font=font, values=[str(x) + " letters" for x in range(5, 13)], command=self.ComboCallBack, width=120, height=24, corner_radius=12, button_color="#1f6aa5", state="readonly")
        self.ComboBox.pack(side="top", padx=10, pady=2)
        self.ConfirmBtn = CTK.CTkButton(self.RightFrame, width=60, height=24, text="DONE", font=font1, command=self.CloseMenu)
        self.ConfirmBtn.pack(side="bottom", padx=10, pady=20)

    def ChangeKeyLayout(self):
        self.currentLayout += 1
        try:
            self.keysList = keyboardLayouts[self.currentLayout]
        except IndexError:
            self.currentLayout = 0
            self.keysList = keyboardLayouts[self.currentLayout]
        self.ChangeKeyLayoutBtn.configure(text=self.layouts[self.currentLayout].upper())
        self.UnpackWidget(self.BottomFrame)
        self.MapButtons(self.BottomFrame)
        for key in self.keyDict.values():
            key.configure(state="disabled")

    def CloseMenu(self):
        for key in self.keyDict.values():
            key.configure(state="normal")
        self.WordGen.configure(state="normal")
        self.UnpackWidget(self.RightFrame)
        self.RightFrame.pack_forget()
        self.SettingsBtn.configure(state="normal")
        self.geometry(self.defaultGeometry)
        self.GenerateNew()
    
    def HueCalc(self):
        red = math.floor(90*math.cos((math.pi/self.totalGuesses)*self.guessCount) + 165)
        green = math.floor(-90*math.cos((math.pi/self.totalGuesses)*self.guessCount) + 165)
        blue = math.floor(-33*math.cos(((2*math.pi)/self.totalGuesses)*self.guessCount) + 33)
        return '#%02x%02x%02x' % (red, green, blue)

    def GenerateNew(self):
        self.GenerateWordList(self.wordSize)
        self.GenMysteryWord()
        self.WordEty.configure(state="normal")
        self.WordEty.delete(0, "end")
        self.WordEty.insert(0, self.hiddenMysteryWord)
        self.WordEty.configure(state="disabled")
        for button in self.keyDict.values():
            button.configure(state="normal", fg_color="#1f6aa5")
        self.guessCount = self.totalGuesses
        self.SmartUnpack(self.resultLabel)
        self.GuessCounter.configure(text=self.guessCount, text_color=self.HueCalc())
        
    def UnpackWidget(self, parent):
        for widget in parent.winfo_children():
            widget.pack_forget()

    def SmartUnpack(self, widget):
        if widget.winfo_ismapped:
            widget.pack_forget()

    def MapButtons(self, master):
        self.keyDict = {}
        font = CTK.CTkFont(family="Arial Black", size=24, weight=Font.BOLD)
        for row in self.keysList:
            frame = CTK.CTkFrame(master, fg_color="transparent")
            frame.pack(side="top", expand=True, anchor="n")
            for key in row:
                button = CTK.CTkButton(frame, width=60, height=60, font=font, text=key, command=lambda x = key: self.Guess(x))
                button.pack(side="left", padx=2, pady=2)
                self.keyDict[key] = button
        for key in self.keyDict.values():
            key.configure(state="normal")

    def EntryConfig(self):
        self.WordEty.configure(state="normal")
        self.WordEty.delete(0, "end")
        self.WordEty.insert(0, self.hiddenMysteryWord)
        self.WordEty.configure(state="disabled")
    
    def Guess(self, key):
        if self.guessCount >= 1:
            guess = False
            for i in range(len(self.mysteryWord)):
                if key == self.mysteryWord[i].upper():
                    guess = True
                    self.hiddenMysteryWord[i] = key
                    self.correctGuesses += 1
            self.EntryConfig()
            if guess:
                self.keyDict[key].configure(fg_color="green", state="disabled")
            else:
                self.keyDict[key].configure(fg_color="gray32", state="disabled")
                self.guessCount -= 1
                self.GuessCounter.configure(text=self.guessCount, text_color=self.HueCalc())
        if self.guessCount < 1:
            guess = False
            for i in range(len(self.mysteryWord)):
                if key == self.mysteryWord[i].upper():
                    guess = True
                    self.hiddenMysteryWord[i] = key
                    self.correctGuesses += 1
            self.EntryConfig()
            if guess:
                self.keyDict[key].configure(fg_color="green", state="disabled")
            else:
                self.keyDict[key].configure(fg_color="gray32", state="disabled")
            self.resultLabel.configure(text=f"YOU RAN OUT OF GUESSES! THE WORD WAS, '{self.mysteryWord.upper()}'")
            self.resultLabel.pack(side="bottom", pady=2)
            self.WordGen.configure(state="disabled")
            self.WordEty.configure(text_color="red")
            self.UnBindKeyboard()
            for key in self.keyDict.values():
                key.configure(state="disabled")
            self.after(3200, lambda: self.SmartUnpack(self.resultLabel))
            self.after(3200, self.GenerateNew)
            self.after(3210, lambda: self.WordGen.configure(state="normal"))
            self.after(3210, lambda: self.WordEty.configure(text_color="snow"))
        if self.correctGuesses == len(self.mysteryWord):
            self.resultLabel.configure(text=f"CONGRATUALTIONS YOU GUESSED THE WORD!")
            self.resultLabel.pack(side="bottom", pady=2)
            self.WordEty.configure(text_color="green")
            for key in self.keyDict.values():
                key.configure(state="disabled")
            self.UnBindKeyboard()
            self.after(3200, lambda: self.SmartUnpack(self.resultLabel))
            self.after(3200, self.GenerateNew)
            self.after(3210, lambda: self.WordGen.configure(state="normal"))
            self.after(3210, lambda: self.WordEty.configure(text_color="snow"))
            
    
    def GenerateWordList(self, wrdSize = 5):
        #https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt
        #https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
        #https://www.mit.edu/~ecprice/wordlist.10000
        #https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw/6bfa15d263d6d5b63840a8e5b64e04b382fdb079/valid-wordle-words.txt
        #https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/d9cddf5e16140df9e14f19c2de76a0ef36fd2748/wordle-La.txt
        rawWords = requests.get(wordDirectories[wrdSize-1])
        fomratedWords = str(rawWords.content)
        self.wordList = []
        if "\\n" in fomratedWords:
            self.wordList = fomratedWords.split("\\n")
        else:
            for word in fomratedWords.split(","):
                self.wordList.append(word[1:7])


game = HangMan()
game.mainloop()