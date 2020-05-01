from tkinter import *

class apps:
      def __init__(self, roots):
           roots.title("小算盤")
           roots.geometry('450x450')

           self.var_str = StringVar()
           self.e = Entry(textvariable=self.var_str ,relief=SUNKEN, font=('Courier New', 24), width=28)
           self.e.pack(side=TOP, pady=10)

           self.frame = Frame(roots)
           self.frame.pack(side=TOP)
           self.frame_1 = Frame(roots)
           self.frame_1.pack(side=TOP)

           self.buttons()
     
      def buttons(self):
           self.names = ("0" , "1" , "2" , "3", "4" , "5" , "6" , "7" , "8" , "9", "+" , "-" , "*" , "/" , ".", "=", "c")
           for i in range(len(self.names)):
                if "c" != self.names[i]:
                     self.b = Button(self.frame, text=self.names[i], font=('Verdana', 20), width=8, height=3, command=lambda b_text=self.names[i], e_text=self.var_str: self.command(b_text, e_text))
                     self.b.grid(row=i // 4, column=i % 4)
                else:
                     self.b = Button(self.frame_1, text=self.names[i], font=('Verdana', 20), width=33, height=3, command=lambda b_text=self.names[i], e_text=self.var_str: self.command(b_text, e_text))
                     self.b.grid()
                        
      def command(self, b, e):
           if "=" != b:
                e.set(e.get() + b)
           if "c" == b:
                e.set("")
           if "=" == b:
                self.tot = self.var_str.get()
                e.set(eval(self.tot))
                 
root = Tk()
sinan = apps(root)
root.mainloop()