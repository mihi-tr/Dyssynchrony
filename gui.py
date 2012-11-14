from Tkinter import *
import angles
import tkFileDialog
import tkMessageBox

class Gui():
  def __init__(self,root):
    self.root=root
    lf=Frame(root)
    label=Label(lf,text="Strain Files")
    label.pack()
    self.lb=Listbox(lf,width=50,selectmode=MULTIPLE)
    self.lb.pack()
    self.bf=Frame(lf)
    self.ab=Button(self.bf,text="+",command=self.add_files,width=1)
    self.ab.grid(column=0,row=0)
    self.rb=Button(self.bf,text="-",command=self.remove_files,width=1)
    self.rb.grid(column=1,row=0)
    self.bf.pack(side=LEFT)
    lf.pack()
    saf=Frame(lf)
    self.outfile=StringVar()
    self.sab=Button(saf,text="Save as...",command=self.save_as)
    self.sab.grid(column=0,row=0)
    self.sal=Label(saf,textvariable=self.outfile,width=20)
    self.sal.grid(column=1,row=0)
    saf.pack(side=LEFT)
    self.gb=Button(lf,text="Go!",command=self.process)
    self.gb.pack()

    
  def add_files(self):
    """ Add files to the list """
    files=tkFileDialog.askopenfilenames(multiple=True)
    for f in files: 
      self.lb.insert(END,f)
      

  def remove_files(self):
    """ remove files from the list """
    while self.lb.curselection():
      self.lb.delete([i for i in self.lb.curselection()][0])

  def save_as(self):
    """ select the file for saving as """
    self.outfile.set(tkFileDialog.asksaveasfilename())

  def process(self):
    """ do the processing """
    angles.process(self.outfile.get(),self.lb.get(0,END))
    tkMessageBox.showinfo("Done","Finished Calculating Dyssynchrony")
    


if __name__=="__main__":
  root=Tk()
  gui=Gui(root)
  root.mainloop()
