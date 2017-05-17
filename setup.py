import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as buf:
        return buf.read()


conf = dict(
        name='valeriovive',
        version='0.1',
        description='Twitter Filter Bubble Experiment',
        long_description=read('README.md'),
        author='cocconat',
        author_email='g3-3k@paranoici.org',
        url='https://github.com/g3-3k/valeriovive',
        license='AGPL',
        packages=['valeriovive'],
        install_requires=[
            'tweepy',
            'pymongo',
            'mutagen',
            'logging',
        ],
        zip_safe=False,

        classifiers=[
          "License :: OSI Approved :: GNU Affero General Public License v3",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2",
        ])


if __name__ == '__main__':
    setup(**conf)
