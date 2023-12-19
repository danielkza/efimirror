project('efimirror')

sync_conf_data = configuration_data({
  'lsyncd_exe': get_option('lsyncd-exe'),
  'boot_efi_dir': get_option('boot-efi-dir'),
})

libexec_dir = get_option('prefix') / get_option('libexecdir') / 'efimirror'

sync_exe = configure_file(input: 'src/bin/sync.sh.in',
  output: 'efimirror-sync', install_dir: libexec_dir, install_mode: 'rwxr-xr-x',
  configuration: sync_conf_data)

conf_env_dir = get_option('config-env-dir') != '' ? get_option('config-env-dir') : (get_option('sysconfdir') /  'default')
env_file_path = conf_env_dir / 'efimirror'

generator_conf_data = configuration_data({
  'boot_efi_dir': get_option('boot-efi-dir'),
  'env_file_path': env_file_path,
  'sync_script_path': libexec_dir / 'efimirror-sync',
})

generator_exe = configure_file(input: 'src/bin/systemd-generator.sh.in',
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

conf_file = configure_file(input: 'src/conf/efimirror.in',
  output: 'efimirror', install_dir: conf_env_dir, install_mode: 'rw-r--r--',
  configuration: conf_conf_data)
