from numpy import *

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

def core(dataSet, k, centroids ,distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]  #m为样本数
    clusterAssment = mat(zeros((m,2)))
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf               #minDist为正无穷
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: 
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print(centroids)
        for cent in range(k):#重定位中心点
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment

def kMeans(dataSet,k,centroids):
    myCentroids, clustAssing= core(dataSet,k,centroids)
    myCentroids[isnan(myCentroids)]=0
    return myCentroids
    #show(dataSet, k, myCentroids, clustAssing)
