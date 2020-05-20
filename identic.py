import argparse
import os
import hashlib
import operator

#as recommended I  use arparse library to read given input
parser=argparse.ArgumentParser()
parser.add_argument("-cn",help="Identical will mean both the contents and the directory/file names are exactly the same.",action="store_true")
group1=parser.add_mutually_exclusive_group()
group1.add_argument("-f",action="store_true")
group1.add_argument("-d",action="store_true")
parser.add_argument('-c',help="Identical will mean the contents are exactly the same (note that the names can be different).",action="store_true")
parser.add_argument("-n",help="Identical will mean the directory/file names are exactly the same	(note that the contents can	be different).",action="store_true")
parser.add_argument("-s",action="store_true" ,
help="The size for each	duplicate will also	be  printed. The  duplicates should	be printed in descending order of size.This	option is to be	ignored	when –n	option is used.")
parser.add_argument('args',nargs='*')
args=parser.parse_args()


#this funciton split dictionaries into related groups according to their hash-values and returns list that have dictionaries groups
def split_into_groups(result):
    temp_list=[]
    for key,value in result.items():
        aa=True
        for x in temp_list:
            if value in x.values():
                index=temp_list.index(x,0,len(temp_list))
                temp_list[index].update({key:value})
                aa=False
        else:
            if aa:
               temp_list.append({key:value})
    return temp_list
#this function takes a list ready to output and splits elements into groups and sort them according to their alphabetic order and then prints them one by one
def write_display(result):
    available_list=[]
    temp_list=split_into_groups(result)
    for abc in temp_list:
        if len(abc)>1:
            tt=sorted(abc)
            available_list.append(tt)
    sortlandi=sorted(available_list,key=lambda key: key)
    for xx in sortlandi:
        for cc in xx:
            print(cc,'\t')
        print('\t')
def Convert(tup, di): 
    di = dict(tup) 
    return di 
#this function takes list,as parameter, whose dictionary groups and sort them according to their size
def my_sort(ll):
    sorted_list=[]
    while ll:
        temp={}
        tt=sorted(ll.pop(0).items())
        temp=Convert(tt,temp)
        if len(temp)!=1:
            value = next( v for i, v in enumerate(temp.values()) if i == 0 )
            key = next( v for i, v in enumerate(temp.keys()) if i == 0 )
            for eleman in sorted_list:
                value2 = next( v for i, v in enumerate(eleman.values()) if i == 0 )
                key2 = next( v for i, v in enumerate(eleman.keys()) if i == 0 )
                if value>value2 or(value==value2 and key<key2):
                    indexx=sorted_list.index(eleman,0,len(sorted_list))
                    sorted_list.insert(indexx,temp)
                    break
                elif eleman==sorted_list[len(sorted_list)-1]:
                    indexx=sorted_list.index(eleman,0,len(sorted_list))
                    sorted_list.insert(indexx+1,temp)
                    break
            if len(sorted_list)==0:
                sorted_list.append(temp)
    return sorted_list
#this function takes parameter directory_path path and traverses recursively to get files size in given path or sub folders under given path and returns size of directory
def directory_size(start_path):
    total_size = 0
    for path, _, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return str(total_size)
#this function returns hash-value of the content of file by reading given file content in byte-type
def filecontent(files_addres):
    file_hash=hashlib.sha256()
    with open(files_addres,'rb') as f:
        fb=f.read()
        while len(fb)>0:
            file_hash.update(fb)
            fb=f.read()
    return file_hash.hexdigest()
#this function traverse sub directories to find files by using os.walk and put them into list with their hash value and then return list
def for_contents_of_files(x):
    contents_of_files={}
    for root,X,files in os.walk(x):
        for fl in files:
            contents_of_files.update({os.path.join(root,fl):filecontent(os.path.join(root,fl))})
    return contents_of_files
"""this function starts from the leaf of the tree of given root path and traverses backup the tree in the perspective of postorder-traversal,
before that initially processes file contents and put them into list related root-path so all files has own index in list even if that is empty directory, 
Lastly returns contents_of_directories list which has all directories contents"""
def for_contents_of_directories(y):
    contents_of_directories_showed_with_root={}
    contents_of_directories={}
    liste_root=[]
    liste_directories=[]
    files_=[]
    for root,directories,files in os.walk(y):
        liste_root.append(root)
        liste_directories.append(directories)
        files_.append(files)
    for (root,directories,files) in zip(reversed(liste_root) , reversed(liste_directories),reversed(files_)): #to start lead all list reversed
        contents_of_directories_showed_with_root.update({root:[]})
        for dr in directories:
            contents_of_directories_showed_with_root.get(root).append(contents_of_directories_showed_with_root.get(os.path.join(root,dr)))
        for fl in files: #traverse files of root directories and put them into index in root-path
            crpt_for_content_of_file=filecontent(os.path.join(root,fl))
            contents_of_directories_showed_with_root.get(root).append(crpt_for_content_of_file)
        if len(directories)==0 and len(files)==0: #if root-path has no file or directory it is get hashed with space hash
               hash_=hashlib.sha256()
               hash_.update("".encode('utf-8'))
               contents_of_directories_showed_with_root[root]=hash_.hexdigest()
               contents_of_directories[root]=hash_.hexdigest()
        else:
            hash_value=None
            s=""
            for x in contents_of_directories_showed_with_root.get(root): #if root directory hash file or sub directories, all hash-values are combined and hashed again
                s=s+x
            hash_value=hashlib.sha256()
            hash_value.update(s.encode('utf-8'))
            contents_of_directories_showed_with_root[root]=hash_value.hexdigest()
            contents_of_directories[root]=hash_value.hexdigest()
    return contents_of_directories
#this funtion traverse all files by starting from given root and hashes them with their name
def name_of_files_for_dublicate(z):
    name_of_files={}
    for root,Y,files in os.walk(z):
        for fl in files:
            name=hashlib.sha256()
            name.update(fl.encode('utf-8'))
            xx=name.hexdigest()
            name_of_files.update({os.path.join(root,fl):xx})
    return name_of_files
#this function traverse all directories from leaf to root and return list containing names of all directories
def names_of_directories_for_duplicate(k):
    name_of_directories_showed_with_root={}
    name_of_directories={}
    liste_root=[]
    liste_directories=[]
    liste_files=[]
    for root,directories,files in os.walk(k):
        liste_root.append(root)
        liste_directories.append(directories)
        liste_files.append(files)
    for (root,directories,files) in zip(reversed(liste_root), reversed(liste_directories), reversed(liste_files)):
        name_of_directories_showed_with_root.update({root:[]})
        for dr in directories:
            name_of_directories_showed_with_root.get(root).append(name_of_directories_showed_with_root.get(os.path.join(root,dr))) #add hash value of sub directories to root directories
        for fl in files: #add hash value of file to root directories
            file_hash=hashlib.sha256()
            file_hash.update(fl.encode('utf-8'))
            name_of_directories_showed_with_root.get(root).append(file_hash.hexdigest())
        string=""
        string=root
        root2=string.rsplit("/",1)
        if len(root2)==1:
            root2=root
        else:
            root2=root2[1]
        if len(directories)==0 and len(files)==0: #if there is no file or sub directory
                hash_=hashlib.sha256()
                hash_.update(root2.encode('utf-8'))
                ff=hash_.hexdigest()
                hash_.update(ff.encode('utf-8'))
                name_of_directories_showed_with_root[root]=hash_.hexdigest()
                name_of_directories[root]=hash_.hexdigest()
        else: #else
            hash_value=None
            s=""
            hash_=hashlib.sha256()
            hash_.update(root2.encode('utf-8'))
            s=s+hash_.hexdigest()
            for x in sorted(name_of_directories_showed_with_root.get(root)):
                s=s+x
            hash_value=hashlib.sha256()
            hash_value.update(s.encode('utf-8'))
            name_of_directories_showed_with_root[root]=hash_value.hexdigest()
            name_of_directories[root]=hash_value.hexdigest()
    return name_of_directories
#this funtion is used in -cn option and this function binds hash-values of name and contents for dir or files
def trasla(list1,list2):
    common_list={}
    for i in list1.items():
        temp=list2.get(i[0])
        if temp==None:
            continue
        hash_value=hashlib.sha256()
        s=""
        s=s+i[1]
        s=s+temp
        hash_value.update(s.encode('utf-8'))
        common_list.update({i[0]:hash_value.hexdigest()})
    return common_list
#this function is used in only -s option to print path and sizes
def yazdir(y):
    for a in y:
        if len(a)>1:
            srtoed=sorted(a.items())
            for i in srtoed:
                print(i[0]," \t",i[1])
            print('\t')
#this funtion gets the size of files in given path
def size_of_files(x):
    for i in x:
        for j in i.items():
            size_=os.path.getsize(j[0])
            i[j[0]]=size_
    return my_sort(x)
#this funtion gets the size of directories in given path
def size_of_directories(starting_path):
    for i in starting_path:
        for j in i.items():
            i[j[0]]=directory_size(j[0])
    return starting_path
#main function is used to control all corditantion and options to give the proper output
def main():
    if len(args.args)==0:
        args.args.append(os.path.abspath('./'))
    else:
        for i in range(0,len(args.args)):
           args.args[i]=os.path.abspath(args.args[i])
    if args.c and args.n:
        args.c=False
        args.n=False
        args.cn=True
    if args.n and args.s:
        args.s=False
    if args.f or not args.d:
        if args.s:
                if args.c or not args.cn:#ok
                    file_content_for_me={}
                    for i in range(0,len(args.args)):
                        file_content_for_me.update(for_contents_of_files(args.args[i]))
                    file_content_for_me=split_into_groups(file_content_for_me)
                    ready_for_write=size_of_files(file_content_for_me)
                    yazdir(my_sort(ready_for_write))
                elif args.cn:#ok
                    file_content={}
                    file_name={}
                    for i in range(0,len(args.args)):
                        file_content.update(for_contents_of_files(args.args[i]))
                        file_name.update(name_of_files_for_dublicate(args.args[i]))
                    ready_for_size=trasla(file_content,file_name)
                    ready_for_write=split_into_groups(ready_for_size)
                    ready_for_write=size_of_files(ready_for_write)
                    ready_for_write=my_sort(ready_for_write)
                    yazdir(ready_for_write)
        elif args.c or (not args.n and not args.cn):#ok
            for_contents_of_files_={}
            for i in range(0,len(args.args)):
                for_contents_of_files_.update(for_contents_of_files(args.args[i]))
            write_display(for_contents_of_files_)
        elif args.n:#ok
            name_of_files={}
            for i in range(0,len(args.args)):
               name_of_files.update(name_of_files_for_dublicate(args.args[i]))
            write_display(name_of_files)
        elif args.cn:#ok
            fl_contents={}
            fl_list_name={}
            for i in range(0,len(args.args)):
                fl_contents.update(for_contents_of_files(args.args[i]))
                fl_list_name.update(name_of_files_for_dublicate(args.args[i]))
            write_display(trasla(fl_contents,fl_list_name))
    elif args.d:
        if args.s:#ok
                if args.c or not args.cn:
                    dr_content={}
                    for i in range(0,len(args.args)):
                        dr_content.update(for_contents_of_directories(args.args[i]))
                    dr_content=split_into_groups(dr_content)
                    dr_content=size_of_directories(dr_content)
                    a=my_sort(dr_content)
                    yazdir(a)
                elif args.cn:#ok
                    dr_content={}
                    dr_name={}
                    for i in range(0,len(args.args)):
                        dr_content.update(for_contents_of_directories(args.args[i]))
                        dr_name.update(names_of_directories_for_duplicate(args.args[i]))
                    ready_for_size=trasla(dr_content,dr_name)
                    ready_for_write=split_into_groups(ready_for_size)
                    ready_for_write=size_of_directories(ready_for_write)
                    yazdir(my_sort(ready_for_write))
        elif args.c or (not args.n and not args.cn):#ok
            for_contents_of_directories_={}
            for i in range(0,len(args.args)):
                for_contents_of_directories_.update(for_contents_of_directories(args.args[i]))
            write_display(for_contents_of_directories_)
        elif args.n:#ok
            names_of_directories_for_duplicate_={}
            for i in range(0,len(args.args)):
                names_of_directories_for_duplicate_.update(names_of_directories_for_duplicate(args.args[i]))
            write_display(names_of_directories_for_duplicate_)
        elif args.cn:#ok
            dr_name_list={}
            dr_content_list={}
            for i in range(0,len(args.args)):
                dr_name_list.update(names_of_directories_for_duplicate(args.args[i]))
                dr_content_list.update(for_contents_of_directories(args.args[i]))
            temp=trasla(dr_name_list,dr_content_list)
            write_display(temp)
if __name__=='__main__':
        main()