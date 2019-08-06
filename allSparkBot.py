#All Spark Labs Assignment

import json
import re


def spark():
    
    user_inputs = {}

    with open(inPath) as json_file:
        input_data = json.load(json_file)['questions']
        
        for rules in input_data:
            if user_inputs.get('__builtins__'):
                del user_inputs['__builtins__']
            try:

                if rules.get('instruction'):
                    instructions(rules, user_inputs)
                    continue

                if rules.get('text'):
                    print("\n\n",rules)
                    if rules.get('conditions'):
                        con = rules['conditions'][0][0].replace( rules['var'], "user_inputs['" + rules['var'] + "']" )
                        for c in con:
                            while eval(c,user_inputs):
                                if rules.get('text'):
                                    print(rules['var'])
                                    break
                            else:
                                pass
                            
                            x = int(input())
                            user_inputs.update({rules['var']: x })
                            continue
                        
                    if rules.get('option'):
                        opt = rules.get('option')
                        print(rules['text'],'\t',opt)

                    else:
                        x = take_input(rules["text"], rules.get("options"))
                        user_inputs.update({rules['var']: x })

                else:   
                    x = input()
                    user_inputs.update({rules['var']:x})


                if  rules.get('calculated_variable' ):
                    user_inputs[rules["var"]] = calculations(rules, user_inputs)


            except Exception as e:
                print(e)
                pass

def take_input(text, options=[]):
    try:
        inp, opt = "", ""
        if options:
            opt = "(" + " / ".join(options) + ")"

        inp = input("{0} {1}: ".format(text, opt))

        if options and inp not in options:
            print("Invalid option. Please select one of these {0}".format(opt))
            inp = take_input(text, options)

        return inp
    
    except:
        return


def calculations(d, localVar):
	return eval(d["formula"], localVar)


def instructions(data, localVar):
	output = data["instruction"]

	if data.get("list_var") and data.get("list_length"):
		for i in range(0, int(data["list_length"])):
			localVar["i"] = i
			args = [eval(x, localVar) for x in data["instruction_var"]]
			output = data["instruction"] % tuple(args)
			print(output)
		return
	elif data.get("instruction_var"):
		args = [localVar[d] for d in data["instruction_var"]]
		output = output % tuple(args)

	print(output)
            

inPath = str(input())

spark()
