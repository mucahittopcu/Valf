import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Vte
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GLib
from gi.repository import GObject
from pathlib import Path

HOME = "HOME"
SHELLS = [ "/bin/bash" ]

ICONSIZE = Gtk.IconSize.MENU
get_icon = lambda name: Gtk.Image.new_from_icon_name(name, ICONSIZE)

class MyWindow(Gtk.Window):
    notebook = Gtk.Notebook()
    home = str(Path.home())
    baglantilar = dict() # Goal 1
    __gsignals__ = {
        "close-tab": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, [GObject.TYPE_PYOBJECT]),
    }

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(750, 500)
        self.connect("destroy", Gtk.main_quit)
        self.main()
        self.number_list = [1]
         
    def main(self):
        self.table = Gtk.Table(n_rows=10, n_columns=30, homogeneous=True)
        self.add(self.table)

        self.listbox = Gtk.ListBox()
        self.add(self.listbox)
        self.listbox_add_items()

        new_window_button = Gtk.Button("Add New Host")
        new_window_button.connect('clicked',self.add_newhost_window)

        self.table.attach(new_window_button,5,10,9,10)
        self.table.attach(self.listbox,0,10,0,9)

        self.add(self.notebook)
        self.table.attach(self.notebook,10,30,0,10)

        self.notebook.show_all()
        self.listbox.show_all()
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label = "Host Attributes : "))
        self.notebook.append_page(self.page1, Gtk.Label("Attributes"))
        
    def read_config(self): # Conf dosyasını gezer, değerleri okur, dictionary'e atar.
        self.baglantilar.clear()
        with open(self.home+'/.ssh/config','r') as f:    
            for line in f: # Goal 2 
                if 'Host ' in line: # Goal 3
                    if line != '\n':
                        
                        (key,value) = line.split()
                        hostline = value
                        self.baglantilar[hostline] = dict() # Goal 3
                        self.baglantilar[hostline][key] = value # Goal 5

                    else:
                        continue
                    
                else: # Goal 4
                    if line != '\n':
                        (key,value) = line.split() 
                        self.baglantilar[hostline][key] = value
                
                    else:
                        continue

    def write_config(self): # RAM'de tutulan dictionary değerlerini dosyaya yazar.
        with open(self.home+'/.ssh/config','w') as f:
            for p_id, p_info in self.baglantilar.items():
                for key in p_info:
                    f.write(key+" "+p_info[key]+"\n")

                
    def context_menu(self): # Buton sağ tıkında açılan menü 
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("Create New Notebook")
        menu.append(menu_item)
        menu_item.connect("activate", self.on_click_popup)

        menu_item_del = Gtk.MenuItem("Delete Host Configuration")
        menu.append(menu_item_del)
        menu_item_del.connect("activate",self.on_click_delete)

        menu_item_connect = Gtk.MenuItem("Connect Host")
        menu.append(menu_item_connect)
        menu_item_connect.connect("activate",self.on_click_connect)

        menu.show_all()

        return menu

    ##  Buton sağ click ise context menu açtı
    def button_clicked(self,listbox_widget,event): 
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            menu = self.context_menu()
            ## Tıklanan objenin labelini print ediyor
            self.labelmenu = listbox_widget.get_label()
            menu.popup( None, None, None,None, event.button, event.get_time()) 
            return True               
                        
    def on_click_popup(self, action): ## Yeni sayfa oluştur
        
        self.new_page = Gtk.Box()
        self.new_page.set_border_width(10)

        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")

        self.close_button()
        self.new_page.add(Gtk.Label(label=self.labelmenu))
        self.notebook.append_page(self.new_page, self._button_box)

        self.number = self.notebook.page_num(self.new_page)
        self.number_list.append(self.number)
        self.number_list.pop()
        self.notebook.show_all()
    
    def on_click_delete(self,action): # # Seçilen bağlantıyı silme fonksiyonu   
        baglantilar_index = list(self.baglantilar.keys()).index(self.labelmenu)
        self.listbox.remove(self.listbox.get_row_at_index(baglantilar_index))  
        self.listbox.show_all()

        self.baglantilar.pop(self.labelmenu)
        self.write_config()               

    def add_newhost_window(self,widget): ## Yeni açılan pencere
        self.input_window = Gtk.Window()
        self.input_window.set_title("New Window")
        self.input_window.set_border_width(10)
        self.table2 = Gtk.Table(n_rows=7, n_columns=0, homogeneous=True)
        self.input_window.add(self.table2)

        self.host = Gtk.Entry()
        self.host_name = Gtk.Entry()
        self.user = Gtk.Entry()
        self.port = Gtk.Entry()
        self.submit_button = Gtk.Button("Gönder")
  
        self.host.set_placeholder_text("Host")
        self.host_name.set_placeholder_text("HostName")
        self.user.set_placeholder_text("User")

        self.input_window.add(self.host)
        self.input_window.add(self.host_name)
        self.input_window.add(self.user)
        self.input_window.add(self.port)
        self.input_window.add(self.submit_button)
        self.submit_button.connect('clicked',self.on_click_add_newhost)

        self.table2.attach(self.host,0,1,0,1)
        self.table2.attach(self.host_name,0,1,2,3)
        self.table2.attach(self.user,0,1,4,5)
        self.table2.attach(self.submit_button,0,1,6,7)

        self.input_window.present()
        self.input_window.show_all()  
        
    def listbox_add_items(self): # Listbox'a host isimlerini ekleyen fonksiyon
        
        self.baglantilar.clear()
        self.read_config()
        keys = self.baglantilar.keys()
        for row in self.listbox.get_children():
            self.listbox.remove(row)
        for i in keys:
            ## label yerine buton oluşturduk
            buttons = Gtk.Button.new_with_label(i)
            buttons.connect("button-press-event",self.button_clicked)
            buttons.connect("button-press-event",self.button_left_click)
            self.listbox.add(buttons) 
        self.listbox.show_all()
    
    def on_click_add_newhost(self,widget): ## Açılır penceredeki gönder butonu fonksiyonu
        self.read_config()
        new_host = self.host.get_text()
        new_hostname = self.host_name.get_text()
        new_user = self.user.get_text()
        default_port = '22'

        self.baglantilar[new_host] = {'Host' : new_host, 'Hostname' : new_hostname , 'User' : new_user, 'Port' : default_port}
        self.write_config()

        self.listbox_add_items()
        self.listbox.show_all()
        self.input_window.hide()

    def _close_cb(self, button): # Kapatma butonu görevi.
        self.notebook.remove_page(self.number_list[-1])
        self.notebook.show_all()
       
    def close_button(self): # Close butonu
        self._button_box = Gtk.HBox()
        self._button_box.get_style_context().add_class("right")
        self.label1 = Gtk.Label(label=self.labelmenu)

        self._close_btn = Gtk.Button()
        self._close_btn.get_style_context().add_class("titlebutton")
        self._close_btn.get_style_context().add_class("close")

        self._close_btn.add(get_icon("window-close-symbolic"))
        self._close_btn.connect("clicked", self._close_cb)
        
        self._close_btn.show_all()
        self.label1.show_all()
        
        self._button_box.pack_start(self.label1, False, False, 3)
        self._button_box.pack_start(self._close_btn, False, False, 3)
    
    def index_host(self,wanted_host):#indeksi istenilen hostun labelname atılmalı String
        self.read_config()
        self.wanted_host_index=int()
        
        baglanti_key=list(self.baglantilar.keys())
        for i in range(0,len(baglanti_key)):
            if(baglanti_key[i]==wanted_host):
                self.wanted_host_index=i

    def notebooks(self,labelname): # Attributes sayfası
        self.read_config()
        self.notebook_change_button = Gtk.Button("Change Configuration")
        self.notebook_change_button.connect('clicked',self.on_click_change)

        self.notebook.remove_page(0)
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.notebook.prepend_page(self.page1, Gtk.Label(labelname+" Attributes"))
        self.notebook.set_current_page(0)
        self.get_host_before = labelname

        grid = Gtk.Grid()
        self.page1.add(grid)
        self.label_dict={}
        self.entries_dict={}
        grid_count=2
        grid_count_2=2
        for p_id, p_info in self.baglantilar.items():
                for key in p_info:
                    if(p_info['Host']==labelname):
                        self.labeltemp = "left_label_"+str(key)
                        self.oldlabel = self.labeltemp
                        self.labeltemp = Gtk.Label(key) 
                        self.label_dict[self.oldlabel] = self.labeltemp

                        grid.attach(self.labeltemp,0,grid_count,2,1)
                        grid_count += 1
                    

                        self.temp = "right_entry_"+str(p_info[key])
                        self.oldname = self.temp
                        self.temp = Gtk.Entry()
                        self.entries_dict[self.oldname] = self.temp
                        self.temp.set_text(p_info[key])
                
                        grid.attach(self.temp,5,grid_count_2,2,1)
                        grid_count_2 += 1


        self.add_attribute_button = Gtk.Button("Add New Attribute")
        self.add_attribute_button.connect("clicked",self.add_attribute)
        grid.attach(self.notebook_change_button,0,20,2,1) # Change butonu    
        grid.attach(self.add_attribute_button,0,19,2,1)     
        self.notebook.show_all()
        self.listbox.show_all()
            
       
    
    def button_left_click(self,listbox_widget,event): # Buton sol click fonksiyonu
        self.notebooks(listbox_widget.get_label())

    def on_click_change(self,listbox_widget): # Change attribute butonu görevi
        self.values_list = list(self.entries_dict.values())
        self.labels_list = list(self.label_dict.values())
        self.updated_list=dict()
        for i in range(0,len(self.values_list)):
            self.updated_list[self.labels_list[i].get_text()]=self.values_list[i].get_text()
            
        self.index_host(self.get_host_before)
        self.baglantilar[self.get_host_before]=self.updated_list
        self.baglantilar[self.values_list[0].get_text()] = self.baglantilar[self.get_host_before]#index değişimi bakılmalı sona eklenen kendi indexsine eklenmeli normalde
        self.write_config()
        self.notebooks(self.values_list[0].get_text())
        self.listbox_add_items()


    def add_attribute(self,widget): # Yeni attribute penceresi
        self.add_attribute_window = Gtk.Window()
        self.add_attribute_window.set_title("Add Attribute")
        self.add_attribute_window.set_border_width(10)
        self.table3 = Gtk.Table(n_rows=5, n_columns=30, homogeneous=True)
        self.add_attribute_window.add(self.table3)

        self.attribute_name = Gtk.Entry()
        self.attribute_value = Gtk.Entry()
        self.add_attribute_submit_button = Gtk.Button("Add")
  
        self.attribute_name.set_placeholder_text("Attribute Name")
        self.attribute_value.set_placeholder_text("Value")

        self.add_attribute_window.add(self.attribute_name)
        self.add_attribute_window.add(self.attribute_value)

        self.add_attribute_window.add(self.add_attribute_submit_button)
        self.add_attribute_submit_button.connect('clicked',self.on_click_add_attribute)

        self.table3.attach(self.attribute_name,0,14,0,1)
        self.table3.attach(self.attribute_value,16,30,0,1)

        self.table3.attach(self.add_attribute_submit_button,10,20,2,3)

        self.add_attribute_window.present()
        self.add_attribute_window.show_all() 

    def on_click_add_attribute(self,widget): # Yeni attribute ekleme butonu görevi
        self.add_attribute_window.hide()
        self.read_config()
        self.baglantilar[self.get_host_before][self.attribute_name.get_text()] = self.attribute_value.get_text()
        self.write_config()
        self.notebooks(self.get_host_before)
        
    def on_click_connect(self,widget): # Sağ tık menüsündeki Connect Host seçeneği ile açılan pencere
        self.connect_window = Gtk.Window()
        self.connect_window.set_title("Connect")
        self.connect_window.set_border_width(10)
        self.table4 = Gtk.Table(n_rows=3, n_columns=2, homogeneous=True)
        self.connect_window.add(self.table4)

        self.connect_password = Gtk.Entry()
        self.connect_button = Gtk.Button("Connect")

        self.connect_password.set_placeholder_text("password")
        self.connect_password.set_visibility(False)
        self.connect_window.add(self.connect_password)

        self.connect_window.add(self.connect_button)
        self.connect_button.connect('clicked',self.on_click_check_password)

        self.table4.attach(self.connect_password,0,1,0,1)

        self.table4.attach(self.connect_button,0,1,2,3)

        self.connect_window.present()
        self.connect_window.show_all()
    
    def terminal_win(self):
        self.terminal_window = Gtk.Window()
        self.terminal_window.set_title("Terminal")
        self.terminal     = Vte.Terminal()
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ[HOME],
            SHELLS,
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,)
    
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.terminal_window.add(self.grid)

        self.grid.attach(self.terminal, 1,1,1,1)
        self.terminal_window.add(self.terminal)
        self.terminal_window.show_all()

    def wrong_password_win(self):
        self.wrong_pass_win = Gtk.Window()
        self.wrong_pass_win.set_title("Wrong")
        
        self.wrong_pass_label = Gtk.Label("Wrong pass ! Try Again.")
        self.table5 = Gtk.Table(n_rows=3, n_columns=3, homogeneous=True)
        self.wrong_pass_win.add(self.table5)

        self.table5.attach(self.wrong_pass_label,1,2,1,2)

        try_again_button = Gtk.Button("Try Again")
        try_again_button.connect("clicked",self.hide)

        self.table5.attach(try_again_button,1,2,2,3)
        self.wrong_pass_win.show_all()
    
    def hide(self,event):
        self.wrong_pass_win.hide()
    
    def on_click_check_password(self,event): # Password kontrolü
        password = self.connect_password.get_text()
        
        if condition:
            pass
            #self.terminal_win()
            
        else:
            #self.wrong_password_win()
            pass


            
window = MyWindow()
window.show_all()

Gtk.main()