from setuptools import setup

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

def get_requirements() -> list:
    """Return requirements as list
	
	from: https://stackoverflow.com/questions/69842651/parse-error-in-pip-e-gith-expected-wabcd
	"""
    with open('requirements.txt') as f:
        packages : list = []
        for line in f:
            line = line.strip()
            # let's also ignore empty lines and comments
            if not line or line.startswith('#'):
                continue
            if 'https://' in line:
                # tail = line.rsplit('/', 1)[1]
                # tail = tail.split('#')[0]
                # line = tail.replace('@', '==').replace('.git', '')
                if (line.count('#egg=') != 1) or (not line.startswith('-e ')):
                    raise ValueError(f'cant parse required package: {line}')

                pckgname : str = line.split('#egg=')[-1]

                line = pckgname + ' @ ' + line.split('-e ', 1)[-1].strip()

            packages.append(line)
    return packages


setup(name='csm_functions',
	version='0.1',
	description='A Python package for hierarchical Bayesian inversion of electrochemical impedance data',
	long_description=long_description,
    long_description_content_type="text/markdown",
	url='https://github.com/C-Meisel/CSM_Functions',
	author='Charlie Meisel',
	author_email='cmeisel@mines.edu',
	packages=['CSM_functions'],
	install_requires = get_requirements(),
	)