project('ic',
		version: '1.0.0')

source = 'ic'

python = import('python')
python_install = python.find_installation('python3')

# configuration = configuration_data()
# configuration.set('name', meson.project_name())
# configuration.set('version', meson.project_version())
# source = configure_file(input: 'git-hud.in',
# 						output: 'git-hud',
# 						configuration: configuration)

install_data(source, install_dir: './bin', install_mode: 'rwxr-xr-x')
