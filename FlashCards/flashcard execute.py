import random
import os.path
import sys
from os import listdir
sep = ','
defaultWeight = 10
incremento = 1
decrésimo = -1
minimumWeight = 1
maximumWeight = 20
defaultFlashCard = ['help','hiragana']
extension = '.dic'


def addDic(dic, key, filename):
    with open(filename, "a", encoding='utf-8') as f:
        f.write(key + sep + dic[key][0] + sep + str(dic[key][1]) + "\n")
        f.close()                                                             #added the close(), but I haven't tested for errors yet
def readDic(filename):
    if os.path.isfile(filename) == False:
        return {}
    with open(filename, encoding='utf-8') as f:
        dic = {}
        for line in f:
            if line != '':
               line = line.rstrip()
               values = line.split(sep)
               dic[values[0]] = [values[1],int(values[2])]
        f.close()
        return(dic)
def writeDic(dic, fileName):
    with open(fileName, "w", encoding='utf-8') as f:
        for key in dic.keys():
            f.write(key + sep + dic[key][0] + sep + str(dic[key][1]) + "\n")
        f.close()
def createNewFlashCard(flashCardName): #creates or uploads a file; does not return value
   for value in defaultFlashCard:#does not allow changes in the default flashCard
      if flashCardName == value:
         print('Sorry, but you cannot make changes on this flashcard.')
         print('restarting the program')
         return main()
   fileName = flashCardName + extension
   if os.path.isfile(fileName) == False:
      print ('this file does not exist. Do you want to create it?')
      if input() != 'yes':
         print('restarting the program.')
         return main()                                              #does this work???
       # else:
      #      return {}
   dic = readDic(fileName)
   while True:
      print('What is the key?')
      key = input()
      if key == 'stop' or key == 'quit':
            return
      print ('What is the value?')
      value = input()
      dic[key] = [value,defaultWeight]
      addDic(dic, key, fileName)

def testFlashcard(flashCardName):
   fileName = flashCardName + extension
   if os.path.isfile(fileName) == False:
      createNewFlashCard(flashCardName)
      print('Do you want to play this flashcard?')
      if input() != 'yes':
         print('restarting the program')
         return main()

   dic = readDic(fileName)
   if dic == {}:
      print('File is empty, restarting the program.')
      return main()
   print ('how many times do you want to play?')
   times = int(input())
   stillTimes = times
   correctAnswers = 0
   while times > 0:
      testLetterList = testLetter(dic)
      dicList = corrigir(dic,testLetterList[0],testLetterList[1],testLetterList[2])
      correctAnswers += dicList[0]
      dic[testLetterList[2]][1] = dicList[1]
      times -= 1

   writeDic(dic, fileName)
   correctAnswersPercentage = round(correctAnswers/stillTimes*100)
   if correctAnswersPercentage >= 80:
      print(f'Good job! You got {correctAnswersPercentage}% of the questions corrrect!')
   else:
      print(f'You got {correctAnswersPercentage}% of the questions correct... Got to train more...')
      return

def letterGenerator(dic):
   somaDePeso = 0
   for key in dic.keys():
      somaDePeso += dic[key][1]    
   randomNumber = random.randint(1,somaDePeso)
   peso = 0
   for key in dic.keys():
        if 0 <= randomNumber <= dic[key][1]+peso:
            return key
        else:
            peso += dic[key][1]

def testLetter (dic): #returns a list with the answer, the actual answer and the key
    letra = letterGenerator(dic)
    actualAnswer = dic[letra][0]
    print('Which letter is this?')
    sys.stdout.flush()
    sys.stdout.buffer.write(letra.encode('utf8'))
    print()
    answer = input().strip()
    return [answer,actualAnswer,letra]

def corrigir(dic,answer,actualAnswer,key): #regulates keys' weights/checks if one missed or not
   if answer == actualAnswer:
      print("Congratulations, you are correct!")
      if dic[key][1] > minimumWeight:
         dic[key][1] += decrésimo
      return [1,dic[key][1]]

   else:
      print(f"unfortunately, you are wrong... The correct answer is {actualAnswer}")
      if dic[key][1] < maximumWeight:
         dic[key][1] += incremento
      return [0,dic[key][1]]

def reset():
   fileNameList = os.listdir()
   for fileName in fileNameList:
         if fileName.endswith(extension):
            dic = readDic(fileName)
            for key in dic.keys():
               dic[key][1] = defaultWeight
            writeDic(dic,fileName)

def main (firstTime = 0):
   print('See file "help" for help')
   if len(sys.argv) > 1 and firstTime == 1:
      testFlashcard(sys.argv[1])
      return main()
      
   print('Do you want to create a new flashcard or upload a flashcard?')
   response = input()
   if response == 'yes':
        print('What is the name of the Flashcard?')
        createNewFlashCard(input())
   elif response == 'reset':
      print('are you sure you want to reset all weights?')
      if input() == 'yes':
         reset()
      else:
         print('restarting the program')
         return main()

   print('Ok, which flashcard do you want to see?')
   testFlashcard(input())
   print('restarting the program.')
   return main()

if __name__ == '__main__': main(1)