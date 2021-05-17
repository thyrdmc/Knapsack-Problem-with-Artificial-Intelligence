  
from simpleai.search.viewers import WebViewer, ConsoleViewer
from simpleai.search import SearchProblem, genetic, hill_climbing , hill_climbing_random_restarts
import random

my_viewer = ConsoleViewer()

values = [ ]
weights = [ ]

class KnapsackProblem(SearchProblem):     
        
        def __init__(self, itemsNumber, capacity, weights, values, initial_state=None):              
            super(KnapsackProblem, self).__init__(initial_state)
            self.itemsNumber = itemsNumber
            self.capacity = capacity
            self.weights = weights
            self.values = values
       
        def actions(self,state):
            List = [ ]
            NeighborsList =[ ]  

            for i in state:
                List.append(int(i))        

            NeighborsList.append(List)

            for i in range(0,itemsNumber-1):
                while True:
                    randomState = [ ]
                    weight = 0 
                    
                    for i in range(0,itemsNumber):
                        randomState.append(random.randint(0,1))
                        if(randomState[i] == 1):
                            weight = weight + weights[i]
                                                                      
                    if(weight<=capacity):
                        NeighborsList.append(randomState)
                        break    
                           
            return NeighborsList
        
        def result(self, state, action):
            actionState = ''.join(str(e) for e in action)
            actionState  = actionState .replace("[","")
            actionState  = actionState .replace("]","")
            actionState  = actionState .replace(",","")
                       
            if(self.value(actionState) > self.value(state) ):
                return actionState
            else:
                return state 
             
        def generate_random_state(self): 
            while True:               
                randomState = [ ]
                
                for i in range(0,self.itemsNumber):
                    randomState.append(random.randint(0,1))
                               
                if self.valid(randomState):
                    break

            return randomState
        
        def crossover(self, state0, state1): 
            count = 1
            randomIndex = random.randint(1, itemsNumber-1)
            child = state0[:randomIndex ] + state1[randomIndex :]
            
            while not self.valid(child):
                if count > itemsNumber:
                    return state0
                count += 1
                randomIndex  = random.randint(1, itemsNumber-1)
                child = state0[:randomIndex ] + state1[randomIndex :]

            return child    
        
        def mutate(self, state):              
            valid = False 
            randomIndex0 = 0
            randomIndex1 = 0 
            count = 0
            preState = state 
            while not valid:
                state = preState
                if count > itemsNumber:
                    break
                randomIndex0 = random.randint(0, itemsNumber-1)
                randomIndex1 = random.randint(0, itemsNumber-1)

                if state[randomIndex0]+state[randomIndex1] == 1:
                    if not state[randomIndex0]:
                        state[randomIndex0] = 1
                        state[randomIndex1] = 0
                    else:
                        state[randomIndex0] = 0
                        state[randomIndex1] = 1
                    valid = self.valid(state)
                    count += 1
            return state
        
        def value(self, state):
            value = 0

            if(type(state) == list):
                for index, item in enumerate(state):
                    if item == 1:
                        value += self.values[index]
            else:
                x = 0
                for i in state:
                    if(i == "1"):
                        value = value + self.values[x]
                    x +=1

            return value

        def _weight(self, state):
            weight = 0
            if(type(state) == list):
                for index, item in enumerate(state):
                    if item == 1:
                        weight += self.weights[index]
            else:
                x = 0
                for i in state:
                    if(i == "1"):
                        weight += self.weights[x]
                    x+=1
                    
            return weight

        def valid(self, state):
            if self._weight(state) > capacity:
                return False
            return True

capacity = int(input("Please Enter Knapsack Capacity : " ))  
itemsNumber = int(input("Please Enter Number Of Items : " )) 

for i in range(0, itemsNumber):
    weight = int(input("Please Enter Weight of Item " + str(i+1) + ": ")) 
    weights.append(weight)

    value  = int(input("Please Enter Value of Item " + str(i+1) + ": ")) 
    values.append(value)

print()
print("Write 1 for Genetic Algorithm")
print("Write 2 for Hill Climbing Algorithm")
print("Write 3 for Hill Climbing Random Restart Algorithm")
print()

algorithm_selection = int(input("Please Choose One of Algorithms Above: "))  
print()

if(algorithm_selection == 1):     
    problem =  KnapsackProblem (itemsNumber, capacity, weights, values, initial_state= None) 

    iterations_limit = int(input("Please Enter Itertions Limit: ")) 
    mutation_chance = float(input("Please Enter Mutation Chance: ")) 

    result = genetic(problem, population_size=itemsNumber, mutation_chance = mutation_chance, iterations_limit = iterations_limit, viewer=my_viewer)

    print()
    print ("Final Path: "+ str(result.path()))
    print ('Weight = ' + str(problem._weight(result.path()[0][1])))
    print ('Value = ' + str(problem.value(result.path()[0][1])))

elif(algorithm_selection == 2):
    
    while True:
        randomState = [ ] 
        weight = 0 
        for i in range(0,itemsNumber):
            randomState.append(random.randint(0,1)) 
            if(randomState[i] == 1): 
                weight = weight + weights[i] 
        if(weight<=capacity):
            break
    
    initial = ''.join(str(e) for e in randomState) 

    initial = initial.replace("[","") 
    initial = initial.replace("]","") 
    initial = initial.replace(",","")  

    problem =  KnapsackProblem (itemsNumber, capacity, weights, values, initial_state= initial)
    iterations_limit = int(input("Please Enter Itertions Limit: ")) 
    result = hill_climbing(problem, iterations_limit, viewer=my_viewer) 

    print()
    print ("Final State: "+ result.state)        
    print ('Weight = ' + str(problem._weight(result.state)))
    print ('Value = ' + str(problem.value(result.state)))
    print()

elif(algorithm_selection == 3):
    while True:
        randomState = [ ]
        weight = 0 
        for i in range(0,itemsNumber):
            randomState.append(random.randint(0,1))
            if(randomState[i] == 1):
                weight = weight + weights[i]
        if(weight <= capacity):
            break

    initial = ''.join(str(e) for e in randomState)

    initial = initial.replace("[","")
    initial = initial.replace("]","")
    initial = initial.replace(",","")
    
    problem =  KnapsackProblem (itemsNumber, capacity, weights, values, initial_state= initial)
    iterations_limit = int(input("Please Enter Itertions Limit: "))
    restarts_limit =  int(input("Please Enter Restarts Limit: ")) 
    result = hill_climbing_random_restarts(problem, restarts_limit, iterations_limit, viewer=my_viewer)

    print()
    print ("Final State: "+ result.state)        
    print ('Weight = ' + str(problem._weight(result.state)))
    print ('Value = ' + str(problem.value(result.state)))
    print()
        
else:
    print("Wrong Input Please Try Again.")


