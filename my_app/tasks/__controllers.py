from flask import render_template, request, redirect, url_for

from flask.views import View

from my_app import app

task_list = ['tasks 1', 'tasks 2', 'tasks 3',]

class ListView(View):
    init_every_request = False

    def __init__(self, template):
        self.template = template

    def dispatch_request(self):
        tasks=task_list
        return render_template(self.template, tasks=tasks)
    
class CreateView(View):
    init_every_request = False

    def __init__(self, template):

        self.template = template

    def dispatch_request(self):
  
        task = request.form.get('task')
        if task is not None:
            task_list.append(task)
            return redirect(url_for('tasks.index'))
        return render_template(self.template)


class UpdateView(View):
    init_every_request = False

    def __init__(self, template):
        self.template = template

    def dispatch_request(self, id):
        task = request.form.get('task')
        if task is not None:
            task_list[id] = task
            return redirect(url_for('tasks.index'))
        return render_template(self.template)

class DetailView(View):
    def __init__(self):
        pass

    def dispatch_request(self, id):
        return 'Show '+str(id)

class DeleteView(View):
    def __init__(self):
        pass

    def dispatch_request(self, id):
        del task_list[id]
        return redirect(url_for('tasks.index'))

app.add_url_rule('/tasks/', view_func=ListView.as_view('tasks.list','dashboard/task/index.html'))
app.add_url_rule('/tasks/<int:id>',view_func=DetailView.as_view('tasks.show'))
app.add_url_rule('/tasks/create/', view_func=CreateView.as_view('tasks.create','dashboard/task/create.html'))
app.add_url_rule('/tasks/update/<int:id>/', view_func=UpdateView.as_view('tasks.update','dashboard/task/update.html'))
app.add_url_rule('/tasks/delete/<int:id>/', view_func=DeleteView.as_view('tasks.delete'))









"""

class DetailView(View):
    def __init__(self, model):
        self.model = model
        self.template = f"{model.__name__.lower()}/detail.html"

    def dispatch_request(self, id)
        item = self.model.query.get_or_404(id)
        return render_template(self.template, item=item)

app.add_url_rule(
    "/users/<int:id>",
    view_func=DetailView.as_view("user_detail", User)
)


from flask import Blueprint, render_template, request, redirect, url_for



taskRoute = Blueprint('tasks',__name__,url_prefix='/tasks',)

@taskRoute.route('/')
def index():
    return render_template('dashboard/task/index.html', tasks=task_list)

@taskRoute.route('/<int:id>')
def show(id:int):
    return 'Show '+str(id)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    del task_list[id]
    return redirect(url_for('tasks.index'))

@taskRoute.route('/create', methods=('GET','POST'))
def create():


@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
def update(id:int):

    task = request.form.get('task')
    if task is not None:
        task_list[id] = task
        return redirect(url_for('tasks.index'))

    return render_template('dashboard/task/update.html')

"""