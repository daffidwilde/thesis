from glob import iglob

for plot_script in iglob('./**/main.py'):
    with open(plot_script, 'r') as r:
        read_file = r.read()
        new_file = read_file.replace('plt.savefig(filename)',
                                     'plt.savefig(filename, transparent=True)')
    with open(plot_script, 'w') as w:
        w.write(new_file)
