
Describe 'bldr --help'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_dir
    bldr init > /dev/null
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