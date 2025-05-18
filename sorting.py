import math
import heapq
def rishabSort(array):
    arrLength = len(array)
    if arrLength == 1: return array
    minVal = array[0]
    maxVal = array[0]
    for number in array:
        if number < minVal: minVal = number
        if number > maxVal: maxVal = number
    range = maxVal - minVal + 1
    sortedArray = []

    K = [0] * range
    if (range <= 2 * arrLength) or (range <= arrLength * (arrLength.bit_length())):  
        for x in array:
            K[x - minVal] += 1
        sortedArray = []
        for i, count in enumerate(K):
            if count:
                value = minVal + i
                sortedArray.extend([value] * count)
        return sortedArray

    freqMap = {}
    for x in array:
        freqMap[x] = freqMap.get(x, 0) + 1
    d = len(freqMap)  

    if d * (d.bit_length()) <= (0.9 * arrLength):
        uniqueValues = sorted(freqMap.keys())
        for values in uniqueValues:
            sortedArray.extend([values] * freqMap[val])
        return sortedArray

    threshold = arrLength / max(math.log2(arrLength), 1)
    heavyValues = [values for values, count in freqMap.items() if count >= threshold]
    heavyValues.sort()
    heavyOutput = []
    heavyCount = 0
    for values in heavyValues:
        heavyOutput.extend([values] * freqMap[values])
        heavyCount += freqMap[values]
        freqMap.pop(values, None)
    remaining = arrLength - heavyCount

    cluster = []
    remOutput = []
    if remaining > 0:
        rKeys = sorted(freqMap.keys())
        rTotal = sum(freqMap[v] for v in rKeys)
        target = 0.9 * rTotal
        cumulative = 0
        clusterStart = rKeys[0]
        clusterEnd = clusterStart
        for v in rKeys:
            cumulative += freqMap[v]
            clusterEnd = v
            if cumulative >= target: break

        clusterSize = clusterEnd - clusterStart + 1
        if cumulative >= target and clusterSize < (rKeys[-1] - rKeys[0] + 1) * 0.5:
            clusterCounts = [0] * clusterSize
            mapKeys = list(freqMap.keys())
            for values in mapKeys:
                if (clusterStart <= values)  and (values <= clusterEnd):
                    clusterCounts[values - clusterStart] += freqMap[values]
                    freqMap.pop(values)  
            for i, count in enumerate(clusterCounts):
                if count:
                    cluster.extend([clusterStart + i] * count)
        
        if freqMap:
            outliers = []
            for v, count in freqMap.items():
                outliers.extend([v] * count)
            outliers.sort()
            remOutput = outliers
    finalReturn = []
    
    mergedAll = [heavyOutput, cluster, remOutput]
    sortedAll = [lst for lst in mergedAll if lst]
    if not sortedAll:
        return []  
    
    heap = []
    for x, lists in enumerate(sortedAll):
        heapq.heappush(heap, (lists[0], x, 0))
    while heap:
        x,y,z = heapq.heappop(heap)
        finalReturn.append(x)
        if z+1 < len(sortedAll[y]):
            heapq.heappush(heap, (sortedAll[y][z+1], y, z+1))
    return finalReturn
