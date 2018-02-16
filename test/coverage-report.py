import subprocess
import os.path

TEST_DIR = os.path.dirname(os.path.realpath(__file__))  # test
SRC_DIR = os.path.dirname(TEST_DIR)
TMP_DIR = os.path.join(SRC_DIR, 'tmp')

PYTEST_PATH = 'pytest' if not os.path.isdir(SRC_DIR + '/v') else 'v/bin/pytest'

subprocess.call([
    os.path.join(PYTEST_PATH),
    '--cov-config', os.path.join(SRC_DIR, '.coveragerc'),
    '--cov', os.path.join(SRC_DIR, 'src'),
    '--cov', os.path.join(SRC_DIR, 'test'),
    '--cov-report', 'html:' + TMP_DIR + '/cov_html',
    os.path.join(SRC_DIR, 'test')]
               )

if os.path.isdir(SRC_DIR + '/v'):
    try:
        os.unlink('.coverage')
    except OSError as e:
        if e.errno == 2:
            pass
        else:
            raise
