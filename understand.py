#!/usr/bin/env python
# encoding: utf-8
import json, re
from peewee import *

db = SqliteDatabase('yeahrly.sqlite3')

class School(Model):
	name = CharField(unique=True)
	typee = CharField(choices=(("t","technikum"),("z","zawodowa"),("l","liceum"),("i","inne")))
	class Meta:
		database = db

class Subject(Model):
	name = CharField()
	class Meta:
		database = db

class Clazz(Model):
	name = CharField()
	job = CharField(null=True)
	code = CharField()
	primes = IntegerField(default=0)
	contestors = IntegerField(default=0)
	girls = IntegerField(default=0)
	boys = IntegerField(default=0)
	minimum = FloatField(default=0)
	maximum = FloatField(default=0)
	average = FloatField(default=0)
	school = ForeignKeyField(School, related_name="classes")
	class Meta:
		database = db

class CSBinding(Model):
	clazz = ForeignKeyField(Clazz, related_name="subjects")
	subject = ForeignKeyField(Subject, related_name="classes")
	class Meta:
		database = db

db.connect()

def flot(x):
	return float(re.sub(",",".",x) or "0")

def conv():
	db.create_tables([School, Subject, Clazz, CSBinding], safe=True)
	with open("orly.json") as f:
		data = json.load(f)
	i = 1
	for clazz in data:
		print("%i/%i" % (i, len(data)))
		print(clazz["class"])
		sc = School.get_or_create(name=clazz["school"], typee=("t" if "technikum" in clazz["school"].lower() else "z" if "zawodowa" in clazz["school"].lower() else "l" if "liceum" in clazz["school"].lower() else "i"))[0]
		r = re.match(r"^\((?P<code>.+)\)\s+(?P<intel>.+?)(\s+\(\S+-\S+\))?$", clazz["class"])
		if sc.typee == "l":
			rr = re.match(r"(?:[^\-]+\s)?((?:[a-z]+)(?:\-\s?(?:[a-z]+))*)", r.group("intel").strip())
			c = Clazz.get_or_create(name=clazz["class"], primes=int(clazz["prime"]), girls=int(clazz["f"]), boys=int(clazz["m"]), contestors=int(clazz["contest"]), minimum=flot(clazz["min"]), maximum=flot(clazz["max"]), average=flot(clazz["avg"]), job=(None if rr else r.group("intel")), code=r.group("code"), school=sc)[0]
			if rr:
				print(rr.group(0))
				for g in rr.group(0).split("-"):
					if g is not None:
						CSBinding.get_or_create(clazz=c, subject=Subject.get_or_create(name=g)[0])
		else:
			c = Clazz.get_or_create(name=clazz["class"], job=r.group("intel"), code=r.group("code"), school=sc)[0]
		print(c.code+" "+(c.job or ",".join([x.subject.name for x in c.subjects])))
		i += 1

def listem():
	for s in Subject.select(Subject, fn.Sum(Clazz.girls).alias("girlz"), fn.Sum(Clazz.boys).alias("boyz")).join(CSBinding).join(Clazz).group_by(Subject):
		print("%s\t%i\t%i" % (s.name, s.girlz, s.boyz))

if __name__ == "__main__":
	conv()
