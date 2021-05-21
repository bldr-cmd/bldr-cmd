
Describe 'bldr --help'                                                                                           
  Include spec/venv_inc
  setup() {  
    setup_w_bldr
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Shows Help'
    When call bldr --help
    The output should match pattern '*Usage: bldr *'
    The output should match pattern '*Options:*'
    The output should match pattern '*--help         Show this message and exit.*'
    The output should match pattern '*Commands:*'
  End 
End   