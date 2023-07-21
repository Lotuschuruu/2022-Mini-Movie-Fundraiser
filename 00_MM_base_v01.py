import pandas
import random
from datetime import date

# functions go here


# shows instructions
def show_instructions():
    print('''\n
***** Instructions *****

For each ticket, enter ...
- The person's name (can't be blank)
- Age (between 12 and 120)
- Payment method (cash / credit)

When you have entered all the users, press 'xxx' to quit

The program will them display ticket details
including the cost of each ticket, the total cost 
and the total profit

This information will also be automatically written to 
a text file.

*************************''')


# checks that user response is not blank
def not_blank(question):

    while True:
        response = input(question)

        # if the response is blank, outputs error
        if response == "":
            print("Sorry this can't be blank. Please try again")
        else:
            return response


# checks users enter an integer to a given question
def num_check(question):

    while True:

        try:
            response = int(input(question))
            return response

        except ValueError:
            print("Put in an actual number, goof.")
# main routine starts here


# Calculate the ticket price based on the age
def calc_ticket_price(var_age):

    # ticket is $7.50 for users under 16
    if var_age < 16:
        price = 7.5
    # ticket is 10.50 for users between 16 and 64
    elif var_age < 65:
        price = 10.5
    # ticket price is $6.50 for seniors (65+)
    else:
        price = 6.5

    return price


# checks that users enter a valid response (eg:  yes / no
# cash / credit) based on a list of options
def string_checker(question, num_letters, valid_responses):

    error = "Please choose {} or {}".format(valid_responses[0],
                                            valid_responses[1])

    if num_letters == 1:
        short_version = 1
    else:
        short_version = 2

    while True:

        response = input(question).lower()

        for item in valid_responses:
            if response == item[:short_version] or response == item:
                return item

        print(error)


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# set maximum number of tickets below
MAX_TICKETS = 3
tickets_sold = 0

yes_no_list = ["yes", "no"]
payment_list = ["cash", "credit"]

# lists to hold ticket details
all_names = ["a", "b", "c", "d", "e"]
all_ticket_costs = [7.50, 7.50, 10.50, 10.50, 6.50]
all_surcharge = [0, 0, 0.53, 0.53, 0]

mini_movie_dict = {
    "Name": all_names,
    "Ticket Price": all_ticket_costs,
    "Surcharge": all_surcharge
}

# Ask user if they want to see the instructions
want_instructions = string_checker("Do you want to read the instructions? (y/n): ", 1, yes_no_list)

if want_instructions == "yes":
    show_instructions()

print()

# loop to sell tickets

while tickets_sold < MAX_TICKETS:
    name = not_blank("Enter your name (or 'xxx' to quit) ")

    if name == 'xxx' and len(all_names) > 0:
        break
    elif name == 'xxx':
        print("You must sell at least ONE ticket before quitting")
        continue

    age = num_check("Age: ")

    # check user is between 12 and 120 (inclusive)
    if 12 <= age <= 120:
        pass
    elif age < 12:
        print("Get out of here goof, grow up")
        continue

    else:
        print("That's gotta be a typo, redo it.")
        continue

    # calculate ticket cost
    ticket_cost = calc_ticket_price(age)

    # get payment method
    pay_method = string_checker("Choose a payment method (cash / "
                                "credit: ", 2, payment_list)

    if pay_method == "cash":
        surcharge = 0
    else:
        # calculate 5% surcharge if users are paying by credit card
        surcharge = ticket_cost * 0.05

    # add ticket name cost and surcharge to lists
    all_names.append(name)
    all_ticket_costs.append(ticket_cost)
    all_surcharge.append(surcharge)

    tickets_sold += 1

    mini_movie_dict = {
        "Name": all_names,
        "Ticket Price": all_ticket_costs,
        "Surcharge": surcharge
    }

    mini_movie_frame = pandas.DataFrame(mini_movie_dict)
    # mini_movie_frame = mini_movie_frame.set_index('Name')

    # Calculate the total ticket cot (ticket + surcharge)
    mini_movie_frame['Total'] = mini_movie_frame['Surcharge'] \
        + mini_movie_frame['Ticket Price']

    # calculate the profit for each ticket
    mini_movie_frame['Profit'] = mini_movie_frame['Ticket Price'] - 5

    # calculate ticket and profit totals
    total = mini_movie_frame['Total'].sum()
    profit = mini_movie_frame['Profit'].sum()

    # choose winner and look up total won
    winner_name = random.choice(all_names)
    win_index = all_names.index(winner_name)
    total_won = mini_movie_frame.at[win_index, 'Total']

    # choose a winner from our name list
    winner_name = random.choice(all_names)

    # get position of winner name in list
    win_index = all_names.index(winner_name)

# Currency formatting (uses currency function)
    add_dollars = ['Ticket Price', 'Surcharge', 'Total', 'Profit']
    for var_item in add_dollars:
        mini_movie_frame[var_item] = mini_movie_frame[var_item]

        # choose a winner from our name list
        winner_name = random.choice(all_names)

    # **** Get current date for heading filename ****
    # get today's date
    today = date.today()

    # Get day, month and year as individual strings
    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")

    heading = "---- Mini Movie Fundraiser Ticket Data ({}/{}/{}) ----\n".format(day, month, year)
    filename = "MMF_{}_{}_{}".format(year, month, day)

    # Change frame to a string so that we can export it to file
    mini_movie_string = pandas.DataFrame.to_string(mini_movie_frame)

    # create strings for printing....
    ticket_cost_heading = "\n----- Ticket Cost / Profit -----"
    total_ticket_sales = "Total Ticket Sales: ${:.2f}".format(total)
    total_profit = "Total Profit : ${:.2f}".format(profit)

    # show users ho many tickets have been sold & how much they won
    if tickets_sold == MAX_TICKETS:
        sales_status = "\n*** All the tickets have been sold ***"
    else:
        sales_status = "\n **** You have sold {} out of {} " \
                       " tickets ****".format(winner_name, total_won)

    winner_heading = "\n---- Raffle Winner ----"
    winner_text = "The winner of the raffle is {}.  " \
                  "They have won ${:.2f}.  ie: Their ticket is" \
                  "free!".format(winner_name, total_won)

    # list holding contact to print / write to file
    to_write = [heading, mini_movie_string, ticket_cost_heading,
                total_ticket_sales, total_profit, sales_status,
                winner_heading, winner_text]

    # print output
    for item in to_write:
        print(item)

    # write output to file
    # create file to hold data (add .txt extension)
    write_to = "{}.txt".format(filename)
    text_file = open(write_to, "w+")

    for item in to_write:
        text_file.write(item)
        text_file.write("\n")

    # close file
    text_file.close()

# Output number of tickets sold
if tickets_sold == MAX_TICKETS:
    print("Congratulations you have sold all the tickets")
else:
    print("You have sold {} ticket/s. There is {} ticket/s "
          "remaining".format(tickets_sold, MAX_TICKETS - tickets_sold))
