import argparse
import json
import sys
import os.path

from string import Template


templateString = """
/*
 * $name.h
 *
 *  Created on:
 *      Author:
 */

#ifndef ${capitalName}_H
#define ${capitalName}_H

#include <QObject>

class $name: public QObject {
    Q_OBJECT
$propertyStatments
public:
    $name(QObject * parent) : QObject(parent) {}
$methods
$signals
$members
};

#endif /* ${capitalName}_H */
"""

class Property:
	def __init__(self, args):
		self.__name = args["name"]
		self.__type = args["type"]
		operations = args["operations"]
		self.__has_read = "r" in operations
		self.__has_write = "w" in operations
		self.__has_notify = "n" in operations
		self.__has_final = "f" in operations
	def memberClass(self):
		return "    {0} m_{1};\n".format(self.__type, self.__name);
	def propertyStatment(self):
		extras = ""
		extras += " READ {0}".format(self.__name) if self.__has_read else ""
		extras += " WRITE set{0}".format(self.__name.title()) if self.__has_write else ""
		extras += " NOTIFY {0}Changed".format(self.__name) if self.__has_notify else ""
		extras += " FINAL" if self.__has_final else ""
		result = "    Q_PROPERTY({0} {1}{2})\n".format(self.__type, self.__name, extras)
		return result
	def signal(self):
		return "    void {0}Changed();\n".format(self.__name) if self.__has_notify else ""
	def inlineMethods(self):
		readMethod = \
        "    {0} {1}() {{\n        return m_{1};\n    }}".format(self.__type, self.__name) if self.__has_read else ""
		signal = "            emit {0}Changed();\n".format(self.__name)
		writeMethod = "    void set{2}({1} new{2}){{\n        if(m_{0} != new{2}) {{\n            m_{0} = new{2};\n{3}        }}\n    }}\n".format(self.__name, self.__type, self.__name.title(), signal if self.__has_notify else "")
		return "\n".join([x for x in [readMethod, writeMethod] if x != ""])


class Model:
	def __init__(self):
		self.__name = ""
		self.__destinyDirectory = ""
		self.__capitalName = ""
		self.__propertyStatments = ""
		self.__signals = "signals:\n"
		self.__privateAttributes = "private:\n"
		self.__methods = ""
		self.__repr = ""
	def fileName(self):
		return self.__name + ".hpp"
	def digest(self, file_path):
		json_file = json.load(open(file_path, "r"))
		self.__destinyDirectory = os.path.dirname(file_path)
		self.__name = json_file["name"]
		self.__capitalName = self.__name.upper()
		for pkw in json_file["properties"]:
			p = Property(pkw)
			self.__propertyStatments += p.propertyStatment()
			self.__signals += p.signal()
			self.__privateAttributes += p.memberClass()
			self.__methods += p.inlineMethods()
		template = Template(templateString)
		self.__repr = template.substitute(name = self.__name,
							   capitalName = self.__capitalName,
							   propertyStatments = self.__propertyStatments,
							   methods = self.__methods,
							   signals = self.__signals,
							   members = self.__privateAttributes)
	def save(self, path=""):
		result = 0
		try:
			dest_dir = path if path else self.__destinyDirectory
			newFile = open(os.path.join(dest_dir, self.fileName()), "w+")
			newFile.write(str(m))
			newFile.close()
		except IOError as e:
			print "Error during saving file({0}): {1}\nCheck the output folder and try it again.".format(e.errno, e.strerror)
			result = 1
		return result
	def __repr__(self):
		return self.__repr

if __name__ == "__main__":
	parser = argparse.ArgumentParser("qtmodelgen.py", description="This is a tool designed for helping you to gen models based on json description files.")
	parser.add_argument("json_files", nargs="+", metavar="json_description_file",
                   help='These are the files used as base for generating the desired models.')
	parser.add_argument('-o', '--output-folder', help="The destiny FOLDER (NOT FILE) for all generated models.", default=".")
	args = parser.parse_args(sys.argv[1:])
	for f in args.json_files:
		m = Model()
		json_file = json.load(open(f, "r"))
		m.digest(f)
		if m.save(args.output_folder):
			print("Generating code for: {0}...[FAIL]".format(m.fileName()))
		else:
			print("Generating code for: {0}...[OK]".format(m.fileName()))
