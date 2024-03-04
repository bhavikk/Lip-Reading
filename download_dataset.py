import os
import multiprocessing


DATASET_DOWNLOAD_PATH = "/home/ubuntu/zipped_dataset"


def download(link,fname):
	import requests
	if os.path.isfile(fname) == False:
		r = requests.get(link, stream = True)
		with open(fname,"wb") as f:
			for chunk in r.iter_content(chunk_size=1024):
				if(chunk):
					f.write(chunk)
try:
	os.mkdir(DATASET_DOWNLOAD_PATH)
except FileExistsError as e:
	pass

os.chdir(DATASET_DOWNLOAD_PATH)

processes = []
for i in range(1,35):

	if i == 21: #speaker 21 video not found
		continue

	folder = f"s{i}"

	try:
		os.mkdir(folder)
	except FileExistsError as e:
		pass

	os.chdir(folder)

	fname = None
	for part in [1,2]:

		fname = f"video_part{part}.tar"
		videolink = f"http://spandh.dcs.shef.ac.uk/gridcorpus/s{i}/video/s{i}.mpg_6000.part{part}.tar"
		process = multiprocessing.Process(target = download , args =(videolink,fname))
		process.start()
		processes.append(process)


	alignlink = f"http://spandh.dcs.shef.ac.uk/gridcorpus/s{i}/align/s{i}.tar"
	# download(alignlink,"align.tar")
	process = multiprocessing.Process(target = download , args =(videolink,"align.tar"))
	process.start()
	processes.append(process)
	# download(videolink,fname)

	os.chdir("../")

for t in processes:
	t.join()
