
project(
	'aimation',
	version: '0.1',
	meson_version: '>= 0.50.0',
)
app_uuid = 'com.github.elbley.aimation'


gnome = import('gnome')


subdir('src')
subdir('data')

meson.add_install_script('build-aux/meson/postinstall.py')
