import tornado.web
import sys

from ex_push_manager import ExamplePushManager

m = ExamplePushManager()
m.connect()

repl_ver_store = m.repl_ver_store()
repl_code_store = m.repl_code_store()

host = sys.argv[1] if len(sys.argv) > 1 else "localhost:11000"

# curl localhost:11000/
class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self, path, **kwargs):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)

template_data = """
<html>
   <head>
      <title>{{ title }}</title>
   </head>
   <body>
     <ul>
       {% for item in items %}
         <li>{{ escape(item) }}</li>
       {% end %}
     </ul>
   </body>
 </html>
"""

repl_ver_store.set(f"template.html", template_data, sync=True)
repl_code_store.set(f"/web/{host}/", HelloWorldHandler, sync=True)
