'''
Created on Jul 1, 2013

@author: Ante Odic
'''

import numpy


def generate_vignettes(numElementsPerSilos, numVignettes, numElemsPerVignettes, numElementAppearances):
    
    # BASIC PARAMETERS
    # number of silos in the dataset
    numSilos = len(numElementsPerSilos)         
    # number of all elements (statements) in dataset
    numElements = sum(numElementsPerSilos)      
    # number of vignettes that were generated
    numGeneratedVignettes = numVignettes        
    print "jjj" 
	
    # MATRICES FOR RESULTS AND TRACKING
    # incidence matrix  (result) 
    indMat = numpy.zeros((numElements,numVignettes))  
    # indices of elements in siloes               
    indElemsInSilos = numpy.zeros((numElemsPerVignettes,1))  
    # max number of elements per silos     
    maxElemsPerSilo = max(numElementsPerSilos)           
    # number of appearances of each element         
    numAppearances = numpy.zeros((numSilos,maxElemsPerSilo))  
    # which element is still remaining    
    remainingElems = numpy.zeros((numSilos,maxElemsPerSilo+1))  
    # which silo is still remaining  
    remainingSilos = numpy.zeros(numSilos+1)                 
    # indices of elements     
    currentElemIndices = numpy.zeros((numElemsPerVignettes,1))    
    
    # INITIALIZE REMAININGELEMS
    for i in range(numSilos):
        remainingElems[i,0]=numElementsPerSilos[i]
        remainingElems[i,1:numElementsPerSilos[i]+1] = range(1,numElementsPerSilos[i]+1)
        
        
    
    # INITIALIZE REMAININGSILOS
    remainingSilos[0]=numSilos
    remainingSilos[1:]=range(1,numSilos+1)
    remainingSilos.T
    
    # VIGNETTES FOR DJANGO
    vignetteDict = {}
    silosNames = ['A','B','C','D','E','F','G','H','I','J','K','L']
    
    # START CREATING VIGNETTES
    for j in range(numVignettes):
        # get number of remaining silos 
        currentNumSilos = remainingSilos[0]   
        # if there are less than 4 remaining silos exit         
        if currentNumSilos < 4:                         
            numGeneratedVignettes = j
            return  {"indMat":indMat,"numGeneratedVignettes":numGeneratedVignettes}
        # get permutation
        currPerm=numpy.random.permutation(range(int(currentNumSilos)))
        # take first n elems in permutation list
        currCutPerm = currPerm[0:numElemsPerVignettes]
        # from remainingSilos take those from permutation list                
        currSilos = [remainingSilos[i+1] for i in currCutPerm]        
        
        #import pdb; pdb.set_trace()
        
        # SELECT SILOS AND ELEMENTS
        for k in range(numElemsPerVignettes):
            currElemPerm = numpy.random.permutation(range(int(remainingElems[currSilos[k]-1,0])))
            indElemsInSilos[k] = remainingElems[currSilos[k]-1,currElemPerm[0]+1]
            numAppearances[currSilos[k]-1,int(indElemsInSilos[k])-1] +=1
           
        # MARK SELECTED ELEMENTS IN RESULT MATRIX
        for k in range(numElemsPerVignettes):
            currentElemIndices[k]=sum(numElementsPerSilos[0:int(currSilos[k])-1])+indElemsInSilos[k]
        for ind in currentElemIndices: 
            indMat[int(ind)-1,j] = 1
            
        # UPDATE TRACKING MATRICES
        for k in range(numElemsPerVignettes):
            siloIndex = int(currSilos[k])
            elemIndex = int(indElemsInSilos[k])
            
            if numAppearances[siloIndex-1,elemIndex-1]==numElementAppearances:
                remainingElems[int(siloIndex)-1,0] -= 1
                indToRemove = numpy.where(numAppearances[siloIndex-1,:]==numElementAppearances)[0][0]+1
                posToRemove = numpy.where(remainingElems[siloIndex-1,1:]==indToRemove)[0][0]+1
                
                remainingElems[siloIndex-1, posToRemove:-1] = remainingElems[siloIndex-1, posToRemove+1:]
                remainingElems[siloIndex-1, -1] = -1
                numAppearances[siloIndex-1,elemIndex-1]=-1
            
                if remainingElems[siloIndex-1,0]==0:
                    remainingSilos[0]-=1
                    indToRemove = numpy.where(remainingSilos[1:]==siloIndex)[0][0]
                    remainingSilos[indToRemove+1:-1] = remainingSilos[indToRemove+2:]     
                    remainingSilos[-1]=-1
        
        # FILL VIGNETTEDICT
        currVignetteElements=[]
        for k in range(numElemsPerVignettes):           
            code = silosNames[int(currSilos[k])-1] + str(int(indElemsInSilos[k][0]))
            currVignetteElements.append( code)
        vignetteDict[str(j+1)]= currVignetteElements
                    
    numGeneratedVignettes = j
    return  {"indMat":indMat,"numGeneratedVignettes":numGeneratedVignettes,"vignetteDict":vignetteDict}

#rezu= generate_vignettes([6,6,6,6,6,6,6], 6, 4, 5)

#a=4

