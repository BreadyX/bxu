project('bat-hud',
		version: '1.0.0')

python = import('python')
python_install = python.find_installation('python3')

configuration = configuration_data()
configuration.set('name', meson.project_name())
configuration.set('version', meson.project_version())
source = configure_file(input: 'bat-hud.in',
						output: 'bat-hud',
						configuration: configuration)

install_data(source, install_dir: './bin', install_mode: 'rwxr-xr-x')
