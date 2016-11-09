# Author: <put your name here>
# HW 1.3.2

# TODO: Enter your name here.
author = 'Glover Ruiz'

print ('\n AP CS Principles  - hw 1.3.2 - ' + author + '\n')



#---------------------------------------------------------------
#this is a function definition, note the "def" key word
def add_tip(total, tip_percent): 
    ''' Return the total amount including tip'''
    #input: leg1,leg2 - sides of the triangle
    #output: returns the hyp, calculated using Pythagora's
    #hint: number**0.5 takes the squre root of a number
    
    total_owe = 0
    # ---------------
    # add your code here. 
    # one liner return fuction. Use when response is simple.
    #return (total + total * tip_percent)

    # define a variable to hold the total bill including the tip
    tip = tip_percent * total
    total_owe =  total + tip
    
    # ---------------
    return total_owe
    
#---------------------------------------------------------------    
#this is a function definition, note the "def" key word
def hyp(leg1,leg2):
    '''returns the hyp given the sides'''
    
    #input: leg1,leg2 - sides of the triangle
    #output: returns the hyp, calculated using Pythagora's
    #hint: number**0.5 takes the squre root of a number
    
    hyp = 0
    # ---------------
    # add your code here. 
    # use "hyp" as the calculation variable
    
    hyp = (leg1**2 + leg2**2)**0.5 
    
    # ---------------
    return hyp
    
    
#---------------------------------------------------------------    
#this is a function definition, note the "def" key word    
def mean(a,b,c):
    ''' Calculates the mean of 3 vales. '''
    
    #input: a,b,c - values used to calculate the mean
    #output: returns mean value of input numbers
    #hint: divide by 3.0 to get a float
    
    mean_value = 0
    #-------------------
    # enter your code here
    #mean_value = (a + b + c)/3  #incorrect as will truncate to int. 
    mean_value = (a + b + c)/3.0  # adding the decimal point to return float
    
    #--------------------
    return mean_value
    


#---------------------------------------------------------------
#this is a function definition, note the "def" key word   
def perimeter( base, height):
    ''' Returns the perimeter of a triangle'''
    
    #input: base of the triangle, height of the triangle
    #output: returns perimeter of the triangle
    #hint: make sure the output is a float. Multiply by 1.0 if necessary
    
    perim = 0
    #-------------------
    # enter your code here
    
    
    
    #--------------------
    return (base + 2.0 * height)
    
    
      
# Start of the assignment here. 

#-----------------------------------------------------------------------------
#Question: 1 - calculate total price including tip, use your own numbers
# this question is given as a guide

# define a variable to hold the bill amount
total = 65.25

# define a variable to hold to tip, in percent e.g. 0.1 for a 10% tip
tip_percent = 0.1

# define a variable to hold the total bill including the tip
tip = tip_percent * total
total_with_tip =  total + tip

# print the result to screen with the message "you owe $ dollaramount."
print(' you owe $ ' + str(total_with_tip))



#-----------------------------------------------------------------------------
#Question: 2 - implement a function to calculate the tip, compare the script 
# based  result whit the function based result to validate the function

print(' you owe $ ' + str(add_tip(total,tip_percent)))



#-----------------------------------------------------------------------------
#Question: 3 - implement a function to calculate mean of 3 variables'
#test with your own values, submit the answer using (12.2, 13.3, 14.4)

a,b,c = 12.2, 13.3, 14.4
print (' the mean value is ' + str(mean(a,b,c)))

#-----------------------------------------------------------------------------
#Question: 4 - implement a function to calculate the hyp of a triangle'
#test with your own values, submit the answer using (10,20)

side_1,side_2  = 3,4
print (' the hyp value is ' + str(hyp(side_1,side_2)))


#-----------------------------------------------------------------------------
#Question: 5 - implement a function to calculate the perimeter of a triangle
#test with your own values, submit the answer using ()

the_base,the_height = 2,3
print(' the perimeter value is ' + str(perimeter(the_base,the_height)))

print('...Homework completed...')