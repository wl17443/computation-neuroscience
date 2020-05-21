#for the submission uncomment the submission statements
#see submission.README

from math import *
from submission import *

def energy(weight_matrix, pattern):
    energy = 0
    for i in range(0,11):
        for j in range(0,11):
            energy += pattern[i] * weight_matrix[i][j] * pattern[j]
    return (-1/2) * energy

def seven_segment(pattern):

    def to_bool(a):
        if a==1:
            return True
        return False
    

    def hor(d):
        if d:
            print(" _ ")
        else:
            print("   ")
    
    def vert(d1,d2,d3):
        word=""

        if d1:
            word="|"
        else:
            word=" "
        
        if d3:
            word+="_"
        else:
            word+=" "
        
        if d2:
            word+="|"
        else:
            word+=" "
        
        print(word)

    pattern_b=list(map(to_bool,pattern))

    hor(pattern_b[0])
    vert(pattern_b[1],pattern_b[2],pattern_b[3])
    vert(pattern_b[4],pattern_b[5],pattern_b[6])

    number=0
    for i in range(0,4):
        if pattern_b[7+i]:
            number+=pow(2,i)
    print(int(number))
    print(energy(weight_matrix, pattern))

submission=Submission("angelaluo")
submission.header("Angela Luo")

six=[1,1,-1,1,1,1,1,-1,1,1,-1]
three=[1,-1,1,1,-1,1,1,1,1,-1,-1]
one=[-1,-1,1,-1,-1,1,-1,1,-1,-1,-1]

weight_matrix = [[0 for i in range(11)] for j in range(11)]
patterns = [one, three, six]

def fix_weight(weight_matrix, patterns):
    patterns_size = len(patterns)
    for i in range(0,11):
        for j in range(0,11):
            if i != j:
                sum = 0
                for x in range(0,patterns_size):
                    sum += patterns[x][i] * patterns[x][j]
                weight_matrix[i][j] = (1/patterns_size)*sum
            else: 
                weight_matrix[i][j] = 0 

fix_weight(weight_matrix, patterns)

seven_segment(three)
seven_segment(six)
seven_segment(one)


##this assumes you have called your weight matrix "weight_matrix"
submission.section("Weight matrix")
submission.matrix_print("W",weight_matrix)

def same_pattern(pattern1, pattern2):
    same = True 
    for i in range(0,len(pattern1)):
        if pattern1[i] != pattern2[i]:
            same = False
            break 
    return same

threshold = 0 

def evolve_network(weight_matrix, pattern):
    og_pattern = pattern
    found = False
    while not found:
        new_pattern = [0]*11
        submission.seven_segment(og_pattern)
        submission.qquad()
        submission.print_number(energy(weight_matrix,og_pattern))
        submission.qquad()
        for i in range (0,11):
            sum = 0
            for j in range(0,11):
                sum += weight_matrix[i][j]*og_pattern[j]
            if sum > threshold: new_pattern[i] = 1
            else: new_pattern[i] = -1
        if new_pattern == og_pattern:
            submission.seven_segment(new_pattern)
            submission.qquad()
            submission.print_number(energy(weight_matrix,new_pattern))
            submission.qquad() 
            found = True
        og_pattern = new_pattern


submission.section("Energies of Learned Patterns - One, Three, Six")
submission.print_number(energy(weight_matrix,one))
submission.print_number(energy(weight_matrix,three))
submission.print_number(energy(weight_matrix,six))

print("test1")
submission.section("Test 1")

test=[1,-1,1,1,-1,1,1,-1,-1,-1,-1]

evolve_network(weight_matrix,test)

##for COMSM0027

##where energy is the energy of test
# submission.print_number(energy(weight_matrix,test))

##this prints a space

#here the network should run printing at each step
#for the final submission it should also output to submission on each step

print("test2")
submission.section("Test 2")

test=[1,1,1,1,1,1,1,-1,-1,-1,-1]

evolve_network(weight_matrix,test)

# seven_segment(test)
# submission.seven_segment(test)

##for COMSM0027
##where energy is the energy of test

##this prints a space

#here the network should run printing at each step
#for the final submission it should also output to submission on each step

submission.bottomer()
