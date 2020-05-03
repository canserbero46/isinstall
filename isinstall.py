#!/usr/bin/python3

import subprocess, sys, getopt, re
import json

def regex_handling(packages_list,opt='-v'):
	if opt=='-v':
		find_criteria=['Status']
	elif opt=='--vv':
		find_criteria=['Status','Version']
	elif opt=='--vvv':
		find_criteria=['Status','Version','Architecture','Maintainer']

	sep=':-;'
	processed_output=dict()
	key_name='Package'
	cont=0
	for package in packages_list:
		cmd=('dpkg -s '+package).strip('\n').split()
		cmd_handler=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		stdout,stderr=cmd_handler.communicate()
		cmd_PIPE=stdout.decode()+stderr.decode()
		processed_output[key_name+str(cont)]={'name':package}
		processed_output[key_name+str(cont)].update(Details={})
		for to_find in find_criteria:
			aux=re.findall(to_find+':\s(.+)',cmd_PIPE)
			if len(aux)==0:
				processed_output[key_name+str(cont)]['Details'][to_find]='None'
				break
			processed_output[key_name+str(cont)]['Details'][to_find]=aux[0]
		cont+=1
	return json.dumps(processed_output,indent=4)

def manage_file(file_name,des,processed_input=''):
	package_list=list()
	sep=' '
	try:
		file=open(file_name,'rt' if des==0 else 'wt',encoding='utf-8')
		if not des:
			packages_per_line=file.readline().strip("\n")
			while packages_per_line!='':
				for package in packages_per_line.split(sep):
					if package=='':
						break
					package_list.append(package)
				packages_per_line=file.readline().strip('\n')
		elif des:
			file.write(processed_input)
		file.close()
	except Exception as e:
		print("Manage",e)
	return package_list if des==0 else None

def check_opt_args(argv):
	short_options="ovi:"
	long_options=["ifile=","ofile","vv","vvv"]
	try:
		opts,remainder=getopt.getopt(argv,short_options,long_options)
		count=0
		for opt,value in opts:
			if opt in ["-i","--ifile"]:
				packages_list=manage_file(value,0)
				#print(packages_list)
			elif opt in ["-v","--vv","--vvv"]:
				processed_output=regex_handling(packages_list,opt)
				print(processed_output)
			elif opt in ["-o","--ofile"]:
				cmd_handler=subprocess.Popen('pwd',stdout=subprocess.PIPE)
				stdout,stderr=cmd_handler.communicate()
				manage_file(value if value!='' else stdout.decode().strip()+'/o_default.txt',1,processed_input)
	except Exception as e:
		print(e)
	except KeyboardInterrupt:
		pass

check_opt_args(sys.argv[1:])
