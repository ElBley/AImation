
################################################################################
# Installation and validation of the .desktop file #############################

desktop_files_dir = join_paths(get_option('datadir'), 'applications')

install_data(
	app_uuid + '.desktop.in',
	install_rename: app_uuid + '.desktop',
	install_dir: desktop_files_dir
)
desktop_file = desktop_files_dir / app_uuid + '.desktop'


desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
	test('Validate desktop file', desktop_utils, args: [desktop_file])
endif


################################################################################
# Installation and validation of the .gschema file #############################

install_data(
	app_uuid + '.gschema.xml',
	install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
	test(
		'Validate schema file',
		compile_schemas,
		args: ['--strict', '--dry-run', meson.current_source_dir()]
	)
endif

################################################################################

subdir('icons')

