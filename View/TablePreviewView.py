import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class TablePreviewView(Gtk.Window):
    def __init__(self, window = Gtk.Window):
        #Gtk.Window.__init__(parent)
        self.window = window
        #self.window.set_size_request(500, 600)
        self.window.set_border_width(10)
        self.tableListObj = None

    def render(self):

        #Rysujemy okno
        self.window.show()
        self.fixed = Gtk.Fixed()
        scroll = Gtk.ScrolledWindow()


        #Przycisk usuwania tabeli
        self.button_delete_table = Gtk.Button("Usuń tabele")
        self.button_delete_table.set_size_request(100, 20)
        self.button_delete_table.override_background_color(0, Gdk.RGBA(1, 0, 0, 1))
        self.button_delete_table.override_color(0, Gdk.RGBA(1, 1, 1, 1))
        self.fixed.put(self.button_delete_table, self.window.get_size()[0] - 40 - self.button_delete_table.get_size_request()[0], 10)

        #Przycisk powrotu
        self.button_back = Gtk.Button("<- Powrót")
        self.button_delete_table.set_size_request(100, 20)
        self.fixed.put(self.button_back, 10, 10)


        #Lista tabel
        #self.tableListView.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 200)

        #self.fixed.put(self.tableListView, 10, 70)
        scroll.add(self.tableListView)
        scroll.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 200)
        self.fixed.put(scroll, 10, 70)

        self.window.add(self.fixed)
        self.window.show_all()

    def tableListRender(self, objList):
        print(objList)
        colnames = objList[0]
        result = objList[1]

        if len(result) == 0:
            coltypes = [str] * len(colnames)
        else:
            coltypes = [type(result[0][0])]
            if type(result[0][0]) == type(None):
                coltypes = [str]

            for i in range(1, len(result[0])):
                temp = type(result[0][i])
                if temp == type(None):
                    temp = str
                coltypes = coltypes + [temp]

        print(coltypes)
        self.tableListObj = Gtk.ListStore(*coltypes)
        for row in result:
            self.tableListObj.append(row)


        self.tableListView = Gtk.TreeView(self.tableListObj)

        for i, col_title in enumerate(colnames):
            renderer = Gtk.CellRendererText()

            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            column.set_sort_column_id(i)

            self.tableListView.append_column(column)

    def deleteTableDialog(self):
        message = Gtk.Dialog("Napewno?", self.window, Gtk.DialogFlags.MODAL,
                             (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                              Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        message.set_default_size(300, 90)

        box = message.get_content_area()
        label = Gtk.Label("Czy na pewno chcesz usunąć tą tabelę?")
        box.pack_start(label, True, True, 0)
        message.add(box)
        message.show_all()
        answer = message.run()

        message.destroy()
        return answer