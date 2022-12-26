import numpy as np
import operator
import sys
import os

# week_10 수업자료에서 가져왔습니다.
def classify(inX, dataSet, labels, k):
    # 거리 계산 (Euclidian distance)
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = np.sum(np.sum(sqDiffMat, axis=1), axis=1) # 주어진 axis로 배열 요소들의 합계 반환
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort() # 배열 소팅 후 인덱스 반환
    classCount = {}
    for i in range(k): # 가장 짧은 거리를 투표
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), # 아이템 정렬
        key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

def readTxt(txtFile):
    result = np.empty((0, 32), int)
    with open(txtFile, "r") as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            result = np.append(result, np.array([list(map(int, line))]), axis=0)
    return result

def readDigits(dirName):
    assert (os.path.isdir(dirName))
    for (path, dir, files) in os.walk(dirName):
        resultDatas = np.empty((0, 32, 32), int)
        resultLabels = []
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.txt':
                label = filename.split('_')[0]
                array = readTxt(f"{path}/{filename}")
                resultDatas = np.append(resultDatas, np.array([array]), axis=0)
                resultLabels.append(label)
    return (resultDatas, np.array(resultLabels))

def main():
    trainingDigits = sys.argv[1]
    testDigits = sys.argv[2]
    (trainDatas, labels) = readDigits(trainingDigits)
    (testDatas, answers) = readDigits(testDigits)

    for k in range(20):
        result = []
        for i in range(len(answers)):
            result.append(classify(testDatas[i], trainDatas, labels, k+1))
        result = np.array(result)
        correct = result == answers
        print(100 - np.count_nonzero(correct))

if __name__ == "__main__":
    main()
