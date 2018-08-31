import os
import subprocess
from flask import Flask, jsonify, render_template, flash, redirect, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegistrationForm
from webservice_helper_method import ip_status, disk_status, all_process_status, network_usage, system_status, \
    memory_status, service_status, agent_list

from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
computer_details = [
    {
        'Networking Details': '',
        'username': 'Administrator',
        'passoword': 'test@123'
    },

]


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/home")
def home():
    return render_template('home.html', computers=agent_list.get_agents())


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/details/<ip>/<guid>/<username>/<password>/<port>")
def details(ip, guid, username, password, port):
    # print(ip)
    # print(guid)
    # print(username)
    # print(password)
    # print(port)

    return render_template('details.html', username=username, password=password, port=port,
                           ip=ip, guid=guid,
                           title='details', ip_details=get_ip_details(),
                           system_details=get_system_details(), disk_details=get_disk_details(),
                           memory_details=get_memory_details(), process_details=get_all_process_details(),
                           service_details=get_service_details(), network_details=get_network_details())


@app.route('/get_ip_details', methods=['GET'])
def get_ip_details():
    response_ip = ip_status.get_ip()
    return response_ip


@app.route('/get_memory_details', methods=['GET'])
def get_memory_details():
    response = memory_status.get_memory_usage()
    return response


@app.route('/get_network_details', methods=['GET'])
def get_network_details():
    response = network_usage.get_network()
    return response


@app.route('/get_disk_details', methods=['GET'])
def get_disk_details():
    response = disk_status.get_disk_usage()
    return response


@app.route('/get_all_process_details', methods=['GET'])
def get_all_process_details():
    response = all_process_status.process_list()
    return response


@app.route('/get_system_details', methods=['GET'])
def get_system_details():
    response = system_status.system_status()
    return response


@app.route('/get_service_details', methods=['GET'])
def get_service_details():
    response = service_status.service_list()
    return response


@app.route('/start_service/<name>', methods=['GET', 'POST'])
def start_service(name):
    if subprocess.call(["net start " + name], shell=True):
        flash('You have Successfully terminated Service  {} '.format(name), 'success')
        return redirect(url_for('details'))
    else:
        flash('There is some problem in starting service {} '.format(name), 'error')
        return redirect(url_for('details'))


@app.route('/stop_service<name>', methods=['GET', 'POST'])
def stop_service(name):
    if subprocess.call(["net stop " + name], shell=True):
        flash('You have Successfully terminated Service  {} '.format(name), 'success')
        return redirect(url_for('details'))
    else:
        flash('There is some problem in terminating service {} '.format(name), 'error')
        return redirect(url_for('details'))


@app.route('/restart_service/<name>', methods=['GET', 'POST'])
def restart_service(name):
    if subprocess.call(["net restart " + name], shell=True):
        flash('You have Successfully restart Service  {} '.format(name), 'success')
        return redirect(url_for('details'))
    else:
        flash('There is some problem in restarting service {} '.format(name), 'error')
        return redirect(url_for('details'))


@app.route('/rdp/<ip>/<username>/<password>/<port>', methods=['GET', 'POST'])
def rdp(ip, username, password, port):
    os.system(
        "py -2 D:\Python_hands_on\RAR\webservice_helper_method\my_rdp.py -u " + username + " -p " + password + " " + ip + ":" + port)
    return redirect(url_for('home'))


@app.route('/kill_process/<process_name>', methods=['GET', 'POST'])
def kill_process(process_name):
    print(process_name)
    if os.system(r"Taskkill /IM " + str(process_name) + " /F") == 0 or 128:
        flash('You have Successfully terminated process name {} '.format(process_name), 'success')
    else:
        flash('You have not proper permission on process name  {}'.format(process_name), 'error')
    return redirect(url_for('details'))


@app.route('/action', methods=['GET', 'POST'])
def action():
    obj1 = request.form.to_dict(flat=False)
    kill_process_name = obj1['kill_process_exe_path']
    start_process_name = obj1['start_process_exe_path']
    manage_services = obj1['manage_service']
    print(kill_process_name)
    print(start_process_name)
    print(manage_services)
    if len(kill_process_name) == 1:
        for process_name in kill_process_name:
            if process_name:
                r, e = subprocess.Popen(process_name, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).communicate()
                result = r.decode('utf-8')
                error = e.decode('utf-8')
                if not error:
                    flash('{}'.format(result), 'success')
                else:
                    flash('{}'.format(error), 'error')
    if len(start_process_name) == 1:
        for process_name in start_process_name:
            if process_name:
                if r"\\" in process_name:
                    new = '"' + process_name + '"'
                else:
                    new = process_name
                print(new)
                r, e = subprocess.Popen(new, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).communicate()
                result = r.decode('utf-8')
                error = e.decode('utf-8')
                if not error:
                    flash('{}'.format(result), 'success')
                else:
                    flash('{}'.format(error), 'error')

    if len(manage_services) == 1:
        for manage in manage_services:
            if manage:
                r, e = subprocess.Popen(manage, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE).communicate()
                result = r.decode('utf-8')
                error = e.decode('utf-8')
                if not error:
                    flash('{}'.format(result), 'success')
                else:
                    flash('{}'.format(error), 'error')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
