password = "Praid1@"


    
def checkPasswordRequirenment(text):
    length = False
    case = False 
    character = False 
    space = False
    specialChar = ["!","@","#","$","%","^","&","*","(",")"]
    num = ["1","2","3","4","5","6","7","8","9","0"]
    number = False
    if len(text)>=8:
        length = True
    for x in text:
        if x == " ":
            space = True
        
        if x in num:
            number = True
        elif x in specialChar:
            character = True
        else:
            
            if x == x.upper():
                case = True

    
    if case == True and character == True and space == False and number == True and length == True:
        return True
    else:
        return False

def checkUsernameRequirenment(text):
    length = False

    if len(text) >6 and len(text) <25:
        length = True
    
    if length == True:
        return True
    else:
        return False
    





        
        