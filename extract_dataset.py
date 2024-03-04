import os
import tarfile
import threading
from multiprocessing import Process,Pool

def untar_task(dir,file):
	""" untar single file {part1.tar, part2.tar, align.tar} """

	extract_here = file.split(".tar")[0]
	try:
		os.mkdir(extract_here)
	except FileExistsError:
		return # assuming extracted if directory made

	with tarfile.open(os.path.join(dir,file)) as tar:

		for i in tar:
			if not i.isdir():
				# reset file path internally
				i.name = os.path.join(dir,extract_here,os.path.basename(i.name))
				tar.extract(i)


def extracting_task(dir):
	# making sx as root of the os.path
	os.chdir(dir)
	threads = []
	for file in os.listdir(dir):
		if os.path.isfile(os.path.join(os.getcwd(),file)):
			thread = threading.Thread(target = untar_task , args = (dir,file,))
			threads.append(thread)
			thread.start()

	for t in threads:
		t.join()

	os.system("rm *.tar")


def driver(root):

	with Pool(processes = 4) as pool:

		dirs = [ os.path.join(root,dir) for dir in os.listdir(root)]
		pool.map(extracting_task,dirs)


if __name__ == "__main__":

	driver("/home/ubuntu/zipped_dataset")
	print("Done!")
