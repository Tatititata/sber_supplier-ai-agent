import requests

BASE_URL = "http://127.0.0.1:8000"

def get_token(user='user', password='userpassword'):
    if user == '':
        user = 'user'
    if password == '':
        password = 'userpassword'
    url = f"{BASE_URL}/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"username": user, "password": password}
    
    resp = requests.post(url, headers=headers, data=data)
    
    if resp.status_code == 200:
        token = resp.json().get('access_token')
        return token
    else:
        print(f"Error: {resp.status_code}")
        return None

def send_task(access_token, file='test.txt'):
    if file == '':
        file = 'test.txt'
    headers = {"Authorization": f"Bearer {access_token}"}
    with open(file, "rb") as f:
        resp = requests.post(f"{BASE_URL}/cp/tasks", headers=headers, files={"file": f})

    if resp.status_code == 200:
        # print("Task sent")
        return resp.json()
    else:
        print("Error")
        return None

def get_task(access_token, task_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(f"{BASE_URL}//cp/tasks/{task_id}", headers=headers)
    if resp.status_code == 200:
        task = resp.json()
        # print('Got task')
        return task
    else:
        print("Error")
        return None




def front():
    print("=== Supplier agent ===")

    user_login = None
    user_password = None
    string = '''
    1. Get token
    2. Send task
    3. Check tasks

    q to quit:
    '''
    token = None
    task_id = None
    tasks = []
    while True:
        choice = input(string)
        
        if choice == 'q':
            break
        elif choice == '1':
            user_login = input("Login: ")
            user_password = input("Password: ")
            token = get_token(user_login, user_password)

        elif choice == '2':
            file_name = input("File name: ")
            task = send_task(token, file_name)
            print(task)
            task_id = task.get('task_id')
            if task_id:
                tasks.append(task_id)

        elif choice == '3':
            for i, n in enumerate(tasks, 1):
                print((f'{i} {n}' ))
            try:
                task_id = int(input("enter task id number: "))
                task = get_task(token, tasks[task_id - 1])
                print(*task.items(), sep='\n')
            except:
                print('Number is not correct')
            
from time import sleep
def front1():
    tasks = []
    token = get_token()
    result = []
    for i in range(10):
        task = send_task(token)
        if task:
            tasks.append(task.get('task_id'))
    for i in range(5):
        sleep(1)
        for t in tasks:
            task = get_task(token, t)
            if task:
                result.append([task.get('id'), task.get('status'), task.get('updated_at')])

    result.sort(key = lambda x: (x[0], x[2]))
    print(*result, sep='\n')

if __name__ == "__main__":
    front1()