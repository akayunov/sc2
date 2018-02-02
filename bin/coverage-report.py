import subprocess
import os.path

bin_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(bin_dir)
tmp_dir = os.path.join(src_dir, 'tmp')

pytest_path = 'pytest' if not os.path.isdir(src_dir + '/v') else 'v/bin/pytest'

subprocess.call([
    os.path.join(pytest_path),
    '--cov-config', os.path.join(src_dir, '.coveragerc'),
    '--cov', os.path.join(src_dir, 'src'),
    '--cov', os.path.join(src_dir, 'bin'),
    '--cov', os.path.join(src_dir, 'test'),
    '--cov-report', 'html:' + tmp_dir + '/cov_html',
    os.path.join(src_dir, 'test')]
)
try:
    os.unlink('.coverage')
except OSError as e:
    if e.errno == 2:
        pass
    else:
        raise
