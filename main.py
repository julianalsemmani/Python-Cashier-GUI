from tkinter import *
import tkinter.font as tkfont
from tkinter import messagebox
import json
import random

# Opens the data.json file, to read seller information for login.
with open("data.json", "r") as file:
    data = json.load(file)


totalAmount = 0
backgroundColor = "#C3C3C3"


# TODO: Design the cashier GUI
# TODO: Create functionality to each element.


def cashierWindow(firstname, lastname, username):
    """
    Opens a new tkinter window. It will open the cashier system when the login is success.
    :param firstname: String parameter
    :param lastname: String parameter
    :param username: String parameter
    :return: Will show the firstname, lastname and username as title and on the Cashier Window Screen
    """
    # Sets Tk() as cahsier
    cashier = Tk()

    # Empty List to add the products to
    productList = []

    # A text variable to display the current amount
    amount = StringVar()
    # Setting default text for the string var
    amount.set("Total amount: $0.00")

    # Sets the size of the window to width = 1250px and height = 750px
    cashier.geometry("900x600")
    # Removes the resizeable feature, so user can not resize the window.
    cashier.resizable(0, 0)
    # Adds a Icon to the software topbar.
    cashier.iconbitmap("image/favicon.ico")

    # Sets background color of the GUI
    cashier.configure(bg=backgroundColor)

    # Sets a font called userInformation to have fontfamily Arial and size 18px
    userInformation = tkfont.Font(family="Arial", size=18)

    # Sets a font called userInformation2 to have fontfamily Arial and size 14px
    userInformation2 = tkfont.Font(family="Arial", size=14)

    # Sets the title to "Welcome, firstname lastname. You're logged in as username
    # Example: Welcome, Julian Alsemmani. You're logged in as juliania
    cashier.title(
        f"Welcome, {firstname} {lastname}. You're logged in as {username}")

    # Same as cashier.title. Shows a "Message" on the GUI, same text as cashier.title
    Label(
        cashier, text=f"Welcome, {firstname} {lastname}. You're logged in as {username}", font=userInformation, bg=backgroundColor).pack()

    listbox = Listbox(cashier, height=18, width=30,
                      bg="white", activestyle="dotbox", font=("Arial", 16))
    listbox.place(x=510, y=40)

    # Scrollbar code from https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
    scrollbar = Scrollbar(cashier)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    def addReceipt():
        """Loads json file, then writes receipt to the json file.
        """
        # Empty list to add the products to it.
        receiptProductList = []

        # Looping through the productList list
        for length in range(len(productList)):
            # Appends product name to receiptProductList list.
            receiptProductList.append(productList[length][0])

        # Opens data.json and reads from it
        with open("data.json", "r") as file:
            # Saves the data inside the json file into old_data variable
            file_data = json.load(file)

        # Appends data to file_data["receipt"]
        file_data["receipt"].append({
            # Setting order number to be length of "receipt" + 1
            "ordernumber": (len(file_data["receipt"]) + 1),
            # Setting the productList to be receiptProductList
            "products": receiptProductList,
            # Setting the totalAmount to be the amount of the variable totalAmount
            "totalamount": totalAmount
        })

        # Opens data.json and writes data to it
        with open("data.json", "w") as file:
            # Dumps filedata to file, and indents it with 4.
            json.dump(file_data, file, indent=4)

    # Function for the Credit/Debit Checkout
    def cardCheckout(amount):
        """Function to compelete the order for Credit/Debit Checkout.

        Args:
            amount ([float]): Takes in a amount as a float.
        """

        # Variable Scope. Needs to get the totalAmount to access it, use it and reassign it.
        global totalAmount
        # Checks if the Total amount variable is less or equal to 0.
        if totalAmount <= 0:
            # Displays a warning message that the amount has to be greater than $0.
            messagebox.showwarning(
                message=f"Your total amount has to be greater than $0.")
        # If the total amount is greater than 0 it will run this code.
        else:
            addReceipt()
            # It will show a messagebox, with a payment successful, and display the amount that has been paid.
            messagebox.showinfo(
                message=f"Payment successful. ${totalAmount} paid.")
            # Clearing out the productList list.
            productList.clear()
            # Clearing out the listbox, from index 0 to 'end'. It will clear the whole listbox
            listbox.delete(0, 'end')
            # Sets the totalAmount to equal 0, so you can continue with the next customer.
            totalAmount = 0
            # Sets the Total Amount text to "Return amount: $0.00"
            # Since you're paying with card, you'll not return any money.
            amount.set("Return amount: $0.00")

    def cashCheckout(amount):
        # Variable Scope. Needs to get the totalAmount to access it, use it and reassign it.
        global totalAmount

        # Checks if the totalamount is less or equal to 0
        if totalAmount <= 0:
            # It will show an error message, that the cart has to be greater than $0.
            messagebox.showwarning(
                message=f"Your total amount has to be greater than $0.")
        # If the totalamount is higher than 0 it will run this code.
        else:
            # Creates a new Tkinter window.
            cash = Toplevel()
            # Sets the size of the window to 200x300
            cash.geometry("300x120")
            # Sets the title of the window
            cash.title("Cash")
            # Changes the favicon of the window
            cash.iconbitmap("image/favicon.ico")
            # Turns of the Resize feature. Users can not resize the window.
            cash.resizable(0, 0)

            # Adds a label to the screen
            Label(cash, text="Enter Given Cash Amount: ").pack()

            # Adds a label to the screen
            Label(cash, text="Amount: ").pack()
            # Adds a Entry Input saved in the variable givenAmount
            givenAmount = Entry(cash)
            # Adds the Entry to the screen
            givenAmount.pack()

            # Variable text
            errorText = StringVar()
            # Displays Label with variable text
            Label(cash, textvariable=errorText).pack()

            # Function to get the value of a entry box.

            def completeCheckout(variable):
                """Completes checkout for cash payment.

                Args:
                    variable (Takes in button as parameter): This is to retrieve the information from the Entry

                Returns:
                    : Returns messages If it's successful or not. 
                """
                # Variable scope to access the variable totalAmount to make changes.
                global totalAmount

                # Try/except, just to be sure that the input is a number value and not a string.
                try:
                    # Converts moneyGiven to a float, and gets the input value from the Entry
                    moneyGiven = float(variable.get())

                    # Checks if moneyGiven is less than the Totalamount
                    if moneyGiven < totalAmount:
                        # Shows a error message that displays, that the money given is not enough.
                        errorText.set(
                            f"Not Enough money. You need ${round((totalAmount - moneyGiven), 2)} more.")

                    # If moneyGiven is more or equal to the total amount else code will run.
                    else:
                        # Makes a receipt out of the order.
                        addReceipt()
                        # Sets amount to display a text of how much to return.
                        amount.set(
                            f"Return amount: ${round((moneyGiven - totalAmount), 2)}")
                        # A messagebox will pop up with payment succcess and the return amount.
                        messagebox.showinfo(
                            message=f"Payment Successful! Return amount: ${round((moneyGiven - totalAmount), 2)}")
                        # Closes the window called "cash"
                        cash.destroy()
                        # Clears out the listbox from index 0 to end of list.
                        listbox.delete(0, 'end')
                        # Clearing out the productList List
                        productList.clear()
                        # Setting the value of totalAmount to be 0, so you can start a new order.
                        totalAmount = 0
                # If the given input in something else than a number:
                except:
                    # Shows an error that the input has to be a number value.
                    errorText.set(
                        f"Given money has to be a number value.")

            # Adds a button to the screen with function getAmount()
            Button(cash, text="Checkout",
                   command=lambda: completeCheckout(givenAmount)).pack()
            cash.mainloop()

    # Function to get the selected item from the listbox
    def getSelectedItem(evt):
        """Gets the seelected item from the listbox and deletes it from the list.

        Args:
            evt : Event to do the code on. In this case it will work on listboxes.
        """
        # Variable Scope. Needs to get the totalAmount to access it, use it and reassign it.
        global totalAmount
        # Code from https://stackoverflow.com/questions/15672552/tkinter-listbox-getactive-method
        # doing evt to a widget
        widget = evt.widget
        # Getting the cursor selection from the widget
        try:
            selection = widget.curselection()
        # Picked will be equal to the pressed item in the listbox
            picked = widget.get(selection[0])
        # Printing out picked variable.
            print(picked)

        # Checks the length of the productList List
            for productlength in range(len(productList)):
            # Checks if the word placed at Index 0 in the List is in the string "picked"
                if productList[productlength][0] in picked:
                # If this is correct, it will remove from the totalAmount
                    totalAmount -= productList[productlength][1]
                # Delete the product from the list
                    del productList[productlength]
                # Delete the product from the listbox
                    listbox.delete(selection)

                # Checks if totalAmount goes below 0.
                    if totalAmount < 0:
                    # If totalamount is less than 0, we will set totalAmount to be equal to 0
                        totalAmount = 0

                # Display the new total amount
                    amount.set(f"Total amount: ${round(totalAmount, 2)}")

                # It will break out of the for loop, because we've successfully found our product and deleted it.
                    break
        except:
            print("Not a valid selection!")

    # Function to cancel the current order.
    def cancelOrder():
        """Removes everything from a cart if they want to cancel the order.
        """

        # Variable Scope. Needs to get the totalAmount to access it, use it and reassign it.
        global totalAmount

        # Checks if the productList has items in it or not. If It's empty the bool will return False.
        if bool(productList) == False:
            # Shows a error message box with a message If the cart is empty.
            messagebox.showerror(
                message="You can't cancel a order with an empty cart. Please add items to the cart to continue.")
        # If the bool of the productList is equal to True this will run
        else:
            # It will clear the List, so it will be empty.
            productList.clear()
            # It will delete items from the listbox. From Index 0 to end of the list.
            listbox.delete(0, 'end')
            # It will set the new Total Amount label to be "Total amount: $0.00"
            amount.set("Total amount: $0.00")
            # Sets totalAmount to equal 0
            totalAmount = 0

    # Binding function to a Listbox Select. It will do something when an item in the listbox is selected.
    listbox.bind('<<ListboxSelect>>', getSelectedItem)

    # Displays text "Payment Options:"
    Label(cashier, text="Payment Options:",
          bg=backgroundColor).place(x=510, y=500)

    # Displays text "Total Amount: ", with the total amount to be paid
    Label(cashier, textvariable=amount, bg=backgroundColor).place(x=720, y=500)

    # Using lambda to be able to throw a value with the function call.
    Button(cashier, text="Cash", command=lambda: cashCheckout(
        amount), width=12, height=2).place(x=510, y=535)

    Button(cashier, text="Debit/Credit", command=lambda: cardCheckout(amount),
           width=12, height=2).place(x=645, y=535)

    Button(cashier, text="Cancel Order", command=cancelOrder,
           width=12, height=2).place(x=780, y=535)

    # Adds product to listbox

    def addProduct(productnames, productprice):
        """Adds product to Listbox, and list.

        Args:
            productnames ([string]): Takes in productname as string
            productprice ([float]): Takes in productprice as float

        Inserts productname and productprice to listbox and productList list.
        """
        # Variable scope. This is to access the variable and being able to change it.
        global totalAmount

        # Appends product into productlist list
        productList.append([productnames, productprice])

        # Increments totalamount with productprice
        totalAmount += productprice

        # Show's the total amount to be paid, rounded down to 2 digits after ".".
        amount.set(f"Total amount: $ {round(totalAmount, 2)}")

        # Adds product into index of length of productlist, with name of product
        listbox.insert(len(productList),
                       f"Product: {productnames} | Price: ${productprice}")
        print(f"Added {productnames} to index {len(productList)}")

    # Using Lambda on the command to be able to give the parameter an value.
    # Buttons for Row 1
    Button(cashier, text="Bag", command=lambda: addProduct(
        "Bag", 1.00), width=12, height=3).place(x=25, y=40)

    Button(cashier, text="Bread", command=lambda: addProduct(
        "Bread", 2.99), width=12, height=3).place(x=25, y=120)

    Button(cashier, text="Egg", command=lambda: addProduct(
        "Egg", 3.99), width=12, height=3).place(x=25, y=200)

    Button(cashier, text="Oil", command=lambda: addProduct(
        "Oil", 5.25), width=12, height=3).place(x=25, y=280)

    # Buttons for Row 2
    Button(cashier, text="Milk", command=lambda: addProduct(
        "Milk", 1.85), width=12, height=3).place(x=150, y=40)

    Button(cashier, text="Rice", command=lambda: addProduct(
        "Rice", 10.99), width=12, height=3).place(x=150, y=120)

    Button(cashier, text="Butter", command=lambda: addProduct(
        "Butter", 2.25), width=12, height=3).place(x=150, y=200)

    Button(cashier, text="Cereal", command=lambda: addProduct(
        "Cereal", 4.50), width=12, height=3).place(x=150, y=280)

    # Buttons for Row 3
    Button(cashier, text="Cheese",
           command=lambda: addProduct("Cheese", 6.76), width=12, height=3).place(x=275, y=40)

    Button(cashier, text="Garlic",
           command=lambda: addProduct("Garlic", 3.99), width=12, height=3).place(x=275, y=120)

    Button(cashier, text="Apple",
           command=lambda: addProduct("Apple", 0.99), width=12, height=3).place(x=275, y=200)

    Button(cashier, text="Banana",
           command=lambda: addProduct("Banana", 1.29), width=12, height=3).place(x=275, y=280)

    # Buttons for Row 4
    Button(cashier, text="Salt",
           command=lambda: addProduct("Salt", 2.29), width=12, height=3).place(x=400, y=40)

    Button(cashier, text="Pepper",
           command=lambda: addProduct("Pepper", 2.29), width=12, height=3).place(x=400, y=120)

    Button(cashier, text="Beef",
           command=lambda: addProduct("Beef", 49.99), width=12, height=3).place(x=400, y=200)

    Button(cashier, text="Chicken",
           command=lambda: addProduct("Chicken", 35.79), width=12, height=3).place(x=400, y=280)

    # Custom Product to Add
    def customProductValues():
        """Gets entry from Entry boxes, and adds it to the cart. Possibility to add custom products with custom price.
        """
        # Gets Custom Product Value from Entry
        customproduct = customProductEntry.get()
        # Gets Custom Price Value from Entry
        customprice = customPriceEntry.get()

        # Checks if length is less or equal to 0
        if len(customproduct) <= 0 and len(customprice) <= 0:
            # Displays an error that the cart can't be empty.
            messagebox.showerror(
                message="Product name and/or price can not be empty.")
        # Checks if one is more than 0 and the other is less or equal to 0
        elif len(customproduct) > 0 and len(customprice) <= 0:
            # Displays an error to the user.
            messagebox.showerror(
                message="Price can not be empty.")
        # Checks if one is less or equal to 0 and the other is more than 0
        elif len(customproduct) <= 0 and len(customprice) > 0:
            # Displays an error to the user.
            messagebox.showerror(
                message="Product Name can not be empty.")
        # If both values values is > 0, this will run.
        else:
            # Tries to change the data type of the Entry's
            try:
                customproduct = str(customproduct)
                customprice = float(customprice)

                # Calls the addProduct Function with the product and price
                addProduct(customproduct, customprice)
                # Clears both of Entrys from 0 to end.
                customPriceEntry.delete(0, 'end')
                customProductEntry.delete(0, 'end')
            # If it isn't able to change the data types, it will display an error message.
            except:
                messagebox.showerror(message="Price has to be a number.")

    # Label for Product Name
    Label(cashier, text="Product Name:", bg=backgroundColor).place(x=22, y=350)
    # Entry for Product Name
    customProductEntry = Entry(cashier, width=30)
    # Displays it on the GUI
    customProductEntry.place(x=110, y=350)

    # Label for Price
    Label(cashier, text="Price: ", bg=backgroundColor).place(x=22, y=380)
    # Entry for Price
    customPriceEntry = Entry(cashier, width=30)
    # Displays it on the GUI
    customPriceEntry.place(x=110, y=380)

    # Button for adding the custom product.
    Button(cashier, text="Add Product",
           command=lambda: customProductValues(), width=12, height=3).place(x=400, y=350)

    # Admin Functions
    def newSeller():
        """Creates a new window for adding a seller. Asks for different inputs and compares username
        to usernames that exists in the json. If it exist it will give an error, and if it doesn't exist
        it will create the user.
        """

        # Variable for the error text.
        createText = StringVar()

        def addNewSeller():
            """Gets the userinputs from Entry's then, checks the data.json for usernames, 
            and if they exists. If they exist it will return an error. 
            If it doesn't exist it will create the user.
            """
            # Gets Entry information, and changes things to title and lowering username.
            seller_firstname = newFirstName.get().title()
            seller_lastname = newLastName.get().title()
            seller_username = newUsername.get().lower()
            seller_pin = newPin.get()

            # Opens data.json and reads from it
            with open("data.json", "r") as file:
                # Saves the data inside the json file into old_data variable
                file_data = json.load(file)

            # Checks length of file_data["seller"]
            for user in range(len(file_data["seller"])):
                # Gets the username from "seller"[index] and checks if it's equal to seller_username
                if file_data["seller"][user].get("username") == seller_username:
                    print(
                        "Username already exists in the system. Please use another username to continue.")
                    # Displays text that the username already exists
                    createText.set("Username already exists.")
                    # Breaks out of the loop.
                    break
                # Checks if length of user is the same as the length of file_data["seller"] to get last element
                elif user == len(file_data["seller"]) - 1:
                    # Appends data to file_data["receipt"]
                    file_data["seller"].append({
                        # Setting order number to be length of "receipt" + 1
                        "firstname": seller_firstname,
                        # Setting the productList to be receiptProductList
                        "lastname": seller_lastname,
                        # Setting the totalAmount to be the amount of the variable totalAmount
                        "username": seller_username,
                        "pin": seller_pin
                    })

                    # Opens data.json and writes data to it
                    with open("data.json", "w") as file:
                        # Dumps filedata to file, and indents it with 4.
                        json.dump(file_data, file, indent=4)

                    # Shows a message that the user has successfully been created.
                    messagebox.showinfo(
                        message=f"New user was successfully registered. Username: {seller_username}, PIN: {seller_pin}")
                    # Closes the current window.
                    newUser.destroy()
                    # Breaks out of the loop to stop it from creating more users.
                    break

        # Makes a new Window
        newUser = Toplevel()

        # Displays Title on the Window
        newUser.title("Add New Seller")
        # Displays a width and height on the window
        newUser.geometry("300x330")

        # Disables resize feature on window. It's not possible to resize it anymore.
        newUser.resizable(0, 0)
        # Adds a Icon to the software topbar.
        newUser.iconbitmap("image/favicon.ico")

        # Title "Add New Seller", with a font configuration
        Label(newUser, text="Add New Seller", font=userInformation2).pack()

        # Label for first name
        Label(newUser, text="First Name:").pack()
        # Entry for first name
        newFirstName = Entry(newUser, width=30)
        # Making the Entry visible
        newFirstName.pack(pady=5, padx=10)

        # Label for last name
        Label(newUser, text="Last Name:").pack()
        # Entry for last name
        newLastName = Entry(newUser, width=30)
        # Making the Entry visible
        newLastName.pack(pady=5, padx=10)

        # Label for username
        Label(newUser, text="Username:").pack()
        # Entry for username
        newUsername = Entry(newUser, width=30)
        # Making the Entry visible
        newUsername.pack(pady=5, padx=10)

        # Label for PIN
        Label(newUser, text="PIN:").pack()
        # Entry for PIN, all input to this Entry will be shown with stars
        newPin = Entry(newUser, width=30, show="*")
        # Making the Entry visible
        newPin.pack(pady=10, padx=10)

        Button(newUser, text="Add Seller", command=addNewSeller, height=2,
               width=20).pack(pady=5, padx=20)

        Label(newUser, textvariable=createText).pack()

    # Gets the last sale receipt
    def getLastReceipt():
        """Gets the last element from "receipt" from data.json, and shows it to a window
        """
        # Reads data.json
        with open("data.json", "r") as file:
            # Saves the json as file_data
            file_data = json.load(file)

        if bool(file_data["receipt"]) == False:
            messagebox.showerror(
                message="There is no receipts saved in the system.")
        else:
            # Getting length of receipt list.
            length = len(file_data["receipt"])
            # Getting the last element in the "receipt"
            receipt_info = file_data["receipt"][length - 1]

            # Assigning variables with the values from the data.json "receipt"
            lastReceiptOrderNumber = receipt_info.get("ordernumber")
            lastReceiptProducts = receipt_info.get("products")
            lastReceiptTotalAmount = receipt_info.get("totalamount")

            print(lastReceiptOrderNumber,
                  lastReceiptProducts, lastReceiptTotalAmount)

        # Creates a new window
            receiptWindow = Toplevel()
        # Sets the height and width of the window
            receiptWindow.geometry("250x400")
        # Displays a new text for the window
            receiptInformation = tkfont.Font(family="Arial", size=12)
        # Changes the title of the window with "Order: Number"
            receiptWindow.title(f"Order: {lastReceiptOrderNumber}")

        # Label with Order Number
            Label(receiptWindow,
                  text=f"Receipt | Order: {lastReceiptOrderNumber}", font=receiptInformation).pack()

        # List box with the products in the list
            receiptList = Listbox(receiptWindow, width=25,
                                  height=15, font=receiptInformation)
        # Displaying it to the screen
            receiptList.pack()

        # Looping through the list, and adding it to the listbox.
            for item in range(len(lastReceiptProducts)):
                receiptList.insert(END, lastReceiptProducts[item])

        # Displaying the total amount that was paid.
            Label(receiptWindow,
                  text=f"Total Amount: ${lastReceiptTotalAmount}", font=receiptInformation).pack(pady=30)

    def userLogout():
        """Logging out the current user from the system. This by destroying the window and displaying
        the login screen again.
        """
        # Shows Messagebox with information that we're logging out of the user.
        messagebox.showinfo(message=f"Logging out of user: {username}")
        # Destroys current window
        cashier.destroy()
        # Calling the loginWindow function that will open a new window.
        loginWindow()

    # Labels for Admin Functions
    Label(cashier, text="Admin Functions",
          bg=backgroundColor, font=userInformation2).place(x=25, y=450)
    # Buttons for "Admin" functions
    Button(cashier, text="Add New Seller", command=newSeller,
           width=12, height=3).place(x=25, y=500)

    Button(cashier, text="Last Receipt", command=getLastReceipt,
           width=12, height=3).place(x=150, y=500)

    Button(cashier, text="Log out", command=userLogout,
           width=12, height=3).place(x=275, y=500)

    # Makes the window a loop, so It will show the window.
    cashier.mainloop()


def loginWindow():
    # Opens the data.json file, to read seller information for login.
    with open("data.json", "r") as file:
        # Loads ada from json file
        data = json.load(file)

    # Setting Tk() as window.
    window = Tk()

    # Sets the size of the window to width = 300px and height = 250px
    window.geometry("300x250")
    # Removes the resizeable feature, so user can not resize the window.
    window.resizable(0, 0)
    # Sets the title window to "POS - Login"
    window.title("Point Of Sale - Login")
    # Adds a Icon to the software topbar.
    window.iconbitmap("image/favicon.ico")

    # Makes a fontHeader, that has the font type Arial, and size 23px.
    fontHeader = tkfont.Font(family="Arial", size=23)

    # Title header with the fontHeader used. padding x dir 5, and padding y dir 5
    Label(window, text="Point Of Sale", font=fontHeader).pack(padx=5, pady=5)

    # Label for username
    Label(window, text="Username:").pack()
    # Username Entry with width of 40px
    username = Entry(window, width=40)
    # Packs the username into the window.
    username.pack()

    # Label for PIN
    Label(window, text="PIN:").pack()
    # PIN Entry with width of 40px
    pin = Entry(window, show="*", width=40)
    # Packs the PIN into the window.
    pin.pack()

    def get_user_input():
        """
        Gets the username and pin entry values. Then checks if the entry boxes is empty or has content.
        If It has content, it will check if the values equals the values inside the data json.
        If the value is the same as the data json, it will login and show a new window.

        :return: Does not return any value.
        """
        # Gets the Username entry and saves it into usern variable, also makes the entry lowercase.
        usern = username.get().lower()
        # Gets the PIN entry and saves it into usern variable
        pincode = pin.get()

        if usern == "" and pincode == "":
            messagebox.showinfo(
                message="Username and PIN Entry can not be empty.")
        elif usern == "" and pincode != "":
            messagebox.showinfo(message="Username Entry can not be empty.")
        elif pincode == "" and usern != "":
            messagebox.showinfo(message="PIN Entry can not be empty.")
        else:
            # Login Logic with JSON
            # Checks the length of the array data["seller"]
            for user in range(len(data["seller"])):
                # If username entry is the same as the username from the dictionary inside the array, it will succeed.
                if usern == data["seller"][user].get("username"):
                    # Printing out Correct username to the console.
                    print(
                        f"Correct Username. Welcome {data['seller'][user].get('username')}")
                    # If pin entry is the same as the pin from the dictionary inside the array, it will succeed.
                    if pincode == data["seller"][user].get("pin"):
                        # Defines 3 variables that stores, firstname, lastname and username from the succeed login.
                        firstname_show = data['seller'][user].get('firstname')
                        lastname_show = data['seller'][user].get('lastname')
                        username_show = data['seller'][user].get('username')

                        # Prints out "Correct PIN" to the console, and the PIN.
                        print(
                            f"Correct PIN. Your PIN is {data['seller'][user].get('pin')}")
                        # Messagebox with Info pops up, with "Logging in. Wait a bit."
                        messagebox.showinfo(message=f"Logging in. Wait a bit.")
                        # Closes the login window.
                        window.destroy()
                        # Calls the cashierWindow function with 3 parameters. firstname, lastname and username
                        cashierWindow(firstname_show,
                                      lastname_show, username_show)
                        # Breaks out of the loop, because we've successfully logged into the user we want.
                        break
                    # If the pincode is wrong, it will go to else
                    else:
                        # Prints out to the console "Wrong PIN"
                        print(f"{user}. Try: Wrong PIN.")
                # If the username is wrong, it will print out "Wrong Username" to the console
                else:
                    print(f"{user}. Try: Wrong username")
            # If the information is wrong, the loop will go to the else, and show a error message box.
            else:
                # Message box with error pops up, and prints out "Wrong username and/or password."
                messagebox.showerror(message="Wrong username and/or password.")

    # Button, uses the get_user_input as command. So It will call the function get_user_input() when the button is
    # clicked.
    Button(window, text="Login", command=get_user_input,
           height=2, width=30).pack(pady=20, padx=10)

    # Label for the "Made by Julian Alsemmani" below the button.
    Label(window, text="Made by Julian Alsemmani").pack()

    # Makes the window a loop, so It will show the window.
    window.mainloop()


# To run the login window when the script is started.
loginWindow()
