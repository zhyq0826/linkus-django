#-*- coding:utf-8 -*-
import os
import shutil


def recursive_clean_svn(path):
    #if current path is dirctory, get dirctory 
    if os.path.isdir(path):
        #get current path content
        path_content = os.listdir(path)
        # if current dirctory content is empty, return 
        if not path_content:
            return 

        for i in path_content:
            child_path = os.path.join(path,i)
            #process if child path is dirctory
            if os.path.isdir(child_path):
                #if dirctory is svn 
                if i == '.svn':
                    #because os.rmdir can't be allowed to deldte not-empty dirctory must empty svn dirctory
                    for root,dirs,files in os.walk(child_path,topdown=False):
                        for name in files:
                            os.remove(os.path.join(root,name))
                        for name in dirs:
                            os.rmdir(os.path.join(root,name))
                    try:
                        os.rmdir(child_path)
                    except:
                        raise 
                else:
                    recursive_clean_svn(child_path)
            else:
                continue
    else:
        return

if __name__ == '__main__':
    current_path = os.getcwd()
    print current_path
    recursive_clean_svn(current_path)

