# encoding: UTF-8
from jinja2 import Environment, FileSystemLoader, Template
from rdflib.parser import StringInputSource

import pandas as pd
from pyrml import RMLConverter

out_path = "../PABAKE/virtuoso/graphs/"


def digest(s):
	print(s)
	return s.replace(".", "_")
	# hash = hashlib.md5(s.encode())
	# return hash.hexdigest()

def sensor_id(row):
    return digest(row["STAT_CODE"] + row["NETWORK"])

def get_string(s):
    return str(s)

def timestamp(date_string):
    if " " not in date_string:
        date_string = date_string + " 00:00:00"
    time = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return time.isoformat()

def build_project(env):
	template = env.get_template('project.ttl')
	rml_mapping = template.render()

	rml_converter = RMLConverter().convert(StringInputSource(rml_mapping.encode('utf-8')))

	rml_converter.serialize(destination=out_path + "project_out.ttl", format="ttl")


if __name__ == '__main__':
	file_loader = FileSystemLoader('.')
	env = Environment(loader=file_loader)

	print("Build Project")
	build_project(env)

	observations_df = pd.read_csv('obs/observations.csv', sep=";")

	for index, row in observations_df.iterrows():
		if index == 1:
			break
		wave_path = row[0].split("/")[-1]
		wave_filename = str(row[9]) + str(wave_path.split('.')[0]) + str(wave_path.split('.')[1])
		print(wave_filename)

		# OBS
		vars_dict = {
			"DATA": "obs/csv/wave/" + row[8] + "/" + wave_path,
			"CODE_PLACE": str(row[9]) if len(str(row[9]))>5 else "0"+str(row[9]),
			"STAT_CODE": row[1],
			"NETWORK": row[2] if len(str(row[2]))>1 else "0"+str(row[2]),
			"TYPE": row[3].lower(),
		}
		# TODO mettere il nome del file nel file di output perchè va a sovrascrivere sempre lo stesso file
		# hm0
		print(out_path)
		print(vars_dict)

		rml_converter = RMLConverter()
		rml_converter.register_function("digest", digest)
		graph = rml_converter.convert('observation.ttl', False, vars_dict)
		graph.serialize(destination=out_path + "observation_out_" + wave_filename + ".ttl", format="ttl")

		rml_converter = RMLConverter()
		rml_converter.register_function("digest", digest)
		graph = rml_converter.convert('observationHm0.ttl', False, vars_dict)
		graph.serialize(destination=out_path + "observationHm0_out_" + wave_filename + ".ttl", format="ttl")

		# dir
		rml_converter = RMLConverter()
		rml_converter.register_function("digest", digest)
		graph = rml_converter.convert('observationDir.ttl', False, vars_dict)
		graph.serialize(destination=out_path + "observationDir_out_" + wave_filename + ".ttl", format="ttl")

		# Tm
		rml_converter = RMLConverter()
		rml_converter.register_function("digest", digest)
		graph = rml_converter.convert('observationTm.ttl', False, vars_dict)
		graph.serialize(destination=out_path + "observationTm_out_" + wave_filename + ".ttl", format="ttl")

		# Tp
		rml_converter = RMLConverter()
		rml_converter.register_function("digest", digest)
		graph = rml_converter.convert('observationTp.ttl', False, vars_dict)
		graph.serialize(destination=out_path + "observationTp_out_" + wave_filename + ".ttl", format="ttl")

	'''
	rml_converter = RMLConverter()
	rml_converter.register_function("digest", digest)
	rml_converter.register_function("sensor_id", sensor_id)
	rml_converter.register_function("timestamp", timestamp)
	rml_converter.convert(StringInputSource(rml_mapping.encode('utf-8')))

	rml_converter.serialize(destination="project_out.ttl", format="ttl")

	'''
