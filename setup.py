import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as buf:
        return buf.read()


conf = dict(
        name='tiber',
        version='0.1',
        description='Twitter fIlter Bubble ExpeRiment',
        long_description=read('README.md'),
        author='cocconat',
        author_email='g3-3k@paranoici.org',
        url='https://github.com/g3-3k/tiber',
        license='AGPL',
        packages=['tiber'],
        install_requires=[
            'tweepy',
            'pymongo',
            'mutagen',
        ],
        zip_safe=False,

        classifiers=[
          "License :: OSI Approved :: GNU Affero General Public License v3",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2",
        ])


if __name__ == '__main__':
    setup(**conf)
