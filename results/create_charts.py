# from brokenaxes import brokenaxes
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

known_columns = set(['Python loop [cpu]', 'Numpy [cpu]',
                     'C++ plain [cpu]',
                     'C++ CUDA [cpu]',
                     'C++ OCL [cpu]', 'C++ OCL [gpu]',
                     'PyOCL [cpu]', 'PyOCL [gpu]',
                     'TensorFlow [cpu]', 'TensorFlow [gpu]'])

def create_chart(spec, output_md, use_rel=True):
    print('Processing {} "{}"'.format(spec['data'], spec['title']))

    plt.style.use('ggplot')

    png_file = os.path.splitext(spec['data'])[0] + ".png"

    output_md += "\n\n# {}\n\n".format(spec['title'])
    output_md += "Submitted by {} on {}\n\n".format(spec['by'], spec['date'])

    if spec['remarks']:
        output_md += spec['remarks'] + "\n\n"

    details = spec.get('details')
    if details:
        output_md += "\n### Specs\n\n"
        output_md += "|    |    |\n"
        output_md += "|----|----|\n"
        for row in details:
            output_md += "| {} | {} |\n".format(row[0], row[1])
        output_md += "\n"

    df = pd.read_csv(spec['data'])
    m = df.mean().sort_values(ascending=False)
    for idx in m.index:
        if idx not in known_columns:
            sys.stderr.write("Error: unrecognized column name '{}'\n".format(idx))
            sys.exit(1)
    rel = m / m[-1]
    std = df.std()

    output_md += "\n### Result\n\n"
    output_md += '![{}]({}?raw=true "{}")\n\n'.format(png_file, png_file, png_file)

    output_md += "\n ### Details\n\n"
    output_md += "| Test   | Mean Time (ms) | StdDev (ms) | Time (rel)\n"
    output_md += "|--------| --------: | --------: | --------: |\n"

    for idx in m.index:
        output_md += "| {} | {} | {} | {} |\n".format(idx, "%.3f" % m[idx], "%.3f" % std[idx],
                                                 "%.2fx" % rel[idx])

    output_md += "\n"

    # Remove outliers as we don't support broken/discontinuous axis yet
    notes = ""
    for i in range(len(m) - 1):
        if m[i] / m[i + 1] > 20:
            # print('** Warning: removing outlier "%s" from the chart' % m.index[i])
            notes += '- **outlier "{}" is removed from the chart**\n'.format(m.index[i])
        else:
            break

    if notes:
        output_md += "\n### Notes\n\n" + notes

    m = m[i:]
    rel = rel[i:]

    tests = m.index
    y_pos = np.arange(len(tests)) * 0.6
    y = rel
    xlims = None

    fig = plt.figure(figsize=(10, 2 + 0.6 * len(m)))
    if xlims:
        ax = brokenaxes(xlims=xlims, hspace=.05)
    else:
        ax = plt.subplot(111)

    ax.barh(y_pos, y, height=0.4, align='center', color='green', ecolor='black')

    for i, v in enumerate(y):
        # ax.text(v, i, '%.3fx' % v)
        ax.text(max(0, v - 0.7), y_pos[i], '%.3fx' % v, fontdict={'size': 8}, color='w')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(tests, fontdict={'size': 10})
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Duration Compared to Fastest Test', fontdict={'size': 10})
    ax.set_title(spec['title'], fontdict={'size': 14})

    ax.grid(color='w')
    plt.savefig(png_file, bbox_inches='tight')

    output_md += "\n\n"
    return output_md


README_MD = """
# Results

This page is autogenerated from the results recorded in CSVs and [result_specs.json](result_specs.json)
file. Feel free to submit a result:
1. Record your test results in a CSV file. Repeat each test at least 5 times. See other csv files for samples.
2. Create an entry in [result_specs.json](result_specs.json)
3. Create pull request

When creating a CSV, please standardize the column names to use the following names, otherwise
the CSV will be rejected by `create_charts.py`:
- 'Python loop [cpu]', 'Numpy [cpu]', 
- 'C++ plain [cpu]', 
- 'C++ CUDA [cpu]', 
- 'C++ OCL [cpu]', 'C++ OCL [gpu]',
- 'PyOCL [cpu]', 'PyOCL [gpu]',
- 'TensorFlow [cpu]', 'TensorFlow [gpu]'
"""

if __name__ == "__main__":
    specs = json.loads(open('result_specs.json').read())
    output_md = README_MD

    for spec in specs:
        output_md = create_chart(spec, output_md)

    print('Writing README.md..')
    f = open('README.md', 'w')
    f.write(output_md)
    f.close()
