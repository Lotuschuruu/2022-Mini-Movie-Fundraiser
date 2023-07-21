# function goes here

# checks that user response is not blank
def not_blank(question):

    while True:
        response = input(question)

        # if the response is blank, outputs error
        if response == "":
            print("Sorry this can't be blank. Please try again")
        else:
            return response


# main routine goes here
while True:
    name = not_blank("Enter your name (or 'xxx' to quit) ")
    if name == "xxx":
        break

print("We are done")
