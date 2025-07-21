from setuptools import setup, find_packages

setup(
    name='super_glitch_bot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List dependencies here
    ],
    entry_points={
        'console_scripts': [
            'super_glitch_bot = super_glitch_bot.main:main',
        ],
    },
)
