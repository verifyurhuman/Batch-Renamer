from webbrowser import open_new
from time import sleep
from re import sub,I
from os import rename,path,getcwd,chdir,listdir
from tkinter import Tk,Toplevel,Menu,Listbox,PhotoImage,IntVar,StringVar
from tkinter.ttk import Style,Entry,Label,Labelframe,Scrollbar
from tkinter.ttk import Button,Radiobutton,Checkbutton,Spinbox
from tkinter.filedialog import askopenfilenames,askdirectory
from tkinter.messagebox import askokcancel,showinfo,showerror



def Renamer():


    ####父窗口内部逻辑####


    #初始化程序
    def init(self):
        self.attributes('-alpha',0.0)
        win.attributes('-disabled',1)
        self.config(bg=['SystemButtonFace','#F0F0F0','#202020'][theme.get()])
        self.protocol('WM_DELETE_WINDOW',lambda:shut(self))
        self.bind('<Escape>',lambda e:shut(self))
        self.resizable(0,0)
        self.transient(win)
        self.focus_set()
    #计算屏幕宽高，居中显示窗口
    def center(self):
        self.update()
        width=self.winfo_width()
        height=self.winfo_height()
        border_width=self.winfo_rootx()-self.winfo_x()
        title_height=self.winfo_rooty()-self.winfo_y()
        winfo_width=width+border_width*2
        winfo_height=height+title_height+border_width
        x=self.winfo_screenwidth()//2-winfo_width//2
        y=self.winfo_screenheight()//2-winfo_height//2
        self.geometry(f'+{x}+{y}')
        self.attributes('-alpha',1.0)
        self.update()
    #关闭各子窗口
    def shut(self):
        win.attributes('-disabled',0)
        self.destroy()
    #设置滚动条关联
    def scroll(*arg):
        line.yview(*arg)
        lbox.yview(*arg)
        rbox.yview(*arg)
    #左侧列表框焦点时同步滚动右侧
    def lscroll(*arg):
        line.yview_moveto(arg[0])
        rbox.yview_moveto(arg[0])
        scrollbar.set(*arg)
    #右侧列表框焦点时同步滚动左侧
    def rscroll(*arg):
        line.yview_moveto(arg[0])
        lbox.yview_moveto(arg[0])
        scrollbar.set(*arg)
    #滚动条同步滚动事件
    def dscroll(*arg):
        lbox.yview_moveto(arg[0])
        rbox.yview_moveto(arg[0])
        scrollbar.set(*arg)
    #左侧列表选择时同步到右侧选择
    def lselect():
        rbox.select_clear(0,'end')
        for i in lbox.curselection():
            rbox.select_set(i)
        if rbox.size():
            ondelete()
    #右侧列表选择时同步到左侧选择
    def rselect():
        lbox.select_clear(0,'end')
        for i in rbox.curselection():
            lbox.select_set(i)
        if lbox.size():
            ondelete()
    #全选
    def selectall():
        lbox.select_set(0,'end')
        rbox.select_set(0,'end')
        ondelete()
    #清除选择
    def selectnone():
        lbox.select_clear(0,'end')
        rbox.select_clear(0,'end')
        offdelete()
    #反向选择
    def invertselect():
        select=lbox.curselection()
        if lbox.size()-len(select):
            selectall()
            for i in select:
                lbox.select_clear(i)
                rbox.select_clear(i)
            status.set([f'选中{str(len(lbox.curselection()))}个项目',
                        f'{str(len(lbox.curselection()))} selected'][lang.get()])
        else:
            selectnone()
    #状态栏文字更新
    def statustxt():
        if len(lbox.curselection()):
            status.set([f'选中{str(len(lbox.curselection()))}个项目',
                        f'{str(len(lbox.curselection()))} selected'][lang.get()])
        elif lbox.size():
            status.set([f'{str(lbox.size())}个项目',
                        f'{str(lbox.size())} item(s)'][lang.get()])
        else:
            status.set(['就绪','Ready'][lang.get()])
    #激活移除所选菜单
    def ondelete():
        status.set([f'选中{str(len(lbox.curselection()))}个项目',
                    f'{str(len(lbox.curselection()))} selected'][lang.get()])
        menufile.entryconfig(3,state='normal')
        win.bind('<Delete>',lambda e:remove())
    #禁用移除所选菜单
    def offdelete():
        status.set([f'{str(lbox.size())}个项目',
                    f'{str(lbox.size())} item(s)'][lang.get()])
        menufile.entryconfig(3,state='disabled')
        win.unbind('<Delete>')
    #列表框项目上移
    def moveup():
        for i in lbox.curselection():
            if not i:
                return 0
            lbox.insert(i+1,lbox.get(i-1))
            rbox.insert(i+1,rbox.get(i-1))
            lbox.delete(i-1)
            rbox.delete(i-1)
        return 1
    #列表框项目下移
    def movedown():
        for i in reversed(lbox.curselection()):
            if not lbox.size()-i-1:
                return 0
            lbox.insert(i,lbox.get(i+1))
            rbox.insert(i,rbox.get(i+1))
            lbox.delete(i+2)
            rbox.delete(i+2)
            lbox.see(i)
        return 1
    #列表框项目上移至顶
    def move2top():
        if lbox.size() and bool(len(lbox.curselection())):
            while moveup():
                pass
    #列表框项目下移至底
    def move2btom():
        if lbox.size() and bool(len(lbox.curselection())):
            while movedown():
                pass
    #列表框项目倒转排列
    def reverse():
        if lbox.size():
            selectnone()
            for i in range(1,rbox.size()):
                lbox.insert(0,lbox.get(i))
                rbox.insert(0,rbox.get(i))
                lbox.delete(i+1)
                rbox.delete(i+1)
    #检查新文件名是否含有非法字符
    def islegal(text):
        for i in text:
            if i in r'\/:*?"<>|':
                return 0
        return 1
    #删除新文件名首尾空格
    def striptxt():
        selectnone()
        for i in rbox.get(0,'end'):
            rbox.insert('end',i.strip())
            rbox.delete(0)
    #检查新文件名是否为空
    def isvalid():
        for i in range(rbox.size()):
            fn=path.splitext(rbox.get(i))[0]
            if not fn or fn.startswith('.'):
                lbox.select_set(i)
                rbox.select_set(i)
        if len(lbox.curselection()):
            ondelete()
            return 0
        return 1
    #检查右侧列表里是否有重名文件
    def isunique():
        for i in range(rbox.size()):
            if rbox.get(0,'end').count(rbox.get(i))-1:
                lbox.select_set(i)
                rbox.select_set(i)
        if len(lbox.curselection()):
            ondelete()
            return 0
        return 1
    #检查原文件有效性
    def isfound():
        global items
        items=listdir(getcwd())
        for i in range(rbox.size()):
            try:
                items.remove(lbox.get(i))
            except ValueError:
                lbox.select_set(i)
                rbox.select_set(i)
        if len(lbox.curselection()):
            ondelete()
            return 0
        return 1
    #检查新文件名是否与目录下其他文件重名
    def isharmony():
        global items
        for i in range(rbox.size()):
            if rbox.get(i) in items:
                lbox.select_set(i)
                rbox.select_set(i)
        if len(lbox.curselection()):
            ondelete()
            return 0
        return 1
    #检查新名称按钮
    def checknow():
        if lbox.size():
            striptxt()
            if not isfound():
                showinfo(message=['已标记未找到的项目。',
                                  'Item(s) not found marked.'][lang.get()])
                return
            if not isvalid():
                showinfo(message=['已标记为空或以"."开头的项目。',
                                  'Empty name(s) or item(s) that start with "." in list marked.'][lang.get()])
                return
            if not isunique():
                showinfo(message=['已标记列表内名称相同的项目。',
                                  'Duplicate names in list marked.'][lang.get()])
                return
            if not isharmony():
                showinfo(message=['已标记目录下名称相同的项目。',
                                  'Duplicate names in directory marked.'][lang.get()])
                return
            offdelete()
            showinfo(message=['没有发现问题。','No problems detected.'][lang.get()])
    #批量重命名按钮
    def renamenow():
        if lbox.size():
            striptxt()
            j=0     #成功项数目
            logs=[]     #使用列表记录错误日志
            line.config(state='normal')
            for i in range(rbox.size()-1,-1,-1):
                try:
                    rename(lbox.get(i),rbox.get(i))
                    line.delete('end')
                    lbox.delete(i)
                    rbox.delete(i)
                    j+=1
                except WindowsError as error:
                    file=path.join(getcwd(),lbox.get(i))
                    match error.winerror:
                        case 2:
                            logs.append([f'项目：{file}\n错误：系统找不到指定的文件。',
                                         f'Item: {file}\nError: The system cannot find the file specified.'][lang.get()])
                        case 3:
                            logs.append([f'项目：{file}\n错误：系统找不到指定的路径。',
                                         f'Item: {file}\nError: The system cannot find the path specified.'][lang.get()])
                        case 5:
                            logs.append([f'项目：{file}\n错误：拒绝访问。',
                                         f'Item: {file}\nError: Access is denied.'][lang.get()])
                        case 32:
                            logs.append([f'项目：{file}\n错误：另一个程序正在使用此文件，进程无法访问。',
                                         f'Item: {file}\nError: The process cannot access the file because it is being used by another process.'][lang.get()])
                        case 123:
                            logs.append([f'项目：{file}\n错误：文件名、目录名或卷标语法不正确。',
                                         f'Item: {file}\nError: The filename, directory name, or volume label syntax is incorrect.'][lang.get()])
                        case 183:
                            logs.append([f'项目：{file}\n错误：当文件已存在时，无法创建该文件。',
                                         f'Item: {file}\nError: Cannot create a file when that file already exists.'][lang.get()])
                        case _:
                            logs.append([f'项目：{file}\n错误：未知错误。',
                                         f'Item: {file}\nError: Uknown Error.'][lang.get()])
            line.config(state='disabled')
            if logs:    #未全部成功的情况
                offdelete()
                menuedit.entryconfig(0,state='disabled')
                menuedit.entryconfig(1,state='disabled')
                win.unbind('<Control-z>')
                win.unbind('<Control-Z>')
                win.unbind('<Control-y>')
                win.unbind('<Control-Y>')
                showinfo(message=[f'成功：{str(j)}，失败：{str(len(logs))}',
                                  f'Success: {str(j)},failure: {str(len(logs))}'][lang.get()],detail='\n'.join(logs))
            else:
                reset()
                showinfo(message=[f'成功：{str(j)}，失败：0',
                                  f'Success: {str(j)},failure: 0'][lang.get()])
    #备份操作
    def backup():
        global lbackup,rbackup  #分别备份左右列表项目
        selectnone()
        if not p.get()+1:   #如果p=-1，即初始状态下应用规则，则先初始化双表
            lbackup=[]
            rbackup=[]
        if len(lbackup)-p.get()-1:  #如果撤销后有新操作则清空此操作列表后的项目
            lbackup[p.get()+1:]=[]
            rbackup[p.get()+1:]=[]
        p.set(len(lbackup))     #更新p
        lbackup.append(lbox.get(0,'end'))
        rbackup.append(rbox.get(0,'end'))
        if p.get():     #如果p>=1，即应用第二次规则之后，激活撤销菜单
            menuedit.entryconfig(0,state='normal')
            menuedit.entryconfig(1,state='disabled')
            win.bind('<Control-z>',lambda e:undo())
            win.bind('<Control-Z>',lambda e:undo())
            win.unbind('<Control-y>')
            win.unbind('<Control-Y>')
    #菜单栏的撤销
    def undo():
        selectnone()
        p.set(p.get()-1)    #更新p
        lbox.delete(0,'end')
        rbox.delete(0,'end')
        for i in lbackup[p.get()]:  #导入左右列表上一个状态的内容
            lbox.insert('end',i)
        for i in rbackup[p.get()]:
            rbox.insert('end',i)
        menuedit.entryconfig(1,state='normal')  #撤销后激活重做
        win.bind('<Control-y>',lambda e:redo())
        win.bind('<Control-Y>',lambda e:redo())
        if not p.get():     #如果p=0，指向表头则禁止撤销
            menuedit.entryconfig(0,state='disabled')
            win.unbind('<Control-z>')
            win.unbind('<Control-Z>')
    #菜单栏的重做
    def redo():
        selectnone()
        p.set(p.get()+1)    #更新p
        lbox.delete(0,'end')
        rbox.delete(0,'end')
        for i in lbackup[p.get()]:  #导入左右列表下一个状态的内容
            lbox.insert('end',i)
        for i in rbackup[p.get()]:
            rbox.insert('end',i)
        menuedit.entryconfig(0,state='normal')  #重做后激活撤销
        win.bind('<Control-z>',lambda e:undo())
        win.bind('<Control-Z>',lambda e:undo())
        if not len(lbackup)-p.get()-1:  #如果p指向表尾则禁止重做
            menuedit.entryconfig(1,state='disabled')
            win.unbind('<Control-y>')
            win.unbind('<Control-Y>')
    #菜单栏的打开文件
    def openfile():
        if lbox.size():     #如果列表框非空则提醒用户
            if not askokcancel(message=['将会清空当前列表，要继续吗？',
                                        'The list will be cleared, continue?'][lang.get()]):
                return
        clear()
        files=askopenfilenames(title=['选择文件','Browse files'][lang.get()])
        if files:   #如果用户有选择文件
            chdir(path.split(files[0])[0])  #切换命令行工作目录
            load(files)
            itemtype.set('normal')  #文件状态下允许修改扩展名
            menurule.entryconfig(6,state='normal')
            win.bind('<F9>',lambda e:Extension())
    #菜单栏的打开文件夹
    def opendir():
        if lbox.size():
            if not askokcancel(message=['将会清空当前列表，要继续吗？',
                                        'The list will be cleared, continue?'][lang.get()]):
                return
        clear()
        fpath=askdirectory(title=['选择包含目标文件夹的目录',
                                  'Please select a directory that contains target folders'][lang.get()])
        if fpath:
            chdir(fpath)
            dirs=[]     #记录要重命名的文件夹
            for i in listdir(fpath):
                if path.isdir(i):
                    dirs.append(i)
            if not dirs:
                showerror(message=['选定目录下无任何子文件夹',
                                   'No folder found in selected directory'][lang.get()])
                return
            load(dirs)
            itemtype.set('disabled')    #文件夹状态下不允许修改扩展名
    #选择完文件或文件夹后初始化
    def load(selected):
        line.config(state='normal')
        for i,j in enumerate(selected,1):   #插入行号
            if i%spacing.get():
                line.insert('end','')
            else:
                line.insert('end',i)
            fname=path.split(j)[1]  #从完整路径中剥离文件名
            lbox.insert('end',fname)
            rbox.insert('end',fname)
        line.config(state='disabled')
        p.set(-1)   #初始化p指针
        backup()    #记录刚导入项目后的初始状态
        status.set([f'{str(lbox.size())}个项目',
                    f'{str(lbox.size())} item(s)'][lang.get()])
        menufile.entryconfig(4,state='normal')
        menuedit.entryconfig(3,state='normal')
        menuedit.entryconfig(4,state='normal')
        menuedit.entryconfig(5,state='normal')
        menurule.entryconfig(0,state='normal')
        menurule.entryconfig(1,state='normal')
        menurule.entryconfig(2,state='normal')
        menurule.entryconfig(3,state='normal')
        menurule.entryconfig(4,state='normal')
        menurule.entryconfig(5,state='normal')
        menurule.entryconfig(7,state='normal')
        win.bind('<Control-r>',lambda e:clear())
        win.bind('<Control-R>',lambda e:clear())
        win.bind('<Control-i>',lambda e:invertselect())
        win.bind('<Control-I>',lambda e:invertselect())
        win.bind('<Control-n>',lambda e:selectnone())
        win.bind('<Control-N>',lambda e:selectnone())
        win.bind('<F2>',lambda e:Edit())
        win.bind('<F3>',lambda e:Insert())
        win.bind('<F4>',lambda e:Replace())
        win.bind('<F5>',lambda e:Delete())
        win.bind('<F6>',lambda e:Erase())
        win.bind('<F7>',lambda e:Serialize())
        win.bind('<F8>',lambda e:Case())
    #菜单栏的移除所选
    def remove():
        line.config(state='normal')
        for i in reversed(lbox.curselection()):
            line.delete('end')
            lbox.delete(i)
            rbox.delete(i)
        line.config(state='disabled')
        if lbox.size():
            offdelete()
        else:
            reset()
    #菜单栏的移除全部
    def clear():
        line.config(state='normal')
        line.delete(0,'end')
        lbox.delete(0,'end')
        rbox.delete(0,'end')
        line.config(state='disabled')
        reset()
    #重置菜单栏和快捷键状态
    def reset():
        menufile.entryconfig(3,state='disabled')
        menufile.entryconfig(4,state='disabled')
        menuedit.entryconfig(0,state='disabled')
        menuedit.entryconfig(1,state='disabled')
        menuedit.entryconfig(3,state='disabled')
        menuedit.entryconfig(4,state='disabled')
        menuedit.entryconfig(5,state='disabled')
        menurule.entryconfig(0,state='disabled')
        menurule.entryconfig(1,state='disabled')
        menurule.entryconfig(2,state='disabled')
        menurule.entryconfig(3,state='disabled')
        menurule.entryconfig(4,state='disabled')
        menurule.entryconfig(5,state='disabled')
        menurule.entryconfig(6,state='disabled')
        menurule.entryconfig(7,state='disabled')
        status.set(['就绪','Ready'][lang.get()])
        win.unbind('<Delete>')
        win.unbind('<Control-r>')
        win.unbind('<Control-R>')
        win.unbind('<Control-z>')
        win.unbind('<Control-Z>')
        win.unbind('<Control-y>')
        win.unbind('<Control-Y>')
        win.unbind('<Control-i>')
        win.unbind('<Control-I>')
        win.unbind('<Control-n>')
        win.unbind('<Control-N>')
        win.unbind('<F2>')
        win.unbind('<F3>')
        win.unbind('<F4>')
        win.unbind('<F5>')
        win.unbind('<F6>')
        win.unbind('<F7>')
        win.unbind('<F8>')
        win.unbind('<F9>')
    #应用图标设定
    def seticon():
        style.configure('TButton',foreground='SystemButtonText')
        if fit:
            top.config(image=blacktop)
            up.config(image=blackup)
            flip.config(image=blackflip)
            down.config(image=blackdown)
            btom.config(image=blackbtom)
            blackicon()
        else:
            top.config(image=whitetop)
            up.config(image=whiteup)
            flip.config(image=whiteflip)
            down.config(image=whitedown)
            btom.config(image=whitebtom)
            whiteicon()
    #黑色图标用于经典主题
    def blackicon():
        to.config(image=blackto)
        menufile.entryconfig(0,image=blackfile)
        menufile.entryconfig(1,image=blackdir)
        menufile.entryconfig(3,image=blackdel)
        menufile.entryconfig(4,image=blackclear)
        menufile.entryconfig(6,image=blackexit)
        menuedit.entryconfig(0,image=blackundo)
        menuedit.entryconfig(1,image=blackredo)
        menuview.entryconfig(7,image=blackdec)
        menuview.entryconfig(8,image=blackinc)
        menuhelp.entryconfig(0,image=blacktips)
        menuhelp.entryconfig(2,image=blackpay)
        menuhelp.entryconfig(3,image=blackabout)
    #白色图标用于暗黑主题
    def whiteicon():
        to.config(image=whiteto)
        menufile.entryconfig(0,image=whitefile)
        menufile.entryconfig(1,image=whitedir)
        menufile.entryconfig(3,image=whitedel)
        menufile.entryconfig(4,image=whiteclear)
        menufile.entryconfig(6,image=whiteexit)
        menuedit.entryconfig(0,image=whiteundo)
        menuedit.entryconfig(1,image=whiteredo)
        menuview.entryconfig(7,image=whitedec)
        menuview.entryconfig(8,image=whiteinc)
        menuhelp.entryconfig(0,image=whitetips)
        menuhelp.entryconfig(2,image=whitepay)
        menuhelp.entryconfig(3,image=whiteabout)
    #菜单栏的系统主题
    def systemtheme():
        win.config(bg='SystemButtonFace')
        line.config(bg='SystemWindow')
        lbox.config(fg='SystemButtonText',bg='SystemWindow')
        rbox.config(fg='SystemButtonText',bg='SystemWindow')
        style.configure('TLabel',foreground='SystemButtonText',background='SystemButtonFace')
        style.configure('TButton',background='SystemButtonFace')
        seticon()
        style.configure('TLabelframe',background='SystemButtonFace')
        style.configure('TRadiobutton',foreground='SystemWindowText',background='SystemButtonFace')
        style.configure('TCheckbutton',foreground='SystemWindowText',background='SystemButtonFace')
        style.configure('TLabelframe.Label',foreground='SystemButtonText',background='#F0F0F0')
        menufile.config(fg='SystemButtonText',bg='SystemButtonFace')
        menuedit.config(fg='SystemButtonText',bg='SystemButtonFace')
        menurule.config(fg='SystemButtonText',bg='SystemButtonFace')
        menuview.config(fg='SystemButtonText',bg='SystemButtonFace',selectcolor='SystemButtonText')
        menulang.config(fg='SystemButtonText',bg='SystemButtonFace',selectcolor='SystemButtonText')
        menuhelp.config(fg='SystemButtonText',bg='SystemButtonFace')
    #菜单栏的经典主题
    def classictheme():
        win.config(bg='#F0F0F0')
        line.config(bg='#FFFFFF')
        lbox.config(fg='#000000',bg='#FFFFFF')
        rbox.config(fg='#000000',bg='#FFFFFF')
        style.configure('TLabel',foreground='#000000',background='#F0F0F0')
        style.configure('TButton',background='#F0F0F0')
        blackicon()
        style.configure('TLabelframe',background='#F0F0F0')
        style.configure('TRadiobutton',foreground='#000000',background='#F0F0F0')
        style.configure('TCheckbutton',foreground='#000000',background='#F0F0F0')
        style.configure('TLabelframe.Label',foreground='#000000',background='#F0F0F0')
        menufile.config(fg='#000000',bg='#F0F0F0')
        menuedit.config(fg='#000000',bg='#F0F0F0')
        menurule.config(fg='#000000',bg='#F0F0F0')
        menuview.config(fg='#000000',bg='#F0F0F0',selectcolor='#000000')
        menulang.config(fg='#000000',bg='#F0F0F0',selectcolor='#000000')
        menuhelp.config(fg='#000000',bg='#F0F0F0')
    #菜单栏的暗黑主题
    def darktheme():
        win.config(bg='#202020')
        line.config(bg='#2A2A2A')
        lbox.config(fg='#E0E0E0',bg='#2A2A2A')
        rbox.config(fg='#E0E0E0',bg='#2A2A2A')
        style.configure('TLabel',foreground='#E0E0E0',background='#202020')
        style.configure('TButton',background='#202020')
        whiteicon()
        style.configure('TLabelframe',background='#202020')
        style.configure('TRadiobutton',foreground='#E0E0E0',background='#202020')
        style.configure('TCheckbutton',foreground='#E0E0E0',background='#202020')
        style.configure('TLabelframe.Label',foreground='#E0E0E0',background='#202020')
        menufile.config(fg='#E0E0E0',bg='#202020')
        menuedit.config(fg='#E0E0E0',bg='#202020')
        menurule.config(fg='#E0E0E0',bg='#202020')
        menuview.config(fg='#E0E0E0',bg='#202020',selectcolor='#E0E0E0')
        menulang.config(fg='#E0E0E0',bg='#202020',selectcolor='#E0E0E0')
        menuhelp.config(fg='#E0E0E0',bg='#202020')
    #菜单栏的紧凑布局
    def tightlayout():
        line.config(selectborderwidth=0)
        lbox.config(selectborderwidth=0)
        rbox.config(selectborderwidth=0)
    #菜单栏的宽松布局
    def looselayout():
        line.config(selectborderwidth=2)
        lbox.config(selectborderwidth=2)
        rbox.config(selectborderwidth=2)
    #菜单栏的减小行号间距
    def decspacing():
        spacing.set(spacing.get()-1)
        line.config(state='normal')
        line.delete(0,'end')
        for i in range(rbox.size()):
            if (i+1)%spacing.get():
                line.insert('end','')
            else:
                line.insert('end',i+1)
        line.config(state='disabled')
        if not spacing.get()-1:     #如果间距为1则禁用减小行号间距菜单
            menuview.entryconfig(7,state='disabled')
    #菜单栏的增加行号间距
    def incspacing():
        spacing.set(spacing.get()+1)
        line.config(state='normal')
        line.delete(0,'end')
        for i in range(rbox.size()):
            if (i+1)%spacing.get():
                line.insert('end','')
            else:
                line.insert('end',i+1)
        line.config(state='disabled')
        if spacing.get()-1:     #如果间距>=1则激活减小行号间距菜单
            menuview.entryconfig(7,state='normal')


    ####子窗口内部逻辑####


    #插入窗口确定按钮
    def insnow(ins,add,pos,num,r2l,before,after,skip):
        if not add:     #如果用户输入为空
            showerror(message=['插入字段不能为空','Empty entry field'][lang.get()])
            return
        if not islegal(add):    #如果用户输入非法
            showerror(message=['插入字段不能包含下列任何字符：\n\\ / : * ? " < > |',
                               'Insert field must contain none the following characters:\n\\ / : * ? " < > |'][lang.get()])
            return
        isnum=num.isdecimal() and bool(int(num))    #判断位置字段是否为正整数
        match pos,isnum,bool(before),bool(after):   #先匹配异常情况以提前退出
            case 2,0,_,_:
                showerror(message=['位置字段必须是正整数',
                                   'Invalid position field, must be positive number'][lang.get()])
                return
            case 3,_,0,_:
                showerror(message=['文本前字段不能为空','Empty before-text field'][lang.get()])
                return
            case 4,_,_,0:
                showerror(message=['文本后字段不能为空','Empty after-text field'][lang.get()])
                return
        if isnum:   #如果位置字段为正整数则进行类型转换
            num=int(num)
            num-=1
        match pos,r2l,skip:
            case 0,_,_:     #插入到开头
                for i in rbox.get(0,'end'):
                    rbox.insert('end',add+i)
                    rbox.delete(0)
            case 1,_,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i+add)
                    rbox.delete(0)
            case 1,_,1:     #插入到末尾，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn+add+ex)
                    rbox.delete(0)
            case 2,0,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i[:num]+add+i[num:])
                    rbox.delete(0)
            case 2,0,1:     #到特定位置，从左往右，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn[:num]+add+fn[num:]+ex)
                    rbox.delete(0)
            case 2,1,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i[:-num]+add+i[-num:])
                    rbox.delete(0)
            case 2,1,1:     #到特定位置，从右往左，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn[:-num]+add+fn[-num:]+ex)
                    rbox.delete(0)
            case 3,_,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',sub(before,add+before,i,flags=I))
                    rbox.delete(0)
            case 3,_,1:     #到文本前，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',sub(before,add+before,fn,flags=I)+ex)
                    rbox.delete(0)
            case 4,_,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',sub(after,after+add,i,flags=I))
                    rbox.delete(0)
            case 4,_,1:     #到文本后，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',sub(after,after+add,fn,flags=I)+ex)
                    rbox.delete(0)
            case 5,_,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',add)
                    rbox.delete(0)
            case 5,_,1:     #替换当前名称，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',add+ex)
                    rbox.delete(0)
        backup()    #备份数据供日后撤销
        shut(ins)
    #替换窗口确定按钮
    def repnow(rep,old,new,caps,full,skip):
        if not old:
            showerror(message=['查找字段不能为空','Empty find field'][lang.get()])
            return
        if not islegal(new):
            showerror(message=['替换字段不能包含下列任何字符：\n\\ / : * ? " < > |',
                               'Replace field must contain none the following characters:\n\\ / : * ? " < > |'][lang.get()])
            return
        match caps,full,skip:
            case 0,0,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',sub(old,new,i,flags=I))
                    rbox.delete(0)
            case 0,0,1:     #不区分大小写，不匹配全字，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',sub(old,new,fn,flags=I)+ex)
                    rbox.delete(0)
            case 0,1,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',sub(fr'\b{old}\b',new,i,flags=I))
                    rbox.delete(0)
            case 0,1,1:     #不区分大小写，匹配全字，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',sub(fr'\b{old}\b',new,fn,flags=I)+ex)
                    rbox.delete(0)
            case 1,0,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',sub(old,new,i))
                    rbox.delete(0)
            case 1,0,1:     #区分大小写，不匹配全字，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',sub(old,new,fn)+ex)
                    rbox.delete(0)
            case 1,1,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',sub(fr'\b{old}\b',new,i))
                    rbox.delete(0)
            case 1,1,1:     #区分大小写，匹配全字，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',sub(fr'\b{old}\b',new,fn)+ex)
                    rbox.delete(0)
        backup()
        shut(rep)
    #删除窗口确定按钮
    def delnow(de1,old,caps,full,skip):
        if not old:
            showerror(message=['删除字段不能为空','Empty delete field'][lang.get()])
            return
        repnow(de1,old,'',caps,full,skip)
    #擦除窗口确定按钮
    def eranow(era,start,stop,num,sep,count,stopsep,keep,skip):
        isnum=num.isdecimal() and bool(int(num))    #判断位置字段是否为正整数
        iscount=count.isdecimal() and bool(int(count))  #判断计数字段是否为正整数
        match start,stop,isnum,bool(sep),iscount,bool(stopsep):     #先匹配异常情况以提前退出
            case 0,_,0,_,_,_:
                showerror(message=['位置字段必须是正整数',
                                   'Invalid position field, must be positive number'][lang.get()])
                return
            case 1,_,_,0,_,_:
                showerror(message=['起始分隔符不能为空','Empty start seperator'][lang.get()])
                return
            case _,0,_,_,0,_:
                showerror(message=['计数字段必须是正整数',
                                   'Invalid count field, must be positive number'][lang.get()])
                return
            case _,1,_,_,_,0:
                showerror(message=['终止分隔符不能为空','Empty stop seperator'][lang.get()])
                return
        if isnum:
            num=int(num)
            num-=1
        if iscount:
            count=int(count)
        match start,stop,keep,skip:
            case 0,0,_,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i[:num]+i[num+count:])
                    rbox.delete(0)
            case 0,0,_,1:   #擦除始于某个位置，直到某个计数，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn[:num]+fn[num+count:]+ex)
                    rbox.delete(0)
            case 0,1,0,0:
                for i in rbox.get(0,'end'):
                    stopnum=i.find(stopsep,num)
                    if stopnum+1:
                        rbox.insert('end',i[:num]+i[stopnum+len(stopsep):])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 0,1,0,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    stopnum=fn.find(stopsep,num)
                    if stopnum+1:
                        rbox.insert('end',fn[:num]+fn[stopnum+len(stopsep):]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 0,1,1,0:
                for i in rbox.get(0,'end'):
                    stopnum=i.find(stopsep,num)
                    if stopnum+1:
                        rbox.insert('end',i[:num]+i[stopnum:])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 0,1,1,1:   #始于某个位置，直到某个分隔符，保留分隔符，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    stopnum=fn.find(stopsep,num)
                    if stopnum+1:
                        rbox.insert('end',fn[:num]+fn[stopnum:]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 0,2,_,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i[:num])
                    rbox.delete(0)
            case 0,2,_,1:   #始于某个位置，直到末尾，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn[:num]+ex)
                    rbox.delete(0)
            case 1,0,0,0:
                for i in rbox.get(0,'end'):
                    num=i.find(sep)
                    if num+1:
                        rbox.insert('end',i[:num]+i[num+len(sep)+count:])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,0,0,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    num=fn.find(sep)
                    if num+1:
                        rbox.insert('end',fn[:num]+fn[num+len(sep)+count:]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,0,1,0:
                for i in rbox.get(0,'end'):
                    num=i.find(sep)
                    if num+1:
                        rbox.insert('end',i[:num+len(sep)]+i[num+len(sep)+count:])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,0,1,1:   #始于某个分隔符，直到某个计数，保留分隔符，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    num=fn.find(sep)
                    if num+1:
                        rbox.insert('end',fn[:num+len(sep)]+fn[num+len(sep)+count:]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,1,0,0:
                for i in rbox.get(0,'end'):
                    num=i.find(sep)
                    stopnum=i.find(stopsep,num+len(sep))
                    if num+1 and stopnum+1:
                        rbox.insert('end',i[:num]+i[stopnum+len(stopsep):])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,1,0,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    num=fn.find(sep)
                    stopnum=fn.find(stopsep,num+len(sep))
                    if num+1 and stopnum+1:
                        rbox.insert('end',fn[:num]+fn[stopnum+len(stopsep):]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,1,1,0:
                for i in rbox.get(0,'end'):
                    fn=path.splitext(i)[0]
                    num=i.find(sep)
                    stopnum=fn.find(stopsep,num+len(sep))
                    if num+1 and stopnum+1:
                        rbox.insert('end',i[:num+len(sep)]+i[stopnum:])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,1,1,1:   #始于某个分隔符，直到某个分隔符，保留分隔符，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    num=fn.find(sep)
                    stopnum=fn.find(stopsep,num+len(sep))
                    if num+1 and stopnum+1:
                        rbox.insert('end',fn[:num+len(sep)]+fn[stopnum:]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,2,0,0:
                for i in rbox.get(0,'end'):
                    fn=path.splitext(i)[0]
                    num=fn.find(sep)
                    if num+1:
                        rbox.insert('end',i[:num])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,2,0,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    num=fn.find(sep)
                    if num+1:
                        rbox.insert('end',fn[:num]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,2,1,0:
                for i in rbox.get(0,'end'):
                    fn=path.splitext(i)[0]
                    num=fn.find(sep)
                    if num+1:
                        rbox.insert('end',i[:num+len(sep)])
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
            case 1,2,1,1:   #始于某个分隔符，直到末尾，保留分隔符，忽略扩展名
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    num=fn.find(sep)
                    if num+1:
                        rbox.insert('end',fn[:num+len(sep)]+ex)
                    else:
                        rbox.insert('end',i)
                    rbox.delete(0)
        backup()
        shut(era)
    #编号窗口确定按钮
    def sernow(ser,start,step,repeat,cycle,gap,fill,pad,pos,num,skip):
        if not start.removeprefix('-').isdecimal():
            showerror(message=['初始值字段必须是整数',
                               'Invalid start field, must be integer'][lang.get()])
            return
        if not step.removeprefix('-').isdecimal():
            showerror(message=['增量字段必须是整数',
                               'Invalid step field, must be integer'][lang.get()])
            return
        if not (repeat.isdecimal() and bool(int(repeat))):
            showerror(message=['重复次数字段必须是正整数',
                               'Invalid repeat field, must be positive number'][lang.get()])
            return
        isgap=gap.isdecimal() and bool(int(gap))    #判断复位间隔字段是否为正整数
        ispad=pad.isdecimal() and bool(int(pad))    #判断补零长度字段是否为正整数
        isnum=num.isdecimal() and bool(int(num))    #判断位置字段是否为正整数
        match cycle,isgap,fill,ispad,pos,isnum:
            case 1,0,_,_,_,_:
                showerror(message=['复位间隔字段必须是正整数',
                                   'Invalid reset field, must be positive number'][lang.get()])
                return
            case _,_,1,0,_,_:
                showerror(message=['补零长度字段必须是正整数',
                                   'Invalid pad-with-zero field, must be positive number'][lang.get()])
                return
            case _,_,_,_,2,0:
                showerror(message=['位置字段必须是正整数',
                                   'Invalid position field, must be positive number'][lang.get()])
                return
        if isgap:
            gap=int(gap)
        if ispad and bool(fill):
            pad=int(pad)
        else:
            pad=0
        if isnum:
            num=int(num)
            num-=1
        j=0     #用于确定何时重置编号
        start=int(start)
        step=int(step)
        repeat=int(repeat)
        match cycle,pos,skip:
            case 0,0,_:
                for i in range(rbox.size()):
                    rbox.insert('end',str(start+i//repeat*step).zfill(pad)+rbox.get(0))
                    rbox.delete(0)
            case 0,1,0:
                for i in range(rbox.size()):
                    rbox.insert('end',rbox.get(0)+str(start+i//repeat*step).zfill(pad))
                    rbox.delete(0)
            case 0,1,1:
                for i in range(rbox.size()):
                    fn,ex=path.splitext(rbox.get(0))
                    rbox.insert('end',fn+str(start+i//repeat*step).zfill(pad)+ex)
                    rbox.delete(0)
            case 0,2,0:
                for i in range(rbox.size()):
                    rbox.insert('end',rbox.get(0)[:num]+str(start+i//repeat*step).zfill(pad)+rbox.get(0)[num:])
                    rbox.delete(0)
            case 0,2,1:
                for i in range(rbox.size()):
                    fn,ex=path.splitext(rbox.get(0))
                    rbox.insert('end',fn[:num]+str(start+i//repeat*step).zfill(pad)+fn[num:]+ex)
                    rbox.delete(0)
            case 0,3,0:
                for i in range(rbox.size()):
                    rbox.insert('end',str(start+i//repeat*step).zfill(pad))
                    rbox.delete(0)
            case 0,3,1:
                for i in range(rbox.size()):
                    fn,ex=path.splitext(rbox.get(0))
                    rbox.insert('end',str(start+i//repeat*step).zfill(pad)+ex)
                    rbox.delete(0)
            case 1,0,_:     #编号勾选复位间隔，插入到开头
                for i in range(rbox.size()):
                    if not i%gap:
                        j=0
                    rbox.insert('end',str(start+j//repeat*step).zfill(pad)+rbox.get(0))
                    rbox.delete(0)
                    j+=1
            case 1,1,0:
                for i in range(rbox.size()):
                    if not i%gap:
                        j=0
                    rbox.insert('end',rbox.get(0)+str(start+j//repeat*step).zfill(pad))
                    rbox.delete(0)
                    j+=1
            case 1,1,1:     #勾选复位间隔，插入到结尾，忽略扩展名
                for i in range(rbox.size()):
                    if not i%gap:
                        j=0
                    fn,ex=path.splitext(rbox.get(0))
                    rbox.insert('end',fn+str(start+j//repeat*step).zfill(pad)+ex)
                    rbox.delete(0)
                    j+=1
            case 1,2,0:
                for i in range(rbox.size()):
                    if not i%gap:
                        j=0
                    rbox.insert('end',rbox.get(0)[:num]+str(start+j//repeat*step).zfill(pad)+rbox.get(0)[num:])
                    rbox.delete(0)
                    j+=1
            case 1,2,1:     #勾选复位间隔，插入到特定位置，忽略扩展名
                for i in range(rbox.size()):
                    if not i%gap:
                        j=0
                    fn,ex=path.splitext(rbox.get(0))
                    rbox.insert('end',fn[:num]+str(start+j//repeat*step).zfill(pad)+fn[num:]+ex)
                    rbox.delete(0)
                    j+=1
            case 1,3,0:
                for i in range(rbox.size()):
                    if not i%gap:
                        j=0
                    rbox.insert('end',str(start+j//repeat*step).zfill(pad))
                    rbox.delete(0)
                    j+=1
            case 1,3,1:     #勾选复位间隔，替换当前名称，忽略扩展名
                for i in range(rbox.size()):
                    if not i%gap:
                        j=0
                    fn,ex=path.splitext(rbox.get(0))
                    rbox.insert('end',str(start+j//repeat*step).zfill(pad)+ex)
                    rbox.delete(0)
                    j+=1
        backup()
        shut(ser)
    #大小写窗口确定按钮
    def casnow(cas,case,skip):
        match case,skip:
            case 0,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i.title())
                    rbox.delete(0)
            case 0,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn.title()+ex)
                    rbox.delete(0)
            case 1,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i.capitalize())
                    rbox.delete(0)
            case 1,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn.capitalize()+ex)
                    rbox.delete(0)
            case 2,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i.upper())
                    rbox.delete(0)
            case 2,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn.upper()+ex)
                    rbox.delete(0)
            case 3,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i.lower())
                    rbox.delete(0)
            case 3,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn.lower()+ex)
                    rbox.delete(0)
            case 4,0:
                for i in rbox.get(0,'end'):
                    rbox.insert('end',i.swapcase())
                    rbox.delete(0)
            case 4,1:
                for i in rbox.get(0,'end'):
                    fn,ex=path.splitext(i)
                    rbox.insert('end',fn.swapcase()+ex)
                    rbox.delete(0)
        backup()
        shut(cas)
    #扩展名窗口确定按钮
    def extnow(ext,pos,new):
        if pos:
            if not new:
                showerror(message=['新扩展名不能为空','Empty new extension'][lang.get()])
                return
            if not islegal(new):
                showerror(message=['新扩展名不能包含下列任何字符：\n\\ / : * ? " < > |',
                                   'New extension must contain none the following characters:\n\\ / : * ? " < > |'][lang.get()])
                return
            for i in rbox.get(0,'end'):
                rbox.insert('end',f'{path.splitext(i)[0]}.{new}')
                rbox.delete(0)
        else:
            for i in rbox.get(0,'end'):
                rbox.insert('end',path.splitext(i)[0])
                rbox.delete(0)
        backup()
        shut(ext)
    #手动修改窗口确定按钮
    def edinow(panel,j,new):
        if not new:
            showerror(message=['新名称不能为空','Empty new name'][lang.get()])
            return
        if not islegal(new):
            showerror(message=['新名称不能包含下列任何字符：\n\\ / : * ? " < > |',
                               'New name must contain none the following characters:\n\\ / : * ? " < > |'][lang.get()])
            return
        selectnone()
        rbox.delete(j)
        rbox.insert(j,new)
        backup()
        panel.destroy()

    def payment(select,l3):
        match select:
            case 0:
                l3.config(text=['已选\n2元\n微信\n扫码',
                                'Donate\n$2 via\nWeChat'][lang.get()],image=pay2)
            case 1:
                l3.config(text=['已选\n5元\n微信\n扫码',
                                'Donate\n$5 via\nWeChat'][lang.get()],image=pay5)
            case 2:
                l3.config(text=['已选\n10元\n微信\n扫码',
                                'Donate\n$10 via\nWeChat'][lang.get()],image=pay10)
            case 3:
                l3.config(text=['微信\n扫码\n打赏',
                                'Donate\nany via\nWeChat'][lang.get()],image=payany)

    def run(b2):
        b2.place(x=160,y=30)
        b2.config(text=['咕咕咕','Not now'][lang.get()])
        b2.bind('<Enter>',lambda e:run2(b2))

    def run2(b2):
        b2.place(x=20,y=110)
        b2.config(text=['下次一定？','Next Time'][lang.get()])
        b2.bind('<Enter>',lambda e:run3(b2))

    def run3(b2):
        b2.grid(row=4,column=1,padx=4,pady=10,sticky='w',ipady=1)
        b2.config(text=['下次一定！','Later'][lang.get()])
        b2.unbind('<Enter>')


    ####子窗口交互界面####


    def Insert():
        ins=Toplevel()
        init(ins)
        ins.title(['插入','Insert'][lang.get()])
        pos=IntVar()
        r2l=IntVar()
        skip=IntVar()

        panel=Labelframe(ins,text=['配置：','Configuration:'][lang.get()])
        l1=Label(panel,text=['插入：','Insert:'][lang.get()])
        l2=Label(panel,text=['到：','Where:'][lang.get()])
        l3=Label(panel,text=['选项：','Option:'][lang.get()])
        e1=Entry(panel,width=40)
        r1=Radiobutton(panel,text=['开头','Start'][lang.get()],var=pos,value=0)
        r2=Radiobutton(panel,text=['末尾','End'][lang.get()],var=pos,value=1)
        r3=Radiobutton(panel,text=['位置：','Position:'][lang.get()],var=pos,value=2)
        s1=Spinbox(panel,width=4,from_=1,to=230)
        c1=Checkbutton(panel,text=['从右往左','Right-to-left'][lang.get()],var=r2l)
        r4=Radiobutton(panel,text=['文本前：','Before text:'][lang.get()],var=pos,value=3)
        e2=Entry(panel)
        r5=Radiobutton(panel,text=['文本后：','After text:'][lang.get()],var=pos,value=4)
        e3=Entry(panel)
        r6=Radiobutton(panel,text=['替换当前名称','Replace current name'][lang.get()],var=pos,value=5)
        c2=Checkbutton(panel,text=['忽略扩展名','Skip extension'][lang.get()],var=skip,state=itemtype.get())
        b1=Button(ins,text=['确定','OK'][lang.get()],
                  command=lambda:insnow(ins,e1.get(),pos.get(),s1.get(),
                                        r2l.get(),e2.get(),e3.get(),skip.get()))
        b2=Button(ins,text=['取消','Cancel'][lang.get()],command=lambda:shut(ins))
        e1.focus_set()
        s1.insert(0,1)
        pos.set(0)
        skip.set(1)

        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        l1.grid(row=0,column=0,padx=14,pady=4,sticky='w')
        l2.grid(row=2,column=0,padx=14,sticky='w')
        l3.grid(row=7,column=0,padx=14,pady=4,sticky='w')
        e1.grid(row=0,column=1,padx=(0,14),pady=4,sticky='w',columnspan=8)
        r1.grid(row=1,column=1,sticky='w')
        r2.grid(row=2,column=1,sticky='w')
        r3.grid(row=3,column=1,sticky='w')
        s1.grid(row=3,column=2,sticky='w')
        c1.grid(row=3,column=3,sticky='w')
        r4.grid(row=4,column=1,sticky='w')
        e2.grid(row=4,column=2,sticky='w',columnspan=2)
        r5.grid(row=5,column=1,sticky='w')
        e3.grid(row=5,column=2,sticky='w',columnspan=2)
        r6.grid(row=6,column=1,sticky='w',columnspan=2)
        c2.grid(row=7,column=1,pady=4,sticky='w',columnspan=2)
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)

        ins.bind('<Return>',lambda e:insnow(ins,e1.get(),pos.get(),s1.get(),
                                            r2l.get(),e2.get(),e3.get(),skip.get()))
        center(ins)

    def Replace():
        rep=Toplevel()
        init(rep)
        rep.title(['替换','Replace'][lang.get()])
        caps=IntVar()
        full=IntVar()
        skip=IntVar()

        panel=Labelframe(rep,text=['配置：','Configuration:'][lang.get()])
        l1=Label(panel,text=['查找：','Find:'][lang.get()])
        l2=Label(panel,text=['替换：','Replace with:'][lang.get()])
        l3=Label(panel,text=['选项：','Options:'][lang.get()])
        e1=Entry(panel,width=40)
        e2=Entry(panel,width=40)
        c1=Checkbutton(panel,text=['区分大小写','Match case'][lang.get()],var=caps)
        c2=Checkbutton(panel,text=['仅全字','Whole word'][lang.get()],var=full)
        c3=Checkbutton(panel,text=['忽略扩展名','Skip extension'][lang.get()],var=skip,state=itemtype.get())
        b1=Button(rep,text=['确定','OK'][lang.get()],
                  command=lambda:repnow(rep,e1.get(),e2.get(),caps.get(),full.get(),skip.get()))
        b2=Button(rep,text=['取消','Cancel'][lang.get()],command=lambda:shut(rep))
        e1.focus_set()
        skip.set(1)

        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        l1.grid(row=0,column=0,padx=14,pady=4,sticky='w')
        l2.grid(row=1,column=0,padx=14,pady=4,sticky='w')
        l3.grid(row=2,column=0,padx=14,pady=4,sticky='w')
        e1.grid(row=0,column=1,padx=(0,14),pady=4,sticky='w',columnspan=4)
        e2.grid(row=1,column=1,padx=(0,14),pady=4,sticky='w',columnspan=4)
        c1.grid(row=2,column=2,padx=14,pady=4,sticky='w')
        c2.grid(row=2,column=3,padx=14,pady=4,sticky='w')
        c3.grid(row=3,column=2,padx=14,pady=4,sticky='w')
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)

        rep.bind('<Return>',lambda e:repnow(rep,e1.get(),e2.get(),caps.get(),full.get(),skip.get()))
        center(rep)

    def Delete():
        de1=Toplevel()
        init(de1)
        de1.title(['删除','Delete'][lang.get()])
        caps=IntVar()
        full=IntVar()
        skip=IntVar()

        panel=Labelframe(de1,text=['配置：','Configuration:'][lang.get()])
        l1=Label(panel,text=['删除：','Delete:'][lang.get()])
        l2=Label(panel,text=['选项：','Options:'][lang.get()])
        e1=Entry(panel,width=40)
        c1=Checkbutton(panel,text=['区分大小写','Match case'][lang.get()],var=caps)
        c2=Checkbutton(panel,text=['仅全字','Whole word'][lang.get()],var=full)
        c3=Checkbutton(panel,text=['忽略扩展名','Skip extension'][lang.get()],var=skip,state=itemtype.get())
        b1=Button(de1,text=['确定','OK'][lang.get()],
                  command=lambda:delnow(de1,e1.get(),caps.get(),full.get(),skip.get()))
        b2=Button(de1,text=['取消','Cancel'][lang.get()],command=lambda:shut(de1))
        e1.focus_set()
        skip.set(1)

        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        l1.grid(row=0,column=0,padx=14,pady=4,sticky='w')
        l2.grid(row=1,column=0,padx=14,pady=4,sticky='w')
        e1.grid(row=0,column=1,padx=(0,14),pady=4,sticky='w',columnspan=4)
        c1.grid(row=1,column=2,padx=14,pady=4,sticky='w')
        c2.grid(row=1,column=3,padx=14,pady=4,sticky='w')
        c3.grid(row=2,column=2,padx=14,pady=4,sticky='w')
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)

        de1.bind('<Return>',lambda e:delnow(de1,e1.get(),caps.get(),full.get(),skip.get()))
        center(de1)

    def Erase():
        era=Toplevel()
        init(era)
        era.title(['擦除','Erase'][lang.get()])
        start=IntVar()
        stop=IntVar()
        keep=IntVar()
        skip=IntVar()

        panel=Labelframe(era,text=['配置：','Configuration:'][lang.get()])
        p1=Labelframe(panel,text=['始于：','From:'][lang.get()])
        p2=Labelframe(panel,text=['直到：','Until:'][lang.get()])
        l1=Label(panel,text=['擦除：','Erase:'][lang.get()])
        l2=Label(panel,text=['选项：','Options:'][lang.get()])
        r1=Radiobutton(p1,text=['位置：','Position:'][lang.get()],var=start,value=0)
        s1=Spinbox(p1,width=4,from_=1,to=230)
        r2=Radiobutton(p1,text=['分隔符：','Seperator:'][lang.get()],var=start,value=1)
        e1=Entry(p1,width=6)
        r3=Radiobutton(p2,text=['计数：','Count:'][lang.get()],var=stop,value=0)
        s2=Spinbox(p2,width=4,from_=1,to=230)
        r4=Radiobutton(p2,text=['分隔符：','Seperator:'][lang.get()],var=stop,value=1)
        e2=Entry(p2,width=6)
        r5=Radiobutton(p2,text=['直到末尾','Till the end'][lang.get()],var=stop,value=2)
        c1=Checkbutton(panel,text=['保留分隔符','Keep seperator'][lang.get()],var=keep)
        c2=Checkbutton(panel,text=['忽略扩展名','Skip extension'][lang.get()],var=skip,state=itemtype.get())
        b1=Button(era,text=['确定','OK'][lang.get()],
                  command=lambda:eranow(era,start.get(),stop.get(),s1.get(),e1.get(),
                                        s2.get(),e2.get(),keep.get(),skip.get()))
        b2=Button(era,text=['取消','Cancel'][lang.get()],command=lambda:shut(era))
        s1.focus_set()
        s1.insert(0,1)
        s2.insert(0,1)
        start.set(0)
        stop.set(0)
        skip.set(1)

        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        p1.grid(row=0,column=1,pady=4,sticky='n',rowspan=2,columnspan=2)
        p2.grid(row=0,column=3,padx=14,pady=4,rowspan=3,columnspan=2)
        l1.grid(row=0,column=0,padx=14,pady=4,sticky='w')
        l2.grid(row=3,column=0,padx=14,pady=4,sticky='w')
        r1.grid(row=0,column=0,padx=8,pady=4,sticky='w')
        s1.grid(row=0,column=1,padx=(0,8),pady=4,sticky='w')
        r2.grid(row=1,column=0,padx=8,pady=4,sticky='w')
        e1.grid(row=1,column=1,padx=(0,8),pady=4,sticky='w')
        r3.grid(row=0,column=0,padx=8,pady=4,sticky='w')
        s2.grid(row=0,column=1,padx=(0,8),pady=4,sticky='w')
        r4.grid(row=1,column=0,padx=8,pady=4,sticky='w')
        e2.grid(row=1,column=1,padx=(0,8),pady=4,sticky='w')
        r5.grid(row=2,column=0,padx=8,pady=4,sticky='w',columnspan=2)
        c1.grid(row=3,column=2,pady=4,sticky='w')
        c2.grid(row=3,column=3,padx=24,pady=4,sticky='w')
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)

        era.bind('<Return>',lambda e:eranow(era,start.get(),stop.get(),s1.get(),e1.get(),
                                            s2.get(),e2.get(),keep.get(),skip.get()))
        center(era)

    def Serialize():
        ser=Toplevel()
        init(ser)
        ser.title(['编号','Serialize'][lang.get()])
        pos=IntVar()
        cycle=IntVar()
        fill=IntVar()
        skip=IntVar()

        panel=Labelframe(ser,text=['配置：','Configuration:'][lang.get()])
        p1=Labelframe(panel,text=['插入到：','Insert where:'][lang.get()])
        l1=Label(panel,text=['初始值：','Start from:'][lang.get()])
        l2=Label(panel,text=['增量：','Step:'][lang.get()])
        l3=Label(panel,text=['重复次数：','Repeat times:'][lang.get()])
        l4=Label(panel,text=['选项：','Option:'][lang.get()])
        s1=Spinbox(panel,width=4,from_=-99999999,to=99999999)
        s2=Spinbox(panel,width=4,from_=-99999999,to=99999999)
        s3=Spinbox(panel,width=4,from_=1,to=9999)
        c1=Checkbutton(panel,text=['复位间隔：','Reset every:'][lang.get()],var=cycle)
        s4=Spinbox(panel,width=4,from_=1,to=9999)
        c2=Checkbutton(panel,text=['补零长度：','Pad with zero:'][lang.get()],var=fill)
        s5=Spinbox(panel,width=4,from_=1,to=230)
        r1=Radiobutton(p1,text=['开头','Start'][lang.get()],var=pos,value=0)
        r2=Radiobutton(p1,text=['末尾','End'][lang.get()],var=pos,value=1)
        r3=Radiobutton(p1,text=['位置：','Position:'][lang.get()],var=pos,value=2)
        s6=Spinbox(p1,width=4,from_=1,to=230)
        r4=Radiobutton(p1,text=['替换当前名称','Replace current name'][lang.get()],var=pos,value=3)
        c3=Checkbutton(panel,text=['忽略扩展名','Skip extension'][lang.get()],var=skip,state=itemtype.get())
        b1=Button(ser,text=['确定','OK'][lang.get()],
                  command=lambda:sernow(ser,s1.get(),s2.get(),s3.get(),cycle.get(),s4.get(),
                                        fill.get(),s5.get(),pos.get(),s6.get(),skip.get()))
        b2=Button(ser,text=['取消','Cancel'][lang.get()],command=lambda:shut(ser))
        s1.focus_set()
        s1.insert(0,1)
        s2.insert(0,1)
        s3.insert(0,1)
        s4.insert(0,1)
        s5.insert(0,1)
        s6.insert(0,1)
        pos.set(0)
        skip.set(1)

        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        p1.grid(row=0,column=2,padx=14,pady=4,rowspan=5,columnspan=2)
        l1.grid(row=0,column=0,padx=14,pady=4,sticky='w')
        l2.grid(row=1,column=0,padx=14,pady=4,sticky='w')
        l3.grid(row=2,column=0,padx=14,pady=4,sticky='w')
        l4.grid(row=5,column=0,padx=14,pady=4,sticky='w')
        s1.grid(row=0,column=1,pady=4,sticky='w')
        s2.grid(row=1,column=1,pady=4,sticky='w')
        s3.grid(row=2,column=1,pady=4,sticky='w')
        c1.grid(row=3,column=0,padx=14,pady=4,sticky='w')
        s4.grid(row=3,column=1,pady=4,sticky='w')
        c2.grid(row=4,column=0,padx=14,pady=4,sticky='w')
        s5.grid(row=4,column=1,pady=4,sticky='w')
        r1.grid(row=0,column=0,padx=8,pady=4,sticky='w')
        r2.grid(row=1,column=0,padx=8,pady=4,sticky='w')
        r3.grid(row=2,column=0,padx=8,pady=4,sticky='w')
        s6.grid(row=2,column=1,padx=(0,8),pady=4,sticky='w')
        r4.grid(row=3,column=0,padx=8,pady=4,sticky='w',columnspan=2)
        c3.grid(row=5,column=1,pady=4,sticky='w',columnspan=2)
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)

        ser.bind('<Return>',lambda e:sernow(ser,s1.get(),s2.get(),s3.get(),cycle.get(),s4.get(),
                                            fill.get(),s5.get(),pos.get(),s6.get(),skip.get()))
        center(ser)

    def Case():
        cas=Toplevel()
        init(cas)
        cas.title(['大小写','Case'][lang.get()])
        cap=IntVar()
        skip=IntVar()

        panel=Labelframe(cas,text=['配置：','Configuration:'][lang.get()])
        l1=Label(panel,text=['大小写变更：','Case change:'][lang.get()])
        l2=Label(panel,text=['选项：','Option:'][lang.get()])
        r1=Radiobutton(panel,text=['仅大写每个单词首字母','Capitalize Every Word'][lang.get()],var=cap,value=0)
        r2=Radiobutton(panel,text=['仅大写句首字母','First letter capital'][lang.get()],var=cap,value=1)
        r3=Radiobutton(panel,text=['全部大写','ALL UPPER CASE'][lang.get()],var=cap,value=2)
        r4=Radiobutton(panel,text=['全部小写','all lower case'][lang.get()],var=cap,value=3)
        r5=Radiobutton(panel,text=['翻转大小写','iNVERT cASE'][lang.get()],var=cap,value=4)
        c1=Checkbutton(panel,text=['忽略扩展名','Skip extension'][lang.get()],var=skip,state=itemtype.get())
        b1=Button(cas,text=['确定','OK'][lang.get()],command=lambda:casnow(cas,cap.get(),skip.get()))
        b2=Button(cas,text=['取消','Cancel'][lang.get()],command=lambda:shut(cas))
        cap.set(0)
        skip.set(1)

        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        l1.grid(row=0,column=0,padx=14,sticky='w')
        l2.grid(row=5,column=0,padx=14,pady=8,sticky='w')
        r1.grid(row=0,column=1,padx=(0,14),sticky='w')
        r2.grid(row=1,column=1,padx=(0,14),sticky='w')
        r3.grid(row=2,column=1,padx=(0,14),sticky='w')
        r4.grid(row=3,column=1,padx=(0,14),sticky='w')
        r5.grid(row=4,column=1,padx=(0,14),sticky='w')
        c1.grid(row=5,column=1,pady=8,sticky='w')
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)

        cas.bind('<Return>',lambda e:casnow(cas,cap.get(),skip.get()))
        center(cas)

    def Extension():
        ext=Toplevel()
        init(ext)
        ext.title(['扩展名','Extension'][lang.get()])
        pos=IntVar()

        panel=Labelframe(ext,text=['配置：','Configuration:'][lang.get()])
        r1=Radiobutton(panel,text=['新扩展名：\n(无需 . )','New extension:\n(dot-free)'][lang.get()],var=pos,value=1)
        e1=Entry(panel,width=20)
        r2=Radiobutton(panel,text=['删除当前扩展名','Delete current extension'][lang.get()],var=pos,value=0)
        b1=Button(ext,text=['确定','OK'][lang.get()],command=lambda:extnow(ext,pos.get(),e1.get()))
        b2=Button(ext,text=['取消','Cancel'][lang.get()],command=lambda:shut(ext))
        e1.focus_set()
        pos.set(1)

        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        r1.grid(row=0,column=0,padx=14,pady=4,sticky='w')
        e1.grid(row=0,column=1,padx=(0,14),pady=4,sticky='w')
        r2.grid(row=1,column=0,padx=14,pady=4,sticky='w',columnspan=2)
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)

        ext.bind('<Return>',lambda e:extnow(ext,pos.get(),e1.get()))
        center(ext)

    def Edit():
        select=rbox.curselection()
        if not select:
            showerror(message=['请先选中一项','Please select an item first'][lang.get()])
            return

        edi=Toplevel()
        init(edi)
        edi.title(['编辑新名称','Edit New Name'][lang.get()])

        b1=Button(edi,text=['确定','OK'][lang.get()],command=lambda:edinow(panel,j,e1.get()))
        b2=Button(edi,text=['取消','Cancel'][lang.get()],command=lambda:shut(edi))
        b1.grid(row=1,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)
        edi.bind('<Return>',lambda e:edinow(panel,j,e1.get()))

        for i,j in enumerate(select):
            if not edi.winfo_exists():
                break
            panel=Labelframe(edi,text=[f'进度：{str(i+1)}/{str(len(select))}',
                                       f'Process: {str(i+1)}/{str(len(select))}'][lang.get()])
            l1=Label(panel,text=['当前名称：','Current name:'][lang.get()])
            l2=Label(panel,text=lbox.get(j))
            l3=Label(panel,text=['新名称：','New name:'][lang.get()])
            e1=Entry(panel,width=40)
            e1.focus_set()
            e1.insert(0,rbox.get(j))
            pos=rbox.get(j).rfind('.')
            if pos+1:
                e1.selection_range(0,pos)
                e1.icursor(pos)
            else:
                e1.selection_range(0,'end')

            panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
            l1.grid(row=0,column=0,padx=14,pady=4,sticky='w')
            l2.grid(row=0,column=1,padx=(1,14),pady=4,sticky='w')
            l3.grid(row=1,column=0,padx=14,pady=4,sticky='w')
            e1.grid(row=1,column=1,padx=(0,14),pady=4,sticky='w')
            center(edi)
            edi.wait_window(panel)
        shut(edi)

    def Chinese():
        menubar.entryconfig(1,label='文件(F)',underline=3)
        menubar.entryconfig(2,label='编辑(E)',underline=3)
        menubar.entryconfig(3,label='规则(R)',underline=3)
        menubar.entryconfig(4,label='查看(V)',underline=3)
        menubar.entryconfig(5,label='语言(L)',underline=3)
        menubar.entryconfig(6,label='帮助(H)',underline=3)

        menufile.entryconfig(0,label='添加文件(F)',underline=5)
        menufile.entryconfig(1,label='添加文件夹(D)',underline=5)
        menufile.entryconfig(3,label='移除所选(S)',underline=5)
        menufile.entryconfig(4,label='移除全部(R)',underline=5)
        menufile.entryconfig(6,label='退出(X)',underline=3)

        menuedit.entryconfig(0,label='撤销(U)',underline=3)
        menuedit.entryconfig(1,label='重做(R)',underline=3)
        menuedit.entryconfig(3,label='全部选择(A)',underline=5)
        menuedit.entryconfig(4,label='全部取消(N)',underline=5)
        menuedit.entryconfig(5,label='反向选择(I)',underline=5)

        menurule.entryconfig(0,label='插入(I)',underline=3)
        menurule.entryconfig(1,label='替换(R)',underline=3)
        menurule.entryconfig(2,label='删除(D)',underline=3)
        menurule.entryconfig(3,label='擦除(E)',underline=3)
        menurule.entryconfig(4,label='编号(S)',underline=3)
        menurule.entryconfig(5,label='大小写(C)',underline=4)
        menurule.entryconfig(6,label='扩展名(X)',underline=4)
        menurule.entryconfig(7,label='手动修改(M)',underline=5)

        menuview.entryconfig(0,label='系统主题')
        menuview.entryconfig(1,label='经典主题')
        menuview.entryconfig(2,label='暗黑主题')
        menuview.entryconfig(4,label='紧凑布局')
        menuview.entryconfig(5,label='宽松布局')
        menuview.entryconfig(7,label='减少行号间距')
        menuview.entryconfig(8,label='增加行号间距')

        menuhelp.entryconfig(0,label='快速上手(Q)',underline=5)
        menuhelp.entryconfig(2,label='赞助作者(D)',underline=5)
        menuhelp.entryconfig(3,label='关于(A)',underline=3)
        win.title('Batch Renamer (仅供非商业使用)')
        llbl.config(text='当前名称')
        rlbl.config(text='新名称')
        see.config(text='检查新名称')
        do.config(text='批量重命名')
        status.set('就绪')

    def English():
        menubar.entryconfig(1,label='File',underline=0)
        menubar.entryconfig(2,label='Edit',underline=0)
        menubar.entryconfig(3,label='Rule',underline=0)
        menubar.entryconfig(4,label='View',underline=0)
        menubar.entryconfig(5,label='Language',underline=0)
        menubar.entryconfig(6,label='Help',underline=0)

        menufile.entryconfig(0,label='Add Files',underline=4)
        menufile.entryconfig(1,label='Add Folders',underline=7)
        menufile.entryconfig(3,label='Remove Selected',underline=7)
        menufile.entryconfig(4,label='Remove All',underline=0)
        menufile.entryconfig(6,label='Exit',underline=1)

        menuedit.entryconfig(0,label='Undo',underline=0)
        menuedit.entryconfig(1,label='Redo',underline=0)
        menuedit.entryconfig(3,label='Select All',underline=7)
        menuedit.entryconfig(4,label='Select None',underline=7)
        menuedit.entryconfig(5,label='Invert Selection',underline=0)

        menurule.entryconfig(0,label='Insert',underline=0)
        menurule.entryconfig(1,label='Replace',underline=0)
        menurule.entryconfig(2,label='Delete',underline=0)
        menurule.entryconfig(3,label='Erase',underline=0)
        menurule.entryconfig(4,label='Serialize',underline=0)
        menurule.entryconfig(5,label='Case',underline=0)
        menurule.entryconfig(6,label='Extension',underline=1)
        menurule.entryconfig(7,label='Edit Manually',underline=5)

        menuview.entryconfig(0,label='System Theme')
        menuview.entryconfig(1,label='Classic Theme')
        menuview.entryconfig(2,label='Dark Theme')
        menuview.entryconfig(4,label='Tight Layout')
        menuview.entryconfig(5,label='Loose Layout')
        menuview.entryconfig(7,label='Line No. Spacing -')
        menuview.entryconfig(8,label='Line No. Spacing +')

        menuhelp.entryconfig(0,label='Quick Guide',underline=0)
        menuhelp.entryconfig(2,label='Donate',underline=0)
        menuhelp.entryconfig(3,label='About',underline=0)
        win.title('Batch Renamer (non-commercial use only)')
        llbl.config(text='Current Name')
        rlbl.config(text='New Name')
        see.config(text='Check Names')
        do.config(text='Rename In Batches')
        status.set('Ready')

    def Tips():
        tip=Toplevel()
        init(tip)
        tip.title(['快速上手','Quick Guide'][lang.get()])

        panel=Labelframe(tip,text=['使用教程：','Tutorial:'][lang.get()])
        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=2)
        Label(panel,text=['1. 点击 文件 以添加要批量重命名的文件/文件夹',
                          '1. Click File to add files/folders to be renamed in batches'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['2. 添加文件时，在空白处拖动鼠标多选，按住Ctrl并单击以翻转选择',
                          '2. For files, drag mouse in blank to multi-select, hold Ctrl and click a file to invert'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['3. 添加文件夹时，将它们放在同一目录下再选择此目录',
                          '3. For folders, select the identical parent directory where you put them'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['4. 点击 规则 以添加各种规则，右侧列表将实时显示预览',
                          '4. Click Rule to add various rules and previews can be seen in New Name list'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['5. 要应用编号规则，请先使用箭头按钮调整项目顺序',
                          '5. Click arrow buttons to reorder items if rule Serialize to be used'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['6. 要撤销一个规则，请点击 编辑-撤销',
                          '6. To revoke a rule, click Edit-Undo'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['7. 检查无误后，点击 批量重命名 使所有更改生效',
                          '7. If there\'s no error, click Rename In Batches to apply all changes'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['感谢您选择Batch Renamer！',
                          'Thank you for choosing Batch Renamer!'][lang.get()]).pack(padx=20,pady=4)
        b1=Button(tip,text=['关闭','Close'][lang.get()],command=lambda:shut(tip))
        b1.grid(row=1,column=1,padx=4,pady=10,sticky='w',ipady=1)
        tip.bind('<Return>',lambda e:shut(tip))
        center(tip)

    def Pay():
        pay=Toplevel()
        init(pay)
        pay.title(['赞助','Donate'][lang.get()])

        l1=Label(pay,text=['如果你觉得此程序帮到了\n你，赏我一下如何？','If you think it helpful,\nhow about buying me:'][lang.get()])
        l2=Label(pay,text=['感谢这些朋友的支持：','Special thanks to:'][lang.get()])
        l3=Label(pay,text=['已选\n5元\n微信\n扫码','Donate\n￥5 via\nWeChat'][lang.get()],image=pay5,compound='right')
        llist=Listbox(pay,height=1,exportselection=0,highlightthickness=0)
        rlist=Listbox(pay,height=10,exportselection=0,highlightthickness=0)
        llist.config(fg=['SystemButtonText','#000000','#E0E0E0'][theme.get()],bg=['SystemWindow','#FFFFFF','#2A2A2A'][theme.get()])
        rlist.config(fg=['SystemButtonText','#000000','#E0E0E0'][theme.get()],bg=['SystemWindow','#FFFFFF','#2A2A2A'][theme.get()])
        b1=Button(pay,text=['我已付款','Donated'][lang.get()],
                  command=lambda:[showinfo(message=['非常感谢您，今后我会做得更好','Thank you soooooo muchXDDD'][lang.get()]),shut(pay)])
        b2=Button(pay,text=['下次一定','Later'][lang.get()],command=lambda:shut(pay))

        l1.grid(row=0,column=0,pady=4)
        l2.grid(row=0,column=1,pady=4)
        l3.grid(row=2,column=0,pady=4,rowspan=2)
        llist.grid(row=1,column=0,padx=4,pady=4,sticky='nsew')
        rlist.grid(row=1,column=1,padx=4,pady=4,sticky='nsew',rowspan=3)
        b1.grid(row=4,column=0,padx=4,pady=10,sticky='e',ipady=1)
        b2.grid(row=4,column=1,padx=4,pady=10,sticky='w',ipady=1)

        llist.insert('end',['一包辣条 --2元','A cup of tea'][lang.get()])
        llist.insert('end',['一个鸡腿 --5元','A beer'][lang.get()])
        llist.insert('end',['一块汉堡 --10元','A burger'][lang.get()])
        llist.insert('end',['自定义金额','Custom'][lang.get()])
        llist.select_set(1)

        rlist.insert('end',['1. believer --66.66元','1. Pacman --$20.48'][lang.get()])
        rlist.insert('end',['2. 狼火本火 --20元','2. Anthony --$15'][lang.get()])
        rlist.insert('end',['3. 996先生 --15元','3. user000 --$14.99'][lang.get()])
        rlist.insert('end',['4. 。 --10元','4. Lucy --$10.24'][lang.get()])
        rlist.insert('end',['5. greenray --10元','5. wannahug --$9.99'][lang.get()])
        rlist.insert('end',['6. 饕餮 --6.6元','6. LazyDog --$5'][lang.get()])
        rlist.insert('end',['7. return(0) --5元','7. return(0) --$5'][lang.get()])
        rlist.insert('end',['8. 往事随她 --5元','8. Yesir --$3'][lang.get()])
        rlist.insert('end',['9. 你还欠我一行代码 --2元','9. Tempermoney --$2'][lang.get()])

        llist.bind('<<ListboxSelect>>',lambda e:payment(llist.curselection()[0],l3))
        b2.bind('<Enter>',lambda e:run(b2))
        pay.protocol('WM_DELETE_WINDOW',lambda:center(pay))
        center(pay)
        win.wait_window(pay)

    def About():
        abo=Toplevel()
        init(abo)
        abo.title(['关于','About'][lang.get()])

        panel=Labelframe(abo,text='© 2023 verifyurhuman@github')
        panel.grid(row=0,column=0,padx=14,pady=(8,0))
        link=Label(abo,cursor='hand2',image=[[whitegit,blackgit][fit],blackgit,whitegit][theme.get()])
        link.grid(row=0,column=0,padx=16,pady=20,sticky='ne')
        Label(panel,text='Batch Renamer',font=('Georgia',18),image=icon,compound='left').pack(pady=10)
        Label(panel,text=['版本：3.4','Version: 3.4'][lang.get()]).pack()
        Label(panel,text=['作者：verifyurhuman','Author: verifyurhuman'][lang.get()]).pack()
        Label(panel,text=['图形界面：Tkinter','GUI: Tkinter'][lang.get()]).pack()
        Label(panel,text=['开发工具：Python','Developing tool: Python'][lang.get()]).pack()
        Label(panel,text=['发行日期：2021年10月21日','Released on: Oct 21, 2021'][lang.get()]).pack()
        Label(panel,text=['更新日期：2023年10月24日','Updated on: Oct 24, 2023'][lang.get()]).pack()
        Label(panel,text=['用户协议：GNU AGPL-3.0','License: GNU AGPL-3.0'][lang.get()]).pack()
        Label(panel,text=['免责声明：本软件是开源免费软件，请勿用于商业用途，\n               严禁盗卖本软件。使用期间一切后果自负',
                          'Disclaimer: Batch Renamer is a freeware. Do not sell it.\n                 Do not use it for any commercial purpose.\n                 Use it at your own risk.'][lang.get()]).pack(padx=10,pady=10)
        Button(abo,text=['确定','OK'][lang.get()],command=lambda:shut(abo)).grid(row=1,column=0,pady=10,ipady=1)

        abo.bind('<Return>',lambda e:shut(abo))
        link.bind('<Button-1>',lambda e:open_new('https://github.com/verifyurhuman/Batch-Renamer'))
        center(abo)

    def Tos():
        tos=Toplevel()
        init(tos)
        tos.title(['服务条款','Terms of Service'][lang.get()])
        accept=StringVar()

        panel=Labelframe(tos,text=['在使用本程序前，请您仔细阅读以下服务条款。\n若您不同意条款的部分或全部内容，则不得使用本程序。\n',
                                   'Please read the ToS before using this program:\nYou shall not use this program if you disagree with any term below.\n'][lang.get()])
        panel.grid(row=0,column=0,padx=14,pady=(8,0),columnspan=3)
        Label(panel,text=['1. 任何个人和组织不得将此程序用于商业用途，\n或利用此程序以任何形式牟利。\n',
                          '1. Any individual and organization shall not use this program for\ncommercial purpose, or make profit with it in any form.\n'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['2. 此程序遵循 GNU AGPL-3.0 开源协议，\n因此用户需自行承担使用本程序所造成的一切后果。\n',
                          '2. This program follows GNU AGPL-3.0 open-source guideline,\nso use it at your own risk.\n'][lang.get()]).pack(anchor='w',padx=20)
        Label(panel,text=['3. 您可以通过赞助来支持作者的开发工作。\n',
                          '3. Please consider a donation to support our future development.\n'][lang.get()]).pack(anchor='w',padx=20)
        b1=Button(tos,text='English',state=['normal','disabled'][lang.get()],command=lambda:[shut(tos),lang.set(1),English(),Tos()])
        b2=Button(tos,text='简体中文',state=['disabled','normal'][lang.get()],command=lambda:[shut(tos),lang.set(0),Chinese(),Tos()])
        b3=Button(tos,text=['赞助','Donate'][lang.get()],command=Pay)
        b4=Button(tos,textvar=accept,state='disabled',command=lambda:[shut(tos),accept.set('')])
        b1.grid(row=1,column=0,padx=4,pady=(10,0),sticky='e',ipady=1)
        b2.grid(row=1,column=2,padx=4,pady=(10,0),sticky='w',ipady=1)
        b3.grid(row=1,column=1,padx=4,pady=(10,0),sticky='we',ipady=1)
        b4.grid(row=2,column=1,padx=4,pady=10,sticky='we',ipady=1)
        tos.bind('<Escape>',lambda e:win.destroy())
        tos.protocol('WM_DELETE_WINDOW',win.destroy)
        center(tos)
        for i in range(5,0,-1):
            accept.set([f'接受({i})',f'Accept({i})'][lang.get()])
            tos.update()
            sleep(1)
        try:
            accept.set(['接受','Accept'][lang.get()])
            b4.config(state='normal')
        except:
            pass


    ####父窗口交互界面####


    win=Tk()
    win.attributes('-alpha',0.0)
    win.title('Batch Renamer (仅供非商业使用)')
    win.geometry('720x540')
    win.minsize(480,360)
    win.rowconfigure(1,weight=1)
    win.rowconfigure(2,weight=1)
    win.rowconfigure(3,weight=1)
    win.columnconfigure(1,weight=1)
    win.columnconfigure(3,weight=1)

    blackfile=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAA6SURBVDhPYxj+IAWKyQbzgXg9hEkeoL8BIP+CNMHwbShGFsMbJhQbgA5AGoZYIKIDkH9J8vOQAwwMADvGFdWcs61nAAAAAElFTkSuQmCC')
    blackdir=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABkSURBVDhPYxhUwAGIE5CwBxATDYqA+D8WXA/ERIH5QIzNAFz4ORCDXAwHIAMOAzGyF/BhkNrZQAwHIAPWQ5hEAQz1owZQwYASIMYW3/gwSiJjAWJQ0sUW59iwDxCD9Aw4YGAAACxjO7tVch09AAAAAElFTkSuQmCC')
    blackdel=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAeSURBVDhPYxgFwxGkAPF8AhikBieg2IBRMAQBAwMAUCkLgdvfSuYAAAAASUVORK5CYII=')
    blackclear=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABrSURBVDhPYxh+gAeIIyBMrAAkB1KDE4AU/AfiAjAPFYDEQHL4LAADmEJkQ7CJ4QXIGkjWDAMwjWRpBoEyIP4OxCAD6kECpABkZyOziQLYNBBtSAIQ41IIMwSkBieQAGJ8CkByIDXDBzAwAADUXR2m3A2NowAAAABJRU5ErkJggg==')
    blackexit=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADPSURBVDhPzZCtEoFBFIa/IAqiCxBE0QW4AJcgiIILMONCBEEUBEEUBFEUBEEURcX77Ms3dmf9NJ6ZZ+bdnbNnd0/x90zlwvE7qrLhGKABPmjKmmMeineOgbTBVr58UVdeZSesTNqgJS+yF1YJFK4dS9IGMJNzx5ijHDuW5BoM5Mkxhs2RY0n/7jM0ODvGMJyl41t40coxhpsYYjus8jBEaoZhlYEhHiSFKezt5UZW2MhRlzThlonkv8iz2eMwNR/hEPNgWMifefbLm39FUdwAXeMqFq9yfDUAAAAASUVORK5CYII=')
    blackundo=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACQSURBVDhPYxgFcMADpckGk4HYBsIEAwEg9gHiCiCeDsQFQGwBxDjBfCD+DMQgQyKA+DEQ/8eC9wOxCRBjAJABIAW/ofRzIM4AYh0g5oDS9UD8HohhFqEAmAEwQ0DOxwY0gBhkOMgQFZAADCAbAMJYbYECkBdAakB64CAFiEECyBgUsLhiBxS4oLAaBZQDBgYAemIkwFdkk1AAAAAASUVORK5CYII=')
    blackredo=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACQSURBVDhPYxgFFAEWKI0VmABxDhBPBuIKIA4AYgEghgENIG6HMFEBSON+IP6PBb8G4gQgBml+DsTzgRgF2ADxZyD+DsTNQKwDxBxQOgOIHwMxyKDfUBrFAAkgBmkGmQyyARsAuQ6mGcOAfiAGCYIUYQMwZ8M0YxgACqQSCBMDgEIbFGAgDcg4BYhHAeWAgQEApikkFHJ5aooAAAAASUVORK5CYII=')
    blackdec=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACASURBVDhPYyAAbKCYbDAfiNdDmKQBAyBOAOLDUAxig8SIBppAvAqI/0MxyBUkGQACPEAMcwGITRYAaSRacwAQw5xMCIPCBAOoADFIghgMUosBBt4F2EABFJMFqoH4DxCDnFwPEiAFaAAxKBnfhmIQGyRGMiA7L8BAChTTCjAwAAAWszBeJIbQFwAAAABJRU5ErkJggg==')
    blackinc=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABkSURBVDhPY6AmsAHi+URikFoMQLEB2ABIIdGK0QFI42coJtmQACA+D8T/ofgKEIcBMckA5N/1ECZ5YAgbAArEi0AMC8TrQBwBxCQBiqIRBkAaidYMUgjyMzEYq6EUG0AGYGAAAJICLjL9BvlmAAAAAElFTkSuQmCC')
    blacktips=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAETSURBVDhPtZItEoFRFIZvEAQLEARBECzBIgRBFARBFM0IoiBYgIVYgCCIggUIgiAIAu9zf8z5fozCM/PM3J/vnnvOuZ/7Fw3Zl8so46b8SkXO5SO6j97jnGBVWQqHd/ImJ9J+yN5QXuVBlgbhZg63/cy5qbxEZywIyiAImWSgZlLkZujJp1zLlWRvIIFMmKeLPDSJxZQaHy/C0LOVmzD0kMUoDAOkRLPK4CYOjP0sQECye/MpQEueJWVYCgEogaei2xYaewrDDPmMfHfpAQ2ydKMWLqPBHT8zUAaReZEEjbPNq0ueNZN+ghfgJ+EDbsnDGntHWWOhDIKQCeWQDc1Cxum/+HjYQn28MweQhhVq/gHOvQC/Pz/NSOdzRQAAAABJRU5ErkJggg==')
    blackpay=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACrSURBVDhPzdKhDUIxFEbhSgQCwQCMgGCAJ5EIxkAi2ASBQDyBRDAEAyCQCAQCgUAgEHBOa3CvfSSEP/mStqK9t23460zwwjbOCtPBEm6wRx/Z6eGCO3Y44YYRsjLHA4M4SzmiTsPmLGDp4zhrkS7s200OmMG2imPPK1xhS1O0iqd7B1aTlTV8hc+yXTunYXOG8NksfQM/0hO+TnY83VO9SMuvUJyvvvKvEsIbWCUiZcz4NEoAAAAASUVORK5CYII=')
    blackabout=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEBSURBVDhPtZIhDgIxEEVXIBBYEgQCieAIHANLgkAQwh1wGCQH4AjgCRqBQCK4AAkCgUAg4L92NrRNCQZe8pK2205nplv8i6bsybnJuCW/UpFT+TD35t3mBKvKLBzeyZucyHAj3wbyKg8yG4SbOdx2M0/XLKEMgpBJBDWTIjeHLM0QMmFveJFrEosf60sgi6EfekiJZqWwKdpobOTCDz0zufXDCNJf+WHEWkYB+vIs6272JheAMk9y7GYG3aUHNCgk10T69ZQdNwugDzSHFylJn7EhLzJKv4TU+EnYwC0prPHtKGss5CAImVAO2dBtZEza3PzxcAj18XwcwJGt/ZqieAHiljeYAUSY1gAAAABJRU5ErkJggg==')
    blackto=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACVSURBVEhL7dQhDIJQEIfx1812MmY7mU4n2810O5lOJ9PJdLrZDt8Ftivc3gtXkG/7pf92boqEq/+sxaoMyCBZW3Q5RuhDH0jWllSFL/YjP9SQrC2pBvsRMeEJydqiu6OHPtThBmtLqsAMfegNydqSekEfWVBCsrboXD/A9Sty/5FdH1PXP9oDR68Da4vO/WV3dapC2AB/f31/GO0TRwAAAABJRU5ErkJggg==')
    blacktop=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABGSURBVEhLYxgF5ID/FGKCAJsmUvAIB/1AXABhUh/UAzEsnEFsqgJkw6luCTbDYZjqPoEZTDMwagFBMGoBQTBqwShABwwMAGm7Q7p9WvppAAAAAElFTkSuQmCC')
    blackup=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACHSURBVEhL7ZHBCYAwDEU7ksO4hRc3cAT37MUBPGg+JvAplVIbQbAPPg3S5tU0/I5VMl+lP4vk0KB2hZu7SzAWNNx15bp5XNx81BpB3SxJmwMTgCaJzXyT8GEWgEkSJfhW9Sa4Pd/cSAXA/gRnqhh0ZXICkNv7iDuBG11QpAuKdEGR1wVfI4QTTDlEyV25Tu0AAAAASUVORK5CYII=')
    blackflip=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABnSURBVEhLYxgF1AD9QFwAYVIf1APxfygGsakKkA2nuiXYDIdhqvsEZjDNwPC1gGoWj1pANhi1AANwAHE7EMMMRscgOZAaigAbELcCMbrhIDGQHNUAqI6AGQ5i0wSADKaZ4SMGMDAAAD3LPDZ3XQ/AAAAAAElFTkSuQmCC')
    blackdown=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACPSURBVEhL7ZHBCYAwDEU7jCO5gRePbuAI7ujFITxovvRjKNVYiCDYBx9pSfPSGn7HFvMaVWBSBSZVYOIqaOJXcyXI1d4ySFZJe6xOcgLUoBZnHjNK0GiR9NiIpIJOMkuwhzNFTBIc1DfRAk6OddH0mlRCgUtzoiUUuDUn/Cc6xW9uwZsgbpOnQPJa8y8Swg4CtERUpQgj4QAAAABJRU5ErkJggg==')
    blackbtom=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABOSURBVEhLYxgF1Ab/oZhmYNQCgmDUAoJg1AKsoB6IYQajY5AcVQA2S6hmOAz0AzHM8AKQAC0AyBKaGT50AHJEkoMJAmyaSMGjgBTAwAAA4AlDuxrN7o4AAAAASUVORK5CYII=')
    blackgit=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJ1SURBVDhPjVS/axRBFN4zOUUiaISwyc7sm903kxRX2BxoYSf+GYompZUWadVgYZcEGxtbCTGJINgI1pLCH52KhUmloJUYkDTq92Zm93bNxdwHw83tfO97P+a9SYagk1mbZ8YtZGS3FNndjHhflt8bu5mZckE4wg0mhyBNz00IWRG/8wLG/hm2gjg4hufTNJ2I5m1orc/C+6oyvDdMZPjin8hiRWyjTICPjOxqnRqIMPh9UKBeOOO9ii+izUg7Ps0ggnTs04zKy0JCSp9Rt4/Yb8NwG/sPWDv4/kA42K8FB4jU8HXRSqS4Uo/KOwxvi5d+v9/Nc2e1nlXMfFqW7LW2rtfrHRcOuIshWtgSv1XK6STc5uACEM1972kEiPNKUDR8lBDYqsQQ+nd4uhT5R2KG+CLS/lrZ41I3EnzYHQjal1NTvVORfyRwuych8ry2h5aE3Uz3MXhjgT4SjiHNRwN73m8JIuVnzrkTkTwC+l2UaL0l2EqZ+L2/qRFhjJludgi0dnDLdrP6EKJ1t9Az3WjzP4yjQ26gTL9qQcNPIIhBFyHiHxItHHzB/8XpojBVvzUh33zvGr4JscENQyO0TRYb24vxPH7XvFeZEEwEEU1GrWQSzQ3DZSlNyKaKzEf3RhpfeBg9CMnoEb+S3sL/DYh+AvEezseFFDEGRw/bQliE0Sv4Gs7DQMhgQ2AFovLSLBHNlVlZzqHoZzyhgZm8vNsU86ki6gPPmH++yEo630B8DfEXGmMZj2uo3DYE5fni5WZZWvCRorBSj1ijpXhUQxfujj/DYyDcQx/YBjrSi4rcFVXMXojfauiyPI86XlXO9+s/j0iS/AWTZgVeiOBmqAAAAABJRU5ErkJggg==')
    pay2=PhotoImage(data='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')
    pay5=PhotoImage(data='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')
    pay10=PhotoImage(data='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')
    payany=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAYdEVYdFNvZnR3YXJlAEFuZHJvaWQgR2FsbGVyeWpzpOoAABjwSURBVHhexZwDtBxZ14Z7MrZt2zaTsW3btm3bk7FtJGNmbCODzCRjo7485/bT3+l9q/r2/Sb/+t+19uo6KO06tV1de+ihh4rrr7++uPHGG9uia6+9tnj88ceLHG+88UZx6aWXFu+99169pzWuvvrqonfv3vVWUVx22WXFbbfdVm914KuvvkrHfPrpp1P7nXfeKa666qp0Dfx+9NFHqf/RRx9N87777rvUboW///47zb3zzjvrPR3o379/ceWVV3a611Z0xRVXFP/8809Rm2qqqYpardYtWmKJJeqn7sBuu+2W+o8++uh6T2t4HMH2MMMMU2914J577kn9a6yxRmqffPLJjf2gCy64IPUvtthiqf3ss8+mdldg7tBDD11vdYAFlB+7Xfrxxx+L2lxzzZUae++9d7HvvvsW++yzTykdcMABxUYbbZTmrrTSSvVTd+CBBx4ottpqq+KJJ56o93SAVbbffvsVgwYNqvd0wAsQbI800kjFGWecUVx44YWpjzeD/jnmmCMxa8UVV0ztxRdfvDjooIOKww8/vDjrrLOKaaedNvX369cv7XfmmWemc7Lachx88MHFsccemx72McccU+/twK233pqOMdtssxWHHnpo6f1LRxxxRDHGGGOk+b/88st/GdgOXnvttTQ3MrAKs88+e5r/2Wef1Xs6QF9+TtvQlFNOmfqeeeaZpn7p+OOPT+MbbrhhU78r0Pbvv/+e2sL+MsjAHXfcsd7TGtNPP32a38RAn9jWW29d7LrrrulJQTvttFN62gB5xNzIwPvuu6/Ydttt03z2f/HFF1P/wgsvnOZvttlmaYX++uuvqR8mHHXUUWkb8OofeeSRae5YY42VVsGaa66Z2nPOOWdx/vnnF6ecckpaOTJqk002SePbbLNNOh4yE5x77rlpf+RTDuYON9xwaXvgwIHFxhtvnI4JZCDXCPL7kbbccsvi/fffT+NTTz11ml/KQLYjjT322GmsioGcIJ9/xx13pH6PLX377bepvww//fRT01wJBpVBBvbp06fe0xoe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')

    whitefile=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABFSURBVDhPYxjm4MOHDykgDOWSDj5+/DgfaMB6KJd0QH8DQP4FaYJhIP82CKOJ4Q4Tig1AB1ANQykQ0QHIvyT5eSgCBgYAkmd7S2bMRNYAAAAASUVORK5CYII=')
    whitedir=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB8SURBVDhPYxg84P379w5AnADDb9++9YBKEQZADUUfPnz4j44/fvxYD1WCHwAVzsdmAB78HORiqHaIAUB8GNkL+DBILdCQ2VDtcBesh3IJAgz1owZQwQAgpwSIscU3Tgw0BJHI/v//zwJKutjiHBt+9+6dD0gPVPuAAgYGABn6PrQWgTn4AAAAAElFTkSuQmCC')
    whitedel=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAlSURBVDhPYxgFww58+PAh5ePHj/PxYZAaqHJMQLEBo2BoAgYGABaeQ/ELZIGmAAAAAElFTkSuQmCC')
    whiteclear=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB9SURBVDhP3ZI7EoAgEEM5gAfwaJYcwcrW+1LwqSyVOMHZGXAHLXkVm00CBWYwnHOT937hWIEdPBxrYIgxniGEldIDNOy0C26KUZa0NBUZ+BwulOCvMMjBLaV0sGCn3Id8tjxzrdMKdJdkg30zihJLqSZ/klkzYAcPxzEw5gLSM6841z7d7gAAAABJRU5ErkJggg==')
    whiteexit=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADzSURBVDhPzZItDsJAFIRXIBFIDoBAIjkAB+AICCSCA5BwEAQCiaioqKxAIJEIBKKu/w1yRZm3mbApywYJX/LSzLxfaNV/0zTNvq7rgPI7aZr20TSiNAMkKFWe5+OqqgaULtx4oXQGIHf2XoTJcyQ1YkbLGYCaCfIPPBe0LNweUxreBwjQB9QdKS0w70huKQ2fBpRluUJtQmkRE6dtKA3wlhKUBg7IKC0wA2wLKb3IRaiNKC3cpouimNJy4J+o8VzT6oJkjLhJIa0XbL7iglPbtj3aXfAhDTlEXudOfq8Ez9bSLDUs98OmEE0ZI5KzvZt/iFJP5qv6SxO4iucAAAAASUVORK5CYII=')
    whiteundo=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACzSURBVDhPYxgFEPDq1SseKJM88PHjx8nv3r2zgXIZ3r9/LwDk+wBxxYcPH6YD+QVv3761gEpjAqAB84EKP4MMAeIIIPsxEP/HgvcDsQlUGwJADQAp+A2lnwMNygBinfv373OAaKCaeqD4eyAGWwTVCgFIBoANASrwgUqhgDdv3mgA5Z+DDAHqUYEKYxgAwpi2QAFQzgSkBqQHKgQWTAEJoOHJuGIHaHgFEEdAuaOAMsDAAAD/cs+3N78UrwAAAABJRU5ErkJggg==')
    whiteredo=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAC4SURBVDhPYxgF5IP///+zQJmY4MOHDybv3r3L+fjx42QgXfH+/fsAIBaASjO8efNGA6imHcpFAJBGIN4PxP+x4NdAQxKgmp8DDZ8P1QYBQJtsgBKfgfg7ULIZyNe5f/8+B4gG4gyg+GMgBhn0G0SjGPDq1SsJoCBI83OQDVBhFACUA7kOrBmEUQwAcvqhEiZQIRQAczZMMwijGAAKJKBgCZSLAkChDZRrB2lAxkCxFKiSUUAZYGAAANqaz3pPtRKeAAAAAElFTkSuQmCC')
    whitedec=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACwSURBVDhPY8AH3r17ZwPCUC7p4OPHj/M/fPiwHsolHrx//94AiBOABhwGYRAbJAaVJgw+f/6sCbR5FRD/h+L1JBkAAq9eveKBuQDEhgqTBkAaidYMdGIAkpPxYlCYQLUhANCpKtDAIohBaqHaEAAoMcAuwAaAigtAGMolDQCdWg3Ef0BOBtpYDxUmDrx580YDqAmUjG+DMIgNEoNKEw+ghpCeF2AAqDkFhKFcWgAGBgADgyG0mNykkgAAAABJRU5ErkJggg==')
    whiteinc=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB9SURBVDhPY6AaePfunc3Hjx/nE4NBaqHaEIBiA7ABkEKiFaMDkMYPHz58BmGSDXn//n0AUON5IP4PwkBnXwHSYVBp4gHIv0CN66Fc0sEQNuDTp0+gQLwIxOBABOLrwJiIgEoTByiKRhgAaSRaM0ghyM/EYKyGUmwAeYCBAQBu6g9lwUy4gwAAAABJRU5ErkJggg==')
    whitetips=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFFSURBVDhPtZItUsNQFIUjEAgWgEAgEAiWwCIQEUhEBQKJZAaBjEB0AV1IF4CoqERURDKT5ncqKiLC+R4nmWZoHJyZM5Nz7s+7971E/4KiKC7quo7FxIyrqrp0eBpd1500TfOqgtZcmXvrJE3TU6ePQbESPsRdWZZPh4nENMGDYpW4PtrEJ+/yPL9G6/tZ3EIVv+CxhjRNEvQA79xyMlqJd9Kdms7Fd8fuHWOStj8oQAYX1vajkazCtxAUFFtKLyzRTDGzDAY3vbIcgZMoUNNHW33DueV0AyVdyf9iDVsBxxqwwp7bthWgJC52YzlA3mii/nZbLshWgJJuoWWAD+vk39j6gUzWqHgRW0ywgJZRlmXnytmOxu/BCyi4JkGMbQ/Ac+xTjc5sj+EmTMJvy1MtTb7DfzFZfAj2U8GMAsiF/dr5bxBF36dEipxUi/t4AAAAAElFTkSuQmCC')
    whitepay=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADRSURBVDhPzZItEoJAHEeJBoPBA3gEAwcwGg0ew2jwJgaDwWAkeAgOQCBuMDCDAwsYCAZ8O/MLpgUMjm/mDbP/r10Wgv/FWrupqqrDSKHhGGMmNB41IG6aZq5UP+w8oynDZ13XN54GLYYq8UPhHlsGLRRysZRhFy39lGV5oKErimKt0DjyPJ8yIHZDMGHgzr2W0sOhOcQTPrDFrVLj0KWmmCjkh8s6U5x9Hluxu5Z+aFxS7D6bO/oVI3zhXiX9uN21q7vIlPVKqeHQ9P2v/EOC4A31UsJSEAyoLAAAAABJRU5ErkJggg==')
    whiteabout=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAE5SURBVDhPtVKhUsNAFDyBQNQyg0AgEf0EPiOWGUQFw/QfcDWRfACfAL6DRlRUIipimTTJJXOi4sSxe12uCW0c7MzOZPfee/feu5h/QV3XV23bZmAuZtbaax2PI4Rw1nXdExK8uBJ30nlRFOcKH4LJCPgAXdM0834gz9DBPc4suD5ZRDe7qqpuZBkUuiUlDcdQkVzWHprZ82ZZESj6QkpGqBPfv8jA4ML86Hy/gFh2MZOMBje9kkxg0CBQgLdEZ8+S0ViA75IJbB/+q2QCxngDDwUQeAd+OecuZEWcKsAx4W1w9igrbddzQbIiWICUjEAc9xWw8KmsPWByD5YvIuvoGcuyvETMFkUP7f9Ara0ZAGayE+jp7BOFJrKHUBF2wt+WT7UU+R1482hyH5wPCTMmkNAPRzP/DYz5Bg2mYzVNYlU3AAAAAElFTkSuQmCC')
    whiteto=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACrSURBVEhLYxgFIxB8+PBhKhD/R8Jb379/r0BIjmjw+fNnLaDG/WgGdRGSIwkANYUC8SskQ74AXZpASI4k8PHjx3okQ0D4FFDMlJAc0QAYHKJAjauQDQIaMv/Fixfc+OSg2okDQK87ADVeQTYIiEsJyZEEgIZkoRlyHyjmRUiOaEBTC2gaRDSPZKAG2iVToAbaZbS3b99qAzVhLQ7wyRENgBpoW9iNguEGGBgAGeJhRYYvhogAAAAASUVORK5CYII=')
    whitetop=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABYSURBVEhLYxgFJIMPHz78pwRDjcENsGkiBUONGang48eP/e/fvy+AcqkLgIbXw8IZxIYKUwcgG051S7AZDsNU9wnMYCiX+mDUAoJg1AKCYNSCUYAFMDAAAAu6DlvQ3x4NAAAAAElFTkSuQmCC')
    whiteup=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACbSURBVEhL7ZDBCYAwDEU7ksO4hRc3cAT39NL27KHml28tpVLRCoJ9EEhC8n+I+hfW2llrPbKsi4hPxhiHQM52HWLx6iZ4C0XXyMDnj9+ViPfMEcifmaTi6LF2zO+bRD+X3WOZPW8AZG6QekEPO2yX4fXh8h0IIVh6MINZ7LB1Dbm8YxrIGYDc7C3ODKrRDIo0gyLNoMjrBh9EqQ2vTDEq+AH1IgAAAABJRU5ErkJggg==')
    whiteflip=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB6SURBVEhL7ZQxCsAgDEWdSo/bG3SSjh5VPUGaDwmU1kl/l9YHARPD+7gYJsPUWlPOebOWi8r3UoqgcLYxh6ucHtKSe9Ff4mJr+Xw3gBY8A7qZAQ9EZFXh4eJGHdix9T5UsKgo3sSoiDtbG0c/vORynG3MBeLX5H8ihBOc/AeX6swc8AAAAABJRU5ErkJggg==')
    whitedown=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACmSURBVEhLYxhZ4MOHD/9BGMqlPhi1gCAYtYAgGLWAIKCqBR8/flSBMuEAlwXY1OIF79+/LwAa9BuIQ6BCYIDNApAakFqQHqgQYQB0UT3UsOfv3r3LgApjWABkJwMNfgQSA+mBChMHgBr6oQbCfQLlgy0AiUHl/pPkemSAbgmUDcKUGw4DaJbALKCO4TCAFCdwTHKYEwJIPqGey9EByBKaGT5IAQMDAPVzMKa/pLF4AAAAAElFTkSuQmCC')
    whitebtom=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABfSURBVEhLYxgFVAUfPnz4D8JQLvXBqAUEwagFBMGoBVjBx48f62EGo2OQHFQZZQCbJVQzHAaABvbDDH///n0BVJi6AGQJzQwfOgA5IsnBUGNwA2yaSMFQY0YBsYCBAQCBPg5WHV50twAAAABJRU5ErkJggg==')
    whitegit=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI3SURBVDhPjZRBSFRRFIZnsFBjoCzFRbSzRWTLDCEUQQzJQhSmbYvCCFyUYi0SShBdhuhOSHAsjBJxI2Ii5iJqFUFFm1Ah0hS0MaWyZvz++868fMyM0w8f595z/nPmvTt3JpRJyWTyUCKRqIA2iMELmIZhuA1nodDs2cWgPIyV8AS+wV9yASlntcdwjlSetQdFMR9aYAkSXnt2yYMW4Rrk2xhP1A+SbCVuyCW5rn2ERU8qrcNNUgdsnHu6Olg24yzhLnEetiEOK8YmbMEcdMBL6/lKqE0NOwo6dCcNgzAUs22AajhjaK3cMXmIncTU60+xLNLAJtjaU+h0n/QfwvtAfRLrH3BZyUfgzoyg12s2f07hjcKm9UqDSn5UQmI9Rzhs/pzCe4SeedeMWH/QQPe6piHIfK8ySF76h10n0iwN3LG9EiOEf19/DslLz6hrRpqlgSu2V+IVocj8OYVfN+S11+36l5Wcsb0S3+ESy7D1ZJU80Ig/rl6J9bQG3gHd+l+gi/yWWi0UWG+a8BTCBXgHqRvyB9pVLIcF+AS34A3ox/8MruON2Bw9VYTcDRiDNfB/oiw/wyl3sHCfzU94DhfhPeiiDoL/w8dXAE8hIDy/4R5L7wtlUwoToPO4SjwNNXDcGfaIXI+bYmKv4xqHErN4InESpuALxPD2Euut7ItctzfKDduBSSizclAUTkAfrILUZSVf5Lq9kjvnh5D2FgFh0B9tFQxA1NK+yF2Bfh7wPDH4xxoKhXYBsby39hrye/cAAAAASUVORK5CYII=')
    icon=PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAC9SURBVFhHYxgFo2AkgPlQnALm4QEqQJxAJQwyCwZAlt+G0nhBABD/pxIGOQIZgCxfD2HiBgPuAFpFAQiAHEAwCmgJQAmQYCIcBbQCsPgnmA5oWQ6A8H0gfg4SwAVAGrFlKXIwyCxk4AHE34HYBszDAWjlAAMg/gzEMWAeHkCrKAAFOwgTTAO0AjCLB8wBo4DoKKB1OXAYiEE5BCcAaUTPTuRikFnIAFQRDX4HDHgU0ArAHADDo2AUDCbAwAAAjDm/yGLJQU4AAAAASUVORK5CYII=')

    p=IntVar()  #备份列表的全局指针
    theme=IntVar()  #主题切换的全局指针
    theme.set(0)
    layout=IntVar()     #布局选择的全局指针
    layout.set(0)
    lang=IntVar()   #语言选择
    lang.set(0)
    spacing=IntVar()    #行号选择
    spacing.set(2)
    itemtype=StringVar()    #文件/文件夹状态
    status=StringVar()
    status.set('就绪')
    style=Style()
    style.theme_use('vista')
    rgb=win.winfo_rgb('SystemButtonFace')
    fit=bool((rgb[0]*0.299+rgb[1]*0.587+rgb[2]*0.114)>38400)
    win.iconphoto(1,icon)
    topwin=win.winfo_toplevel()
    menubar=Menu(topwin)
    topwin.config(menu=menubar)

    menufile=Menu(menubar,tearoff=0,fg='SystemButtonText',bg='SystemButtonFace')
    menuedit=Menu(menubar,tearoff=0,fg='SystemButtonText',bg='SystemButtonFace')
    menurule=Menu(menubar,tearoff=0,fg='SystemButtonText',bg='SystemButtonFace')
    menuview=Menu(menubar,tearoff=0,fg='SystemButtonText',bg='SystemButtonFace',selectcolor='SystemButtonText')
    menulang=Menu(menubar,tearoff=0,fg='SystemButtonText',bg='SystemButtonFace',selectcolor='SystemButtonText')
    menuhelp=Menu(menubar,tearoff=0,fg='SystemButtonText',bg='SystemButtonFace')

    menubar.add_cascade(label='文件(F)',underline=3,menu=menufile)
    menubar.add_cascade(label='编辑(E)',underline=3,menu=menuedit)
    menubar.add_cascade(label='规则(R)',underline=3,menu=menurule)
    menubar.add_cascade(label='查看(V)',underline=3,menu=menuview)
    menubar.add_cascade(label='语言(L)',underline=3,menu=menulang)
    menubar.add_cascade(label='帮助(H)',underline=3,menu=menuhelp)

    menufile.add_command(label='添加文件(F)',underline=5,acc='Ctrl+F',compound='left',command=openfile)
    menufile.add_command(label='添加文件夹(D)',underline=6,acc='Ctrl+D',compound='left',command=opendir)
    menufile.add_separator()
    menufile.add_command(label='移除所选(S)',underline=5,acc='Delete',compound='left',state='disabled',command=remove)
    menufile.add_command(label='移除全部(R)',underline=5,acc='Ctrl+R',compound='left',state='disabled',command=clear)
    menufile.add_separator()
    menufile.add_command(label='退出(X)',underline=3,acc='Alt+F4',compound='left',command=lambda:[Pay(),win.destroy()])

    menuedit.add_command(label='撤销(U)',underline=3,acc='Ctrl+Z',compound='left',state='disabled',command=undo)
    menuedit.add_command(label='重做(R)',underline=3,acc='Ctrl+Y',compound='left',state='disabled',command=redo)
    menuedit.add_separator()
    menuedit.add_command(label='全部选择(A)',underline=5,acc='Ctrl+A',state='disabled',command=selectall)
    menuedit.add_command(label='全部取消(N)',underline=5,acc='Ctrl+N',state='disabled',command=selectnone)
    menuedit.add_command(label='反向选择(I)',underline=5,acc='Ctrl+I',state='disabled',command=invertselect)

    menurule.add_command(label='插入(I)',underline=3,acc='F3',state='disabled',command=Insert)
    menurule.add_command(label='替换(R)',underline=3,acc='F4',state='disabled',command=Replace)
    menurule.add_command(label='删除(D)',underline=3,acc='F5',state='disabled',command=Delete)
    menurule.add_command(label='擦除(E)',underline=3,acc='F6',state='disabled',command=Erase)
    menurule.add_command(label='编号(S)',underline=3,acc='F7',state='disabled',command=Serialize)
    menurule.add_command(label='大小写(C)',underline=4,acc='F8',state='disabled',command=Case)
    menurule.add_command(label='扩展名(X)',underline=4,acc='F9',state='disabled',command=Extension)
    menurule.add_command(label='手动修改(M)',underline=5,acc='F2',state='disabled',command=Edit)

    menuview.add_radiobutton(label='系统主题',var=theme,value=0,command=systemtheme)
    menuview.add_radiobutton(label='经典主题',var=theme,value=1,command=classictheme)
    menuview.add_radiobutton(label='暗黑主题',var=theme,value=2,command=darktheme)
    menuview.add_separator()
    menuview.add_radiobutton(label='紧凑布局',var=layout,value=0,command=tightlayout)
    menuview.add_radiobutton(label='宽松布局',var=layout,value=1,command=looselayout)
    menuview.add_separator()
    menuview.add_command(label='减少行号间距',compound='left',command=decspacing)
    menuview.add_command(label='增加行号间距',compound='left',command=incspacing)

    menulang.add_radiobutton(label='简体中文',var=lang,value=0,command=Chinese)
    menulang.add_radiobutton(label='English',var=lang,value=1,command=English)
    menuhelp.add_command(label='快速上手(Q)',underline=5,acc='F1',compound='left',command=Tips)
    menuhelp.add_separator()
    menuhelp.add_command(label='赞助作者(D)',underline=5,compound='left',command=Pay)
    menuhelp.add_command(label='关于(A)',underline=3,compound='left',command=About)

    to=Label(win)
    llbl=Label(win,text='当前名称')
    rlbl=Label(win,text='新名称')
    line=Listbox(win,width=3,justify='right',highlightthickness=0,state='disabled',yscrollcommand=dscroll)
    lbox=Listbox(win,exportselection=0,highlightthickness=0,selectmode='extended',yscrollcommand=lscroll)
    rbox=Listbox(win,exportselection=0,highlightthickness=0,selectmode='extended',yscrollcommand=rscroll)
    scrollbar=Scrollbar(win,orient='vertical',command=scroll)
    top=Button(win,command=move2top)
    up=Button(win,command=moveup)
    flip=Button(win,command=reverse)
    down=Button(win,command=movedown)
    btom=Button(win,command=move2btom)
    see=Button(win,text='检查新名称',command=checknow)
    do=Button(win,text='批量重命名',width=30,command=renamenow)
    statusbar=Label(win,textvar=status,relief='solid')
    seticon()

    to.grid(row=0,column=2)
    llbl.grid(row=0,column=1,pady=4)
    rlbl.grid(row=0,column=3,pady=4)
    line.grid(row=1,column=0,rowspan=3,sticky='ns')
    lbox.grid(row=1,column=1,rowspan=3,sticky='nsew')
    rbox.grid(row=1,column=3,rowspan=3,sticky='nsew')
    scrollbar.grid(row=1,column=4,rowspan=3,sticky='ns')
    top.grid(row=1,column=2,sticky='n')
    up.grid(row=1,column=2,sticky='s')
    flip.grid(row=2,column=2)
    down.grid(row=3,column=2,sticky='n')
    btom.grid(row=3,column=2,sticky='s')
    see.grid(row=4,column=3,pady=10,ipady=1,sticky='e')
    do.grid(row=4,column=0,columnspan=5,ipady=1,pady=10)
    statusbar.grid(row=5,column=0,columnspan=5,sticky='ew')
    center(win)

    lbox.bind('<<ListboxSelect>>',lambda e:lselect())
    rbox.bind('<<ListboxSelect>>',lambda e:rselect())
    top.bind('<Enter>',lambda e:status.set(['上移所选项目至顶 (2)','Move selected to top (2)'][lang.get()]))
    up.bind('<Enter>',lambda e:status.set(['上移所选项目 (W)','Move up selected (W)'][lang.get()]))
    flip.bind('<Enter>',lambda e:status.set(['逆序全部项目 (F)','Reverse all (R)'][lang.get()]))
    down.bind('<Enter>',lambda e:status.set(['下移所选项目 (S)','Move down selected (S)'][lang.get()]))
    btom.bind('<Enter>',lambda e:status.set(['下移所选项目至底 (X)','Move selected to bottom (X)'][lang.get()]))
    see.bind('<Enter>',lambda e:status.set(['检查新名称是否可用 (F11)','Check if new names are available (F11)'][lang.get()]))
    do.bind('<Enter>',lambda e:status.set(['应用全部更改 (F12)','Apply all changes (F12)'][lang.get()]))
    top.bind('<Leave>',lambda e:statustxt())
    up.bind('<Leave>',lambda e:statustxt())
    flip.bind('<Leave>',lambda e:statustxt())
    down.bind('<Leave>',lambda e:statustxt())
    btom.bind('<Leave>',lambda e:statustxt())
    see.bind('<Leave>',lambda e:statustxt())
    do.bind('<Leave>',lambda e:statustxt())

    win.bind('2',lambda e:move2top())
    win.bind('w',lambda e:moveup())
    win.bind('W',lambda e:moveup())
    win.bind('s',lambda e:movedown())
    win.bind('r',lambda e:reverse())
    win.bind('R',lambda e:reverse())
    win.bind('S',lambda e:movedown())
    win.bind('x',lambda e:move2btom())
    win.bind('X',lambda e:move2btom())
    win.bind('<F1>',lambda e:Tips())
    win.bind('<F11>',lambda e:checknow())
    win.bind('<F12>',lambda e:renamenow())
    win.bind('<Control-f>',lambda e:openfile())
    win.bind('<Control-F>',lambda e:openfile())
    win.bind('<Control-d>',lambda e:opendir())
    win.bind('<Control-D>',lambda e:opendir())
    win.protocol('WM_DELETE_WINDOW',lambda:[Pay(),win.destroy()])
    Tos()
    win.mainloop()



if __name__=='__main__':
    Renamer()
