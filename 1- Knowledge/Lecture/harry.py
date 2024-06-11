from logic import *

rain = Symbol("rain") # it is raining 
hagrid = Symbol("hagrid") # Harry visited Hagrid 
dumbledore = Symbol("dumbledore") # Harry visited Dumbledore 

sentence = And(rain, hagrid) 
print(sentence.formula())

first = Implication(Not(rain), hagrid) 
second = Or(hagrid, dumbledore) 
third = Not(And(hagrid, dumbledore))
fourth = dumbledore
print(first.formula()) 
print(second.formula()) 
print(third.formula()) 
print(fourth.formula())

knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid, dumbledore),
    Not(And(hagrid, dumbledore)),
    dumbledore
)

print(model_check(knowledge, rain))
