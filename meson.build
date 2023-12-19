project('efimirror')

sync_conf_data = configuration_data({
  'lsyncd_exe': get_option('lsyncd-exe'),
  'boot_efi_dir': get_option('boot-efi-dir'),
})

libexec_dir = join_paths(get_option('prefix'), get_option('libexecdir'), 'efimirror')

sync_exe = configure_file(input : 'src/sync.sh.in',
  output : 'efimirror-sync', install_dir: libexec_dir, install_mode: 'rwxr-xr-x',
  configuration : sync_conf_data)

generator_conf_data = configuration_data({
  'boot_efi_dir': get_option('boot-efi-dir'),
  'boot_efi_instance_dir': get_option('boot-efi-instance-dir'),
  'env_file_path': join_paths(get_option('prefix'), get_option('sysconfdir'), 'default', 'efimirror'),
  'sync_script_path': join_paths(libexec_dir, 'efimirror-sync'),
})

generator_exe = configure_file(input : 'src/systemd-generator.sh.in',
  output : 'efimirror-mount-generator', install_dir: libexec_dir, install_mode: 'rwxr-xr-x',
  configuration : generator_conf_data)

install_symlink('efimirror-mount-generator', install_dir: get_option('systemd-generator-dir'),
  pointing_to: join_paths(libexec_dir, 'efimirror-mount-generator'))
