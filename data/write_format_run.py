import glob

with open('format_run.sh', 'w') as bashfile:
    for csv_file in glob.iglob('/Volumes/thesis-data/unformatted/*.csv'):
        bashfile.write('python format.py {}'.format(csv_file) + '\n')
