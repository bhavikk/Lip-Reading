import requests

response = requests.get('http://spandh.dcs.shef.ac.uk/gridcorpus/s2/video/s2.mpg_vcd.zip', stream=True)


total_size = (response.headers['content-length'])

filename = "s2.mpg_vcd.zip"

chunk_size = 1024

with open(filename, 'wb') as f:

    total = int(total_size) / chunk_size
    cnt = 0
    for data in response.iter_content(chunk_size=chunk_size):
        print("{}/{}\r".format(cnt, total))
        cnt+=1
        f.write(data)


# data = response.read()
#
# filename = 's2.mpg_vcd.zip'
#
# with open(filename, 'wb') as f:
#     f.write(data)
