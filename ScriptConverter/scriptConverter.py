import os
import sys
import re

def writeCloseLabel(outputScript):
    outputScript.write('    return\n')
    outputScript.write('\n')

def writeScript(outputScript, intend, line):
    intendStr = ''
    for i in range(0, intend):
        intendStr = intendStr + '    '

    if (line[0:1] == '('):
        outputScript.write(intendStr + '\"' + line + '\"\n')
    else:
        outputScript.write(intendStr + '아이리 \"' + line + '\"\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('usage: python ' + sys.argv[0] + ' scriptName')
        exit()

    inputScript = open(sys.argv[1], mode='r', encoding='utf8')
    outputScript = None

    exportDirName = "export"

    if not os.path.exists(exportDirName):
        os.makedirs(exportDirName)

    # mode = 0 : 연속 모드
    # mode = 1 : 랜덤 모드
    # mode = 2 : 액션 모드
    mode = 0

    categoryNum = -1
    scriptNum = 0
    actionNum = 0
    t = '    '

    inputArray = inputScript.readlines()

    for line in inputArray:
        if (line[:3] == '---'):
            if outputScript != None:
                writeCloseLabel(outputScript)
                outputScript.close()
                outputScript = None
        
        elif (line[:1] == '<') and outputScript == None:
            # 파일의 시작. 태그 내용 그대로 파일 이름으로 작성
            print (line[:-1])
            outputScript = open('export/' + line[1:-2] + '.rpy', mode='w', encoding='utf8')
            scriptNum = 0

            if (line[-4:-2] == u'미만'):
                mode = 1
            else:
                mode = 0

            if mode == 0:
                if line[:-1] == u'<도입부>':
                    outputScript.write('# Intro\n')
                    outputScript.write('label start:\n')

                if line[1:4] == u'호감도':
                    outputScript.write('# lovePoint ' + line.split(' ')[1] + ' event\n')
                    outputScript.write('label event_' + str(categoryNum) + ':\n')

            if mode == 1:
                if line[1:4] == u'호감도':
                    categoryNum = categoryNum + 1
                    outputScript.write('# dialog_' + str(categoryNum) + ' : lovePoint < ' + line.split(' ')[1] + '\n')

        elif (line[:1] == '['):
            if (re.match(r'[0-9]', line[1:2])):
                print ('matched: ' + line)
            else:
                # 지시 사항은 그대로 주석으로 출력
                outputScript.write('    #' + line[:-1] + '\n')

        elif (line[:1] == '<'):
            # 액션 모드로 전환
            writeCloseLabel(outputScript)
            outputScript.write('# ' + line[1:-2] + '\n')

            mode = 2
        
            actionNum = actionNum + 1
            scriptNum = 0

        elif (line[:1] == '-'):
            if (mode == 0):
                # 연속 모드에서는 대사를 이어갑니다
                writeScript(outputScript, 1, line[1:-1])
            elif (mode == 1):
                # 랜덤 모드에서는 새 함수를 생성합니다
                if (scriptNum != 0):
                    writeCloseLabel(outputScript)

                outputScript.write('label dialogue_' + str(categoryNum) + '_' + str(scriptNum) + ':\n')
                writeScript(outputScript, 1, line[1:-1])
                scriptNum = scriptNum + 1

            elif (mode == 2):
                if (scriptNum != 0):
                    writeCloseLabel(outputScript)

                outputScript.write('label action_' + str(categoryNum) + '_' + str(actionNum) + '_' + str(scriptNum) + ':\n')
                writeScript(outputScript, 1, line[1:-1])
                scriptNum = scriptNum + 1

            else:
                print ('Script Error! unknown mode = ' + str(mode))
        
        elif (line[0] == '\n'):
            # 빈 줄을 그대로 추가합니다
            if (outputScript != None):
                outputScript.write('\n')

        else:
            # 그냥 대사를 이어갑니다.
            writeScript(outputScript, 1, line[:-1])

    inputScript.close()
    if (outputScript != None):
        writeCloseLabel(outputScript)
        outputScript.close()
        outputScript = None
