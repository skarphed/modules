import pygtk
pygtk.require("2.0")
import gtk
import webkit

import os

from data.skarphed.Skarphed import module_rpc


class WidgetPage(gtk.VBox):
    def __init__(self, parent, widget):
        self.par = parent
        gtk.VBox.__init__(self)
        self.widgetId = widget.getLocalId()

        self.editor = webkit.WebView()
        self.editor.set_editable(True)

        scroll = gtk.ScrolledWindow()
        scroll.add(self.editor)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.ui = self.generateUi()
        #self.add_accel_group(self.ui.get_accel_group())
        self.toolbar_main = self.ui.get_widget("/toolbar_main")
        self.toolbar_format = self.ui.get_widget("/toolbar_format")
            
        self.pack_start(self.toolbar_main, False)
        self.pack_start(self.toolbar_format, False)
        self.pack_start(scroll, True, True)

        self.show()

        self.loadContent()

    def generateUi(self):
        ui_def = """
        <ui>
            <toolbar name="toolbar_main">
                <toolitem action="save" />
                <separator />
                <toolitem action="undo" />
                <toolitem action="redo" />
                <separator />
                <toolitem action="cut" />
                <toolitem action="copy" />
                <toolitem action="paste" />
            </toolbar>
            <toolbar name="toolbar_format">
                <toolitem action="bold" />
                <toolitem action="italic" />
                <toolitem action="underline" />
                <toolitem action="strikethrough" />
                <separator />
                <toolitem action="font" />
                <toolitem action="color" />
                <separator />
                <toolitem action="justifyleft" />
                <toolitem action="justifyright" />
                <toolitem action="justifycenter" />
                <toolitem action="justifyfull" />
            </toolbar>
        </ui>
        """

        actions = gtk.ActionGroup("Actions")
        actions.add_actions([
            ("save", gtk.STOCK_SAVE, "_Save", None, None, self.onSave),

            ("undo", gtk.STOCK_UNDO, "_Undo", None, None, self.onAction),
            ("redo", gtk.STOCK_REDO, "_Redo", None, None, self.onAction),

            ("cut", gtk.STOCK_CUT, "_Cut", None, None, self.onAction),
            ("copy", gtk.STOCK_COPY, "_Copy", None, None, self.onAction),
            ("paste", gtk.STOCK_PASTE, "_Paste", None, None, self.onPaste),

            ("bold", gtk.STOCK_BOLD, "_Bold", "<ctrl>B", None, self.onAction),
            ("italic", gtk.STOCK_ITALIC, "_Italic", "<ctrl>I", None, self.onAction),
            ("underline", gtk.STOCK_UNDERLINE, "_Underline", "<ctrl>U", None, self.onAction),
            ("strikethrough", gtk.STOCK_STRIKETHROUGH, "_Strike", "<ctrl>T", None, self.onAction),

            ("font", gtk.STOCK_SELECT_FONT, "Select _Font", "<ctrl>F", None, self.onSelectFont),
            ("color", gtk.STOCK_SELECT_COLOR, "Select _Color", None, None, self.onSelectColor),

            ("justifyleft", gtk.STOCK_JUSTIFY_LEFT, "Justify _Left", None, None, self.onAction),
            ("justifyright", gtk.STOCK_JUSTIFY_RIGHT, "Justify _Right", None, None, self.onAction),
            ("justifycenter", gtk.STOCK_JUSTIFY_CENTER, "Justify _Center", None, None, self.onAction),
            ("justifyfull", gtk.STOCK_JUSTIFY_FILL, "Justify _Full", None, None, self.onAction)
        ])

        ui = gtk.UIManager()
        ui.insert_action_group(actions)
        ui.add_ui_from_string(ui_def)
        return ui

    def onAction(self, action):
        self.editor.execute_script(
                "document.execCommand('%s', false, false);" % action.get_name())
    def onPaste(self, action):
        self.editor.paste_clipboard()

    def onSelectFont(self, action):
        dialog = gtk.FontSelectionDialog("Select a font")
        if dialog.run() == gtk.RESPONSE_OK:
            fname, fsize = dialog.fontsel.get_family().get_name(), dialog.fontsel.get_size()
            self.editor.execute_script("document.execCommand('fontname', null, '%s');" % fname)
            self.editor.execute_script("document.execCommand('fontsize', null, '%s');" % fsize)
        dialog.destroy()

    def onSelectColor(self, action):
        dialog = gtk.ColorSelectionDialog("Select Color")
        if dialog.run() == gtk.RESPONSE_OK:
            gc = str(dialog.colorsel.get_current_color())
            color = "#" + "".join([gc[1:3], gc[5:7], gc[9:11]])
            self.editor.execute_script("document.execCommand('forecolor', null, '%s');" % color)
        dialog.destroy()

    def onSave(self, action):
        content = self.getHtml()
        self.set_content(content)

    def setHtml(self, html):
        self.editor.load_html_string(html, "file:///")

    def getHtml(self):
        self.editor.execute_script("document.title=document.documentElement.innerHTML;")
        content = self.editor.get_main_frame().get_title()
        first = content.find("<body>")
        last = content.find("</body>")
        content = content[first+6:last]
        return content

    def loadContentCallback(self, data):
        self.setHtml(data)

    @module_rpc(loadContentCallback)
    def get_content(self):
        pass

    def loadContent(self):
        self.get_content()

    def setContentCallback(self, data):
        self.loadContent()

    @module_rpc(setContentCallback)
    def set_content(self, content):
        pass

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
