#!/usr/bin/python3

import subprocess, sys, getopt, re
import json

def regex_handling(raw_input,opt='-v'):
	processed_input=dict()
	if opt=='-v':
		find_result=list()
		find_criteria=['Status','Version','Architecture']
		for to_find in find_criteria:
			find_result.append(re.findall(to_find+':\s(.+)',raw_input))
		inner_cont=0
		cont=0
		for ok,not_ok in re.findall('Package:\s(.+)|(\`.+\')',raw_input):
			cont+=1
			processed_input['node'+str(cont)]={'name':ok if ok!='' else not_ok}
			processed_input['node'+str(cont)].update(Details={})
			if ok!='':
				i_label=0
				for label in find_criteria:
					processed_input['node'+str(cont)]['Details'][label]=find_result[i_label][inner_cont]
					i_label+=1
				inner_cont+=1
			else:
				processed_input['node'+str(cont)]['Details'].update(Status='Not installed')
	elif opt=='-vv':
		pass
	elif opt=='-vvv':
		pass
	return json.dumps(processed_input,indent=4)

def manage_file(file_name,des,processed_input=''):
	raw_input=''
	try:
		file=open(file_name,'rt' if des==0 else 'wt+',encoding='utf-8')
		if not des:
			line=file.readline()
			while line!="":
				cmd=('dpkg -s '+line.strip('\n')).split(" ")
				cmd_handler=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				stdout,stderr=cmd_handler.communicate()
				raw_input+=stdout.decode()+stderr.decode()
				line=file.readline()
		elif des:
			file.write(processed_input)
		file.close()
	except Exception as e:
		print("Manage",e)
	return raw_input if des==0 else None

def check_opt_args(argv):
	short_options="ovi:"
	long_options=["ifile=","ofile="]
	try:
		opts,remainder=getopt.getopt(argv,short_options,long_options)
		count=0
		for opt,value in opts:
			if opt in ["-i","--ifile"]:
				raw_input=manage_file(value,0)
			elif opt in ["-v","-vv","-vvv"]:
				processed_input=regex_handling(raw_input,opt)
			elif opt in ["-o","--ofile"]:
				cmd_handler=subprocess.Popen('pwd',stdout=subprocess.PIPE)
				stdout,stderr=cmd_handler.communicate()
				manage_file(value if value!='' else stdout.decode().strip()+'/o_default.txt',1,processed_input)
	except Exception as e:
		print(e)
	except KeyboardInterrupt:
		pass

check_opt_args(sys.argv[1:])
