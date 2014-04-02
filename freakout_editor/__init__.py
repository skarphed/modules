import os
from skarphedcore.module import AbstractModule

class ModuleException(Exception):
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used"""
    }

    @classmethod
    def get_msg(cls, nr, info=""):
        return "DB_" + str(nr) + ": " + cls.ERRORS[nr] + " " + info

class Module(AbstractModule):
    def __init__(self, core):
        AbstractModule.__init__(self, core)
        self._path = os.path.dirname(__file__)
        self._load_manifest()

    def render_pure_html(self, widget_id, args={}):
        return self.get_content(widget_id)

    def render_html(self, widget_id, args={}):
        return self.render_pure_html(widget_id, args)

    def render_javascript(self, widget_id, args={}):
        return ""

    def set_content(self, widget_id, content=""):
        content = unicode(content)
        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO ${content} (MOD_INSTANCE_ID, CON_CONTENT)\
                VALUES (?,?) MATCHING (MOD_INSTANCE_ID);"
        db.query(self, stmnt, (widget_id, content), commit=True)

    def get_content(self, widget_id):
        db = self._core.get_db();
        stmnt = "SELECT CON_CONTENT FROM ${content} WHERE MOD_INSTANCE_ID = ?;"
        cur = db.query(self, stmnt, (widget_id,))
        row = cur.fetchonemap()
        if row is not None:
            return row["CON_CONTENT"]
        else:
            return ""
