project('efimirror')

libexec_dir = get_option('prefix') / get_option('libexecdir') / 'efimirror'
conf_dir = get_option('prefix') / get_option('sysconfdir') / 'efimirror'

functions_conf_data = configuration_data({
  'config_path': conf_dir,
})

configure_file(input: 'src/functions.sh.in',
  output: 'functions.sh', install_dir: libexec_dir, install_mode: 'rwxr-xr-x',
  configuration: functions_conf_data)

functions_path = libexec_dir / 'functions.sh'

sync_conf_data = configuration_data({
  'lsyncd_exe': get_option('lsyncd-exe'),
  'boot_efi_dir': get_option('boot-efi-dir'),
  'functions_path' : functions_path,
})

configure_file(input: 'src/bin/sync.sh.in',
  output: 'efimirror-sync', install_dir: libexec_dir, install_mode: 'rwxr-xr-x',
  configuration: sync_conf_data)

generator_conf_data = configuration_data({
  'boot_efi_dir': get_option('boot-efi-dir'),
  'sync_script_path': libexec_dir / 'efimirror-sync',
  'functions_path' : functions_path,
})

configure_file(input: 'src/bin/systemd-generator.sh.in',
  output: 'efimirror-mount-generator', install_dir: libexec_dir, install_mode: 'rwxr-xr-x',
  configuration: generator_conf_data)

# Make sure symlink is relative for RPM
generator_install_dir = get_option('prefix') / get_option('systemd-generator-dir')
generator_link_target = run_command(
  'realpath', '-m', '--relative-to', generator_install_dir,
  libexec_dir / 'efimirror-mount-generator',
  check: true,
).stdout().strip()

install_symlink('efimirror-mount-generator', install_dir: generator_install_dir,
  pointing_to: generator_link_target
)

conf_conf_data = configuration_data({
  'default_mount_opts' : get_option('default-mount-opts'),
  'boot_efi_instance_dir': get_option('boot-efi-instance-dir'),
})

configure_file(input: 'src/conf/efimirror.in',
  output: 'config', install_dir: conf_dir, install_mode: 'rw-r--r--',
  configuration: conf_conf_data)
