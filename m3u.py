import re
import json
import sys

class m3u:
	def __init__(self, text):
		self.string=text
		self.previousLineWasExt=False
		self.json={"unassigned":[],
					"tags":[]};
		
	def parse(self):
		lines=self.string.splitlines(True)
		
		for line in lines:
			self.curline=line.strip()
			if self.curline: #not an empty line
				self.parseLine()
	
	
	def parseLine(self):
		match=re.search("^\s*#?(EXT[^:]*):?",self.curline)
		if match:
			self.previousLineWasExt=True
			EXT_TAG=match.group(1)
			self.curtag={"name":EXT_TAG,"attribs":{}}
			self.json["tags"].append(self.curtag) #passed by reference
			i=self.curline.find(":")
			if i != -1 and i+1 != len(self.curline):  #no key value pairs
				keyVal=self.curline[i+1:]
				self.parseKeyVal(keyVal)
		else: #link
			link=self.curline;
			
			if self.previousLineWasExt == False:
				print("Found link that cannot be assigned to an EXT Tag");
				self.json["unassigned"].append(self.removeQuotationMarks(link))
			else:
				self.previousLineWasExt = False
				self.curtag["link"]=self.removeQuotationMarks(link);
	
	def parseKeyVal(self, str):
		matches=re.findall("""("[^"]*"|[^"=,]*)\s*=\s*("[^"]*"|[^,]*)""",str)
		if not matches:
			if str.endswith(","):
				self.curtag["val"]=str[:-1]
			else:
				self.curtag["val"]=str
		else:
			for match in matches:
				key=self.removeQuotationMarks(match[0].strip())
				val=self.removeQuotationMarks(match[1].strip())
				if len(self.curtag["attribs"]) > 0 and key in self.curtag["attribs"]:
					print("Dupliate key detected: %s" % key)
				else:
					self.curtag["attribs"][key]=val
	
	def removeQuotationMarks(self, str):
		if str.startswith("\"") and str.endswith("\""):
			return str[1:-1]
		else:
			return str

#usage example
if __name__ == "__main__":
	if(len(sys.argv) == 2):
		filename=sys.argv[1]
		with open(filename) as f:
			str=f.read()
			parser=m3u(str)
			parser.parse()
			print(json.dumps(parser.json))
	else:
		print("Usage: m3u.py filename")