import hashlib
import sys,os
import json

default_coding='utf-8'
path=os.path.join('.','users.db')
user_data={}

def get_md5(str):
    md5=hashlib.md5()
    md5.update(str.encode(default_coding))
    return md5.hexdigest()

def register(username, password):
    if not user_data.get(user_name):
        user_data[username]=get_md5(password+username)
        print('已将用户:{} 密码:{} 添加到数据库'.format(username, password))
        return True
    print("用户已注册")
    return False

def login(username,password):
    if user_data.get(username)==None:
        print("用户不存在！")
        return -1
    password=get_md5(password+user_name)
    if user_data.get(username)!=password:
        print("密码错误！")
        return 0
    print("登陆成功！")
    return 1

if __name__ =='__main__':
    user_name = sys.argv[1]
    user_password = sys.argv[2]
    if not os.path.exists(path):
        with open(path,'w',encoding=default_coding) as file:
            register('admin','admin')
            register(user_name, user_password)

            json.dump(user_data,file,ensure_ascii=False)

    else:
        with open(path,'r+',encoding=default_coding) as file:
            read=file.read()
            user_data=json.loads(read,encoding=default_coding)
            if login(user_name,user_password)==-1:
                print("用户不存在，是否注册！(Y)")
                if input().upper()=='Y':
                    register(user_name,user_password)
                    file.seek(0,0)
                    json.dump(user_data,file,ensure_ascii=False)