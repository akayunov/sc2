import subprocess
import os.path

scr_dir = os.path.dirname(os.path.realpath(__file__))
tmp_dir = os.path.join(os.path.dirname(scr_dir), 'tmp')
subprocess.call([
    os.path.join(scr_dir, '../v/bin/pytest'),
    '--cov-config', os.path.join(scr_dir, '../.coveragerc'),
    '--cov', os.path.join(scr_dir, '../src'),
    '--cov', os.path.join(scr_dir, '../bin'),
    '--cov', os.path.join(scr_dir, '../test'),
    '--cov-report', 'html:' + tmp_dir + '/cov_html',
    os.path.join(scr_dir, '../test')]
)
os.unlink('.coverage')
