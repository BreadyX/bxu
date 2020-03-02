project('git-hud',
		version: '2.0.3')

python = import('python')
python_install = python.find_installation('python3')

configuration = configuration_data()
configuration.set('name', meson.project_name())
configuration.set('version', meson.project_version())
source = configure_file(input: 'git-hud.in',
						output: 'git-hud',
						configuration: configuration)

# python_install.install_sources(source,
#							   install_dir: './bin')

install_data(source, install_dir: './bin', install_mode: 'rwxr-xr-x')
