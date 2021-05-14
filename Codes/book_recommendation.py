from tkinter import *
import mysql.connector as msc
import pandas as pd
from tkinter import font as tkf
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
import base64
from io import BytesIO
import numpy as np
import cv2
import urllib



class Database_connection:

    def __init__(self):
        self.mydb = msc.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "book_recommendation_db"
        )

class Book_recommendation(Database_connection):
    def __init__(self):
        super(Book_recommendation,self).__init__()

        self.df_books = pd.read_sql("Select * from books",con =self.mydb)

        root = Tk()
        root.title('Book Recommendation System')
        #root.geometry("500x300")
        img = ImageTk.PhotoImage(Image.open("book_background.jpg"))
         
        background_label = Label(root, image=img)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)


        self.new_frame = Frame(root)
        self.new_frame.grid(row = 0, column = 1,padx = 100, pady = 100)

        self.recommendationFrame = Frame(root)
        
        # Created a Label Title
        self.myLabel = Label(self.new_frame,text="BOOK RECOMMENDATION SYSTEM", font=("Helvitica", 14), fg="black")
        self.myLabel.pack(pady=20)

        #Create Entry Box 
        self.my_entry = Entry(self.new_frame, width = 70,font=("Helvitica", 12))
        self.my_entry.pack()


        self.button = Button(self.new_frame,text="Show Recommendations", command = lambda:self.showRecommendations(self.my_entry.get()))
        self.button.pack()
        #Create List box
        self.my_list = Listbox(self.new_frame,width=70, font= tkf.Font(size = 12))

        


        self.update_dataFrame(self.df_books)

        #create a binding on the listbox onclick
        self.my_list.bind("<<ListboxSelect>>", self.fillout)


        #Create a binding on the entry box
        self.my_entry.bind("<KeyRelease>", self.check)

        # self.self.recommended_list_box = ttk.Treeview(self.recommendationFrame, height=7)
        self.recommended_list_box = Listbox(self.recommendationFrame,width=70, height = 20, font= tkf.Font(size = 12))

        #creating a label and title
        self.recommended_books_lbl = Label(self.recommendationFrame, text = "Recommended Books", font=("Helvitica", 20, UNDERLINE), fg="grey")


        self.title_lbl =  Label(self.recommendationFrame, text = "Book Title", font=("Helvitica", 15), fg="black")
        
        root.mainloop()
    
    #Accepts Dataframe as Parameter to populate the listbox
    def update_dataFrame(self,data):
        
        #Clear Listbox
        self.my_list.delete(0,END)

        #Add the data to list
        for item in data['choices']:
            self.my_list.insert(END,item)

    def populate_recommedation(self,data):
                
        #Clear Listbox
        self.recommended_list_box.delete(0,END)

        #Add the data to list
        for item in data['title']:
            self.recommended_list_box.insert(END,item)


    #Accepts Dataframe as Parameter to populate the listbox
    def update_list(self,data):
        
        #Clear Listbox
        self.my_list.delete(0,END)

        #Add the data to list
        for item in data:
           self.my_list.insert(END,item)


    #Update entry box with listbox with listbox clicked

    def fillout(self,e):
        
        #Delete whatever is in entry box
        self. my_entry.delete(0,END)

        #Add clicked list item to entry box
        self.my_entry.insert(0,self.my_list.get(ANCHOR))


    #Create func to check entry vs Listbox

    def check(self,e):

        #grab what was typed
        typed = self.my_entry.get()

        if typed == '':
            self.my_list.pack_forget()
            data = self.df_books
        else:
            self.my_list.pack()
            books_found = []
            for book in self.df_books['choices']:
                if typed.lower() in book.lower():
                    books_found.append(book)

            self.update_list(books_found)

    def showRecommendations(self,bookName_input):
        
        
        # self.clear_tree()
        # self.df_result = pd.read_sql("SELECT title, MATCH(bagowords) AGAINST ((SELECT bagowords FROM books WHERE choices = '{}') IN NATURAL LANGUAGE MODE) AS `Score` FROM books Where author <> (SELECT author FROM books WHERE choices = '{}') AND choices <> '{}' ORDER BY `Score` DESC;".format(bookName_input,bookName_input,bookName_input), con = self.mydb)
        # self.top_recommendation = self.df_result.head(20)
        # #Set up new tree View
        # self.recommended_list_box["column"] = list(self.top_recommendation.columns[0:1])
        # self.recommended_list_box["show"] = "headings"

        # #loop through column list
        # for column in self.recommended_list_box["column"]:
        #    self.recommended_list_box.heading(column,text = column)
        
        # #Put data 

        # df_rows = self.top_recommendation.to_numpy().tolist()
        # for rows in df_rows:
        #     if(rows[0] == "NA"):
        #         continue
            
        #     #URL = str(rows[0])
        #     #u = urlopen(URL)
        #     #raw_data = u.read()
        #     #u.close()

        #     #im = Image.open(BytesIO(raw_data))
        #     #photo = ImageTk.PhotoImage(im)
        #     self.recommended_list_box.insert("", "end",values=rows[0])


        self.recommended_books_lbl.place(x = 190,y=10)
        self.title_lbl.place(x = 0,y=50)


        self.df_result = pd.read_sql("SELECT title, MATCH(bagowords) AGAINST ((SELECT bagowords FROM books WHERE choices = '{}') IN NATURAL LANGUAGE MODE) AS `Score` FROM books Where author <> (SELECT author FROM books WHERE choices = '{}') AND choices <> '{}' ORDER BY `Score` DESC;".format(bookName_input,bookName_input,bookName_input), con = self.mydb)
        self.top_recommendation = self.df_result.head(20)
        
        self.populate_recommedation(self.top_recommendation)
        self.recommended_list_box.pack(pady=80)
        self.recommendationFrame.place(x=830, y=100)

        self.recommended_list_box.bind("<Double-1>",self.bookDeatils)


    def bookDeatils(self,e):
        bookName = self.recommended_list_box.get(ANCHOR)
        self.new_win = Toplevel()
        self.new_win.geometry('500x500+500+100')

        self.selectedBookDetails = pd.read_sql("SELECT title, author, description,avg_rating,gd_cover FROM books WHERE title = '{}'".format(bookName),con = self.mydb)

        lbl_Title = Label(self.new_win, text=("Title: " + self.selectedBookDetails['title'][0]), font=("Helvitica", 18, UNDERLINE), fg="black" )
        lbl_Title.place(x=20,y=20)

        lbl_author = Label(self.new_win, text=("Author: " + self.selectedBookDetails['author'][0]), font=("Helvitica", 12), fg="grey" )
        lbl_author.place(x=20,y=80)
        

        frame_description = Frame(self.new_win)
        frame_description.place(x=20,y=120)

        description = self.selectedBookDetails['description'][0]

        lbl_description = Label(frame_description, text=("Description: " + description), font=("Helvitica", 12), fg="grey", wraplength = 1000, justify = LEFT )
        lbl_description.grid(row=0, column=0)
        

        rating = float(self.selectedBookDetails['avg_rating'][0])

        lbl_rating = Label(self.new_win, text=("Rating: " + str(rating)), font=("Helvitica", 12), fg="grey" )
        lbl_rating.place(x=20,y=300)



        # self.image_frame = Frame(self.new_win)
        # self.image_frame.pack()

        # lblImage = Label()
        # url_response = urllib.request.urlopen(URL)
        # img_array =  np.array(bytearray(url_response.read()),dtype = np.uint8)
        # img = cv2.imdecode(img_array,1)
        
        # URL = "https://drive.google.com/thumbnail?id=13hcWfe6FaJrJ3eFC6GCM_Fo_fLtakKor"
        # u = urlopen(URL)
        # raw_data = u.read()
        # u.close()

        # im = Image.open(BytesIO(raw_data))
        # photo = ImageTk.PhotoImage(im)

        # lblImage = Label(self.image_frame,image = photo)
        # lblImage.grid(row=0,column=0)
        
book = Book_recommendation()
