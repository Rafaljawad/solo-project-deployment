import this
from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_app.models import user,show


#CREATE_____________CONTROLLER
@app.route('/add/new/show',methods=['POST','GET'])
def create_show():
    if request.method=='GET':
        if 'user_id' in session:
            return render_template('new_show.html')
        else:
            return redirect('/')
    #if the method is post:
    if show.Show.create_show(request.form):
        return redirect('/dashboard')
    else:
        return render_template('new_show.html')


# READ______________CONTROLLER
@app.route('/display/show/<int:id>')
def display_show(id):
    this_show=show.Show.get_show_by_id(id)
    return render_template('show_details.html',this_show=this_show)


#EDIT______________CONTROLLERS
@app.route('/show/edit/<int:id>',methods=['POST','GET'])
def edit_show(id):
    if request.method=='GET':
        if 'user_id' not in session:
            return redirect('/')
        else:
            this_show=show.Show.get_show_by_id(id)
            return render_template('edit_show.html',this_show=this_show)
    show_data={
        'id':id,
        'title':request.form['title'],
        'network':request.form['network'],
        'date':request.form['date'],
        'description':request.form['description']
        }
    if show.Show.update_show_by_id(show_data)==None:
        return redirect('/dashboard')
    this_show=show.Show.get_show_by_id(id)
    return render_template('edit_show.html',this_show=this_show)

#DELETE______________CONTROLLERS
@app.route('/show/delete/<int:id>')
def delete_report(id):
    if 'user_id' not in session:
            return redirect('/')
    show.Show.delete_show(id)
    return redirect('/dashboard')