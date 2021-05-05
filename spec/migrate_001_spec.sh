Describe 'bldr gen.up'
  Include venv/bin/activate
  setup() {
    setup_w_bldr
  }
  cleanup() {
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'

  It 'Runs 001_bldr_history.py'
    rm .bldr/migrated.toml
    When call bldr gen.up
    
    The path .bldr/migrated.toml should be exist
    The path .bldr/migrated.toml contents should include "001_bldr_history.py"

  End
End