""" analytics-web setuptools """

import os
import subprocess
import distutils.cmd
import distutils.log
import distutils.command.clean
import distutils.command.build
import setuptools.command.sdist
import setuptools.command.develop
import setuptools.command.install
from setuptools import setup, find_packages
from pip.req import parse_requirements

# analytics-web version
__VERSION__ = "v0.0.7"

# get path to npm command for environment
npm_cmd = os.popen('which npm').read().rstrip()
node_bin = os.popen("%s bin" % npm_cmd).read().rstrip()

# get requirements list from requirements.txt
install_reqs = parse_requirements(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'requirements.txt'))
reqs = [str(ir.req) for ir in install_reqs]

get_data_files = lambda root_dir: \
    [(root, [os.path.join(root, f) for f in files]) \
        for root, dirs, files in os.walk(root_dir)]

data_files = []
data_files.extend(get_data_files('config'))
data_files.extend([
    ('', ['requirements.txt', 'package.json', 'gulpfile.js'])])


class InstallNPMModulesCommand(distutils.cmd.Command):
    """Install NPM dependencies"""

    description = 'install NPM modules'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        assert npm_cmd != None, ('npm: command not found')
        npm_install_command = [npm_cmd, 'install']
        self.announce(
            'Running command: %s' % str(npm_install_command),
            level=distutils.log.INFO)
        subprocess.check_call(npm_install_command)


class BundleStaticCommand(distutils.cmd.Command):
    """Install NPM dependencies"""

    description = 'bundle static resources'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def check_node_modules(self):
        return not os.path.isdir(node_bin)

    def run(self):
        """Run command."""
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)
        # add node_bin to environment PATH if not present
        if node_bin not in os.environ['PATH']:
            os.environ['PATH'] = ":".join([node_bin, os.getenv('PATH')])
        # get path to gulp command for environment
        gulp_cmd = os.popen('which gulp').read().rstrip()
        assert gulp_cmd != None, ('gulp: command not found')
        gulp_build = [gulp_cmd, 'build']
        self.announce(
            'Running command: %s' % str(gulp_build),
            level=distutils.log.INFO)
        subprocess.check_call(gulp_build)

    sub_commands = [('install_npm_modules', check_node_modules)]


# Prefix all major commands with `bundle_static`
# Update data_files post-bundle

class SDistCommand(setuptools.command.sdist.sdist):
    """Install and bundle static resources before sdist"""

    def run(self):
        self.run_command('bundle_static')
        self.distribution.data_files.extend(get_data_files('public_dist'))
        setuptools.command.sdist.sdist.run(self)


class BuildCommand(distutils.command.build.build):
    """Install and bundle static resources before develop"""

    def run(self):
        self.run_command('bundle_static')
        self.distribution.data_files.extend(get_data_files('public_dist'))
        distutils.command.build.build.run(self)

class DevelopCommand(setuptools.command.develop.develop):
    """Install and bundle static resources before develop"""

    def run(self):
        self.run_command('bundle_static')
        self.distribution.data_files.extend(get_data_files('public_dist'))
        setuptools.command.develop.develop.run(self)


class InstallCommand(setuptools.command.install.install):
    """Install and bundle static resources before install"""

    def run(self):
        self.run_command('bundle_static')
        self.distribution.data_files.extend(get_data_files('public_dist'))
        setuptools.command.install.install.do_egg_install(self)


class CleanCommand(distutils.command.clean.clean):
    """Custom clean command."""

    clean_dirs = ['public_dist']

    def initialize_options(self):
        distutils.command.clean.clean.initialize_options(self)
        self.all = True

    def run(self):
        for _dir in self.clean_dirs:
            if os.path.isdir(_dir):
                print "removing '%s'" % _dir
                for root, dirs, files in os.walk(_dir, topdown=False):
                    for f in files:
                        os.remove(os.path.join(root, f))
                    for d in dirs:
                        os.rmdir(os.path.join(root, d))
                os.rmdir(_dir)
            else:
                print "'%s' does not exist -- can't clean it" % _dir
        distutils.command.clean.clean.run(self)


setup(
    name="nest_m",
    version=__VERSION__,
    author="David Stolfo",
    author_email="david.stolfo@gmail.com",
    #url="",
    description="Nest+m course material",
    install_requires=reqs,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'nest_m_static': 'web/nest_m/static/*',
        'nest_m_templates': 'web/nest_m/templates/*',
    },
    data_files=data_files,
    cmdclass={
        'install_npm_modules': InstallNPMModulesCommand,
        'bundle_static': BundleStaticCommand,
        'build': BuildCommand,
        'sdist': SDistCommand,
        'develop': DevelopCommand,
        'install': InstallCommand,
        'clean': CleanCommand,
    },
    entry_points={
        'console_scripts': [
            'start_server = web.server:main',
        ]
    },
)
