import webapp2
import jinja2
import os
import additional_learning_concepts
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
 autoescape=False)

COMMENT_FROM_PEOPLE_TABLE_NAME = 'comment_from_people_table_name'

def commentFromPeople_key():
    return ndb.Key('comment_from_people', COMMENT_FROM_PEOPLE_TABLE_NAME)

concepts=additional_learning_concepts.concepts


class ExtraResource(ndb.Model):
    # for the comment submitted by user
    catagory = ndb.StringProperty(indexed=False)
    message = ndb.StringProperty(indexed=False)
    link = ndb.StringProperty(indexed=False)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
      self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
      t = jinja_env.get_template(template)
      return t.render(params)

    def render(self, template, **kw):
      self.write(self.render_str(template, **kw))

class MainPage(Handler):

  def render_front(self, error='', catagory='', link=''):
    comments_query = ExtraResource.query()
    comments = comments_query.fetch()
    self.render("note_template.html", concepts=concepts, 
      comments_from_user=comments, error=error, 
      catagory=catagory, link=link)

  def get(self):
    self.render_front()
    

  def post(self):
    messageFromUser = self.request.get("message")
    if messageFromUser:
      # valid input
      # store the data in datastore
      resourceFromUser = ExtraResource(parent=commentFromPeople_key())
      resourceFromUser.catagory = self.request.get("catagory")
      resourceFromUser.message = messageFromUser
      resourceFromUser.link = self.request.get("link")
      resourceFromUser.put()
      self.redirect('/')
    else:
      error = "the comment cannot be empty"
      self.render_front(error=error, catagory=self.request.get("catagory"),
       link=self.request.get("link"))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)